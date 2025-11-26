#!/usr/bin/env python3
"""
Script to redact student information from Word documents using OpenAI API.

This script:
1. Reads .docx files (single file or recursively from a directory)
2. Converts them to Markdown
3. Uses OpenAI API to identify and redact student information
4. Saves the redacted content as .md files

This module now serves as a high-level orchestrator for the redaction pipeline.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from lor.llm import call_llm

from lor.file_utils import save_markdown, convert_docx_to_markdown

logger = logging.getLogger(__name__)

class DocumentRedactor:
    """Handles document redaction using OpenAI API."""

    REDACTION_PROMPT = """You are a document redaction assistant. Your task is to identify and replace ALL student-identifying information with standardized placeholders.

Replace the following with these exact placeholders:
- Student names (full names, first names, last names) → [STUDENT_NAME]
- Student ID numbers → [STUDENT_ID]
- Student email addresses → [STUDENT_EMAIL]
- Other personal identifiers (phone numbers, addresses, etc.) → [STUDENT_INFO]

If there are multiple students, number the placeholders (e.g., [STUDENT_NAME_1], [STUDENT_NAME_2]).

IMPORTANT:
- Preserve ALL formatting, structure, line breaks, and markdown syntax exactly as written
- Do NOT modify or redact professor names, course names, institution names, or general content
- Only redact information that identifies specific students
- Return ONLY the redacted document without any additional commentary or explanation

Document to redact:

"""
    
    def redact_text(self, text: str) -> str:
        """Use an LLM to redact student information from text."""
        logger.info("Sending text to OpenAI for redaction...")
        redacted_text = call_llm(
            messages=[
                {"role": "system", "content": "You are a precise document redaction assistant."},
                {"role": "user", "content": self.REDACTION_PROMPT + text}
            ]
        )
        logger.info("Successfully received redacted text from LLM")
        return redacted_text

def process_all(path: str):
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
            if process_document(docx_file):
                success_count += 1
            else:
                failure_count += 1


def process_document(docx_path: Path) -> bool:
    """Process a single document: convert, redact, and save."""
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {docx_path}")
        logger.info(f"{'='*60}")

        # Convert to Markdown
        markdown_text = convert_docx_to_markdown(docx_path)
        
        # Redact student information
        redactor = DocumentRedactor()
        redacted_text = redactor.redact_text(markdown_text)

        # Save to .md file
        output_path = docx_path.with_suffix('.md')
        save_markdown(redacted_text, output_path)

        logger.info(f"✓ Successfully processed {docx_path.name}")
        return True

    except Exception as e:
        logger.error(f"✗ Failed to process {docx_path.name}: {e}")
        return False

