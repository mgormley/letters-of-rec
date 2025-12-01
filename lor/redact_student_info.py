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
from typing import Optional, Tuple
from lor.llm import call_llm

from lor.file_utils import save_markdown, convert_docx_to_markdown, find_docx_files

logger = logging.getLogger(__name__)


def load_redaction_prompt() -> str:
    """Load the redaction prompt template from file."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "redact_student_info.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


class DocumentRedactor:
    """Handles document redaction using an LLM API."""

    def __init__(self):
        """Initialize the redactor and load the prompt template."""
        self.redaction_prompt = load_redaction_prompt()

    def redact_text(self, text: str) -> str:
        """Use an LLM to redact student information from text."""
        logger.info("Sending text to LLM for redaction...")
        full_prompt = f"{self.redaction_prompt}\n\n{text}"
        redacted_text = call_llm(
            messages=[
                {"role": "system", "content": "You are a precise document redaction assistant."},
                {"role": "user", "content": full_prompt}
            ]
        )
        logger.info("Successfully received redacted text from LLM")
        return redacted_text

def process_document(docx_path: Path, out_dir: Path) -> bool:
    """Process a single document: convert, redact, and save.

    Args:
        docx_path: Path to the input .docx file
        out_dir: Directory where the output .md file will be saved

    Returns:
        True if successful, False otherwise
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing: {docx_path}")
    logger.info(f"{'='*60}")

    # Convert to Markdown
    markdown_text = convert_docx_to_markdown(docx_path)

    # Redact student information
    redactor = DocumentRedactor()
    redacted_text = redactor.redact_text(markdown_text)

    # Save to .md file in output directory with same basename
    output_filename = docx_path.stem + '.md'
    output_path = out_dir / output_filename
    save_markdown(redacted_text, output_path)


def process_all(in_path: str, out_dir: str) -> Tuple[int, int]:
    """
    Process all .docx files in the given path (file or directory).

    Args:
        in_path: Path to a .docx file or directory containing .docx files
        out_path: Directory where redacted .md files will be saved

    Returns:
        Tuple of (success_count, failure_count)
    """
    # Validate input path
    input_path = Path(in_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Path '{in_path}' does not exist")

    # Create output directory if it doesn't exist
    output_dir = Path(out_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")

    # Find all .docx files
    docx_files = find_docx_files(input_path)
    if not docx_files:
        raise ValueError("No .docx files found to process")

    # Process each document
    logger.info(f"Processing {len(docx_files)} document(s)...")
    for docx_file in docx_files:
        process_document(docx_file, output_dir)


