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
from lor.extract_style import extract_style_guide
from lor.synthesize_packet import synthesize_student_packet

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
@click.option('--in-path', default='data/original_letters/', type=click.Path(exists=True), help='Input directory or file containing .docx files')
@click.option('--out-path', default='data/redacted_letters/', type=click.Path(), help='Output directory for redacted .md files')
def redact(in_path, out_path):
    """
    Redact student information from Word documents.

    IN_PATH can be either:
    - A single .docx file
    - A directory (will recursively process all .docx files)

    OUT_PATH is the directory where redacted .md files will be saved.

    The script will:
    1. Convert Word documents to Markdown
    2. Use an LLM to identify and redact student information
    3. Save redacted content as .md files in OUT_PATH

    Examples:

        lor redact letter.docx

        lor redact ./letters/
    """
    process_all(in_path, out_path)


@cli.command()
@click.option('--redacted_letters_dir', default='data/redacted_letters/', type=click.Path(exists=True))
@click.option('--output', default='data/style_guide/', type=click.Path(), help='Output directory for style_guide.md')
def extract_style(redacted_letters_dir, output):
    """
    Extract writing style guide from redacted letters.

    REDACTED_LETTERS_DIR should contain .md files with redacted student information
    (typically created by the 'redact' command).

    The script will:
    1. Load all .md files from the directory
    2. Analyze writing patterns using an LLM
    3. Generate a comprehensive style guide
    4. Save as style_guide.md in OUTPUT directory

    The generated style guide captures:
    - Writing style characteristics (tone, vocabulary, sentence structure)
    - Letter structure patterns (opening, body, closing)
    - Example excerpts (reusable phrases with placeholders)

    Examples:

        lor extract-style data/redacted_letters/

        lor extract-style data/redacted_letters/ --output custom_output/
    """
    from pathlib import Path
    extract_style_guide(Path(redacted_letters_dir), Path(output))


@cli.command()
@click.argument('student_dir', type=click.Path(exists=True))
def synthesize_packet(student_dir):
    """
    Synthesize student packet from application materials.

    STUDENT_DIR should be a student-specific directory containing an 'input/'
    subdirectory with the student's application materials.

    Expected input structure:
        student_dir/input/
        ├── resume.pdf (or .docx, .txt)
        ├── transcript.pdf (or .docx, .txt)
        ├── accomplishments.txt (or .pdf, .docx)
        └── statement.pdf (or .docx, .txt)

    The script will:
    1. Find and convert all materials to markdown (saved in student_dir/markdown/)
    2. Send materials to LLM for analysis and extraction
    3. Generate structured student packet (saved as student_dir/student_packet.md)

    The generated packet includes:
    - Student Profile (metadata)
    - Academic Performance (from transcript)
    - Teaching Assistant Work (from accomplishments)
    - Research Contributions (from accomplishments)
    - Goals and Experience Alignment (from statement)
    - Placeholder for Professor's Perspective (to be completed manually)

    After generation, you must:
    1. Review the auto-generated sections
    2. Add the "Strengths from Professor's Perspective" section
    3. Verify all information is accurate

    Examples:

        lor synthesize-packet data/students/jane_smith/

        lor synthesize-packet data/students/john_doe/
    """
    from pathlib import Path
    synthesize_student_packet(Path(student_dir))


if __name__ == '__main__':
    cli()
