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

import logging
from pathlib import Path
from openai import OpenAI
from typing import Optional

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

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-5"):
        """Initialize the redactor with OpenAI API credentials."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        logger.info(f"Initialized DocumentRedactor with model: {model}")

    def redact_text(self, text: str) -> str:
        """Use OpenAI API to redact student information from text."""
        try:
            logger.info("Sending text to OpenAI for redaction...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise document redaction assistant."},
                    {"role": "user", "content": self.REDACTION_PROMPT + text}
                ],
                temperature=0.1  # Low temperature for consistency
            )

            redacted_text = response.choices[0].message.content
            logger.info("Successfully received redacted text from OpenAI")
            return redacted_text

        except Exception as e:
            logger.error(f"Error during OpenAI API call: {e}")
            raise


def process_document(docx_path: Path, dry_run: bool = False) -> bool:
    """Process a single document: convert, redact, and save."""
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {docx_path}")
        logger.info(f"{'='*60}")

        # Convert to Markdown
        markdown_text = convert_docx_to_markdown(docx_path)
        
        # Redact student information
        if not dry_run:
            redactor = DocumentRedactor()
            redacted_text = redactor.redact_text(markdown_text)
        else:
            logger.info("DRY RUN: Skipping OpenAI API call")
            redacted_text = markdown_text

        # Save to .md file
        output_path = docx_path.with_suffix('.md')
        if not dry_run:
            save_markdown(redacted_text, output_path)
        else:
            logger.info(f"DRY RUN: Would save to {output_path}")

        logger.info(f"✓ Successfully processed {docx_path.name}")
        return True

    except Exception as e:
        logger.error(f"✗ Failed to process {docx_path.name}: {e}")
        return False

