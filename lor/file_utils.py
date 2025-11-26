#!/usr/bin/env python3
"""
File utilities for letter of recommendation tools.

Handles file operations like finding documents, saving files, etc.
"""

import logging
from pathlib import Path
from typing import List
import mammoth

logger = logging.getLogger(__name__)

def convert_docx_to_markdown(docx_path: Path) -> str:
    """Convert a Word document to Markdown format, dropping all images."""
    try:
        logger.info(f"Converting {docx_path.name} to Markdown...")
        with open(docx_path, 'rb') as docx_file:
            # Configure mammoth to ignore images by returning empty strings
            result = mammoth.convert_to_markdown(
                docx_file,
                convert_image=mammoth.images.inline(lambda image: {"alt": ""})
            )
            markdown_text = result.value

            # Log any conversion warnings
            if result.messages:
                for message in result.messages:
                    logger.debug(f"Conversion message: {message}")

            logger.info(f"Successfully converted {docx_path.name} to Markdown (images dropped)")
            return markdown_text

    except Exception as e:
        logger.error(f"Error converting {docx_path}: {e}")
        raise

def find_docx_files(path: Path) -> List[Path]:
    """Find all .docx files in a path (file or directory)."""
    if path.is_file():
        if path.suffix.lower() == '.docx' and not path.name.startswith('~$'):
            return [path]
        else:
            logger.warning(f"File {path} is not a .docx file")
            return []
    elif path.is_dir():
        # Recursively find all .docx files, excluding temporary files
        docx_files = [f for f in path.rglob('*.docx') if not f.name.startswith('~$')]
        logger.info(f"Found {len(docx_files)} .docx file(s) in {path}")
        return docx_files
    else:
        logger.error(f"Path {path} does not exist")
        return []


def save_markdown(content: str, output_path: Path) -> None:
    """Save markdown content to a file."""
    try:
        logger.info(f"Saving content to {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Successfully saved {output_path}")

    except Exception as e:
        logger.error(f"Error saving file {output_path}: {e}")
        raise
