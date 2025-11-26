#!/usr/bin/env python3
"""
Script to redact student information from Word documents using OpenAI API.

This script:
1. Reads .docx files (single file or recursively from a directory)
2. Converts them to Markdown
3. Uses OpenAI API to identify and redact student information
4. Saves the redacted content as .md files
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

import mammoth
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
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

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
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


def convert_docx_to_markdown(docx_path: Path) -> str:
    """Convert a Word document to Markdown format."""
    try:
        logger.info(f"Converting {docx_path.name} to Markdown...")
        with open(docx_path, 'rb') as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            markdown_text = result.value

            # Log any conversion warnings
            if result.messages:
                for message in result.messages:
                    logger.debug(f"Conversion message: {message}")

            logger.info(f"Successfully converted {docx_path.name} to Markdown")
            return markdown_text

    except Exception as e:
        logger.error(f"Error converting {docx_path}: {e}")
        raise


def save_markdown(content: str, output_path: Path) -> None:
    """Save markdown content to a file."""
    try:
        logger.info(f"Saving redacted content to {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Successfully saved {output_path}")

    except Exception as e:
        logger.error(f"Error saving file {output_path}: {e}")
        raise


def process_document(docx_path: Path, redactor: DocumentRedactor, dry_run: bool = False) -> bool:
    """Process a single document: convert, redact, and save."""
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {docx_path}")
        logger.info(f"{'='*60}")

        # Convert to Markdown
        markdown_text = convert_docx_to_markdown(docx_path)

        # Redact student information
        if not dry_run:
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


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Redact student information from Word documents using OpenAI API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s letter.docx
  %(prog)s ./letters/
  %(prog)s ./letters/ --api-key YOUR_KEY
  %(prog)s ./letters/ --dry-run
  %(prog)s ./letters/ --model gpt-4-turbo
        """
    )

    parser.add_argument(
        'path',
        type=str,
        help='Path to a .docx file or directory containing .docx files'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key (can also be set via OPENAI_API_KEY environment variable)'
    )

    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4',
        help='OpenAI model to use (default: gpt-4)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be processed without making API calls'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate path
    input_path = Path(args.path).resolve()
    if not input_path.exists():
        logger.error(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)

    # Find all .docx files
    docx_files = find_docx_files(input_path)
    if not docx_files:
        logger.error("No .docx files found to process")
        sys.exit(1)

    # Initialize redactor (skip if dry run)
    if not args.dry_run:
        try:
            redactor = DocumentRedactor(api_key=args.api_key, model=args.model)
        except ValueError as e:
            logger.error(f"Error: {e}")
            sys.exit(1)
    else:
        redactor = None
        logger.info("DRY RUN MODE: No files will be modified")

    # Process each document
    logger.info(f"\nProcessing {len(docx_files)} document(s)...")
    success_count = 0
    failure_count = 0

    for docx_file in docx_files:
        if process_document(docx_file, redactor, dry_run=args.dry_run):
            success_count += 1
        else:
            failure_count += 1

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total files: {len(docx_files)}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {failure_count}")

    if failure_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
