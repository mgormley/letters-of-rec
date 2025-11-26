#!/usr/bin/env python3
"""
Click-based CLI for letter of recommendation tools.

This CLI provides multiple subcommands for managing letters of recommendation:
- redact: Redact student information from Word documents
- (future subcommands can be added here)
"""

import logging
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

from lor.redact_student_info import (
    DocumentRedactor,
    find_docx_files,
    process_document,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Letter of Recommendation Tools

    A collection of utilities for managing letters of recommendation,
    including student information redaction and document processing.
    """
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--api-key', type=str, help='OpenAI API key (can also be set via OPENAI_API_KEY environment variable)')
@click.option('--model', type=str, default='gpt-4', help='OpenAI model to use (default: gpt-4)')
@click.option('--dry-run', is_flag=True, help='Preview what would be processed without making API calls')
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
def redact(path, api_key, model, dry_run, verbose):
    """
    Redact student information from Word documents.

    PATH can be either:
    - A single .docx file
    - A directory (will recursively process all .docx files)

    The script will:
    1. Convert Word documents to Markdown
    2. Use OpenAI API to identify and redact student information
    3. Save redacted content as .md files

    Examples:

        lor redact letter.docx

        lor redact ./letters/

        lor redact ./letters/ --model gpt-4-turbo

        lor redact ./letters/ --dry-run
    """
    # Set logging level
    if verbose:
        logger.setLevel(logging.DEBUG)

    # Validate path
    input_path = Path(path).resolve()
    if not input_path.exists():
        click.echo(f"Error: Path '{path}' does not exist", err=True)
        sys.exit(1)

    # Find all .docx files
    docx_files = find_docx_files(input_path)
    if not docx_files:
        click.echo("Error: No .docx files found to process", err=True)
        sys.exit(1)

    # Initialize redactor (skip if dry run)
    if not dry_run:
        try:
            redactor = DocumentRedactor(api_key=api_key, model=model)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    else:
        redactor = None
        logger.info("DRY RUN MODE: No files will be modified")

    # Process each document
    logger.info(f"\nProcessing {len(docx_files)} document(s)...")
    success_count = 0
    failure_count = 0

    with click.progressbar(
        docx_files,
        label='Processing documents',
        item_show_func=lambda x: x.name if x else ''
    ) as bar:
        for docx_file in bar:
            if process_document(docx_file, redactor, dry_run=dry_run):
                success_count += 1
            else:
                failure_count += 1

    # Summary
    click.echo("\n" + "="*60)
    click.echo("SUMMARY")
    click.echo("="*60)
    click.echo(f"Total files: {len(docx_files)}")
    click.secho(f"Successful: {success_count}", fg='green' if success_count > 0 else None)
    click.secho(f"Failed: {failure_count}", fg='red' if failure_count > 0 else None)

    if failure_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    cli()
