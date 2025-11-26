#!/usr/bin/env python3
"""
Click-based CLI for letter of recommendation tools.

This CLI provides multiple subcommands for managing letters of recommendation:
- redact: Redact student information from Word documents
- (future subcommands can be added here)
"""

import logging
import click
from dotenv import load_dotenv

from lor.redact_student_info import process_all

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
def redact(path):
    """
    Redact student information from Word documents.

    PATH can be either:
    - A single .docx file
    - A directory (will recursively process all .docx files)

    The script will:
    1. Convert Word documents to Markdown
    2. Use an LLM to identify and redact student information
    3. Save redacted content as .md files

    Examples:

        lor redact letter.docx

        lor redact ./letters/

        lor redact ./letters/ --model gpt-4-turbo

        lor redact ./letters/ --dry-run
    """
    process_all(path)


if __name__ == '__main__':
    cli()
