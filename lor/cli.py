#!/usr/bin/env python3
"""
Click-based CLI for letter of recommendation tools.

This CLI provides multiple subcommands for managing letters of recommendation:
- redact: Redact student information from Word documents
- (future subcommands can be added here)
"""

import logging
import click
import pathlib
from dotenv import load_dotenv

from lor.redact_student_info import process_all
from lor.extract_style import extract_style_guide
from lor.synthesize_packet import synthesize_student_packet
from lor.generate_letter import generate_letter
from lor.file_utils import convert_markdown_to_docx

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
    extract_style_guide(pathlib.Path(redacted_letters_dir), pathlib.Path(output))


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
        ├── statement.pdf (or .docx, .txt)
        └── professor_notes.md (REQUIRED - use templates/professor_notes.md as starting point)

    IMPORTANT: Before running this command, you must:
    1. Copy templates/professor_notes.md to student_dir/input/professor_notes.md
    2. Fill in the professor notes with your observations and assessment

    The script will:
    1. Find and convert all materials to markdown (saved in student_dir/markdown/)
    2. Send materials to LLM for analysis and extraction
    3. Generate structured student packet (saved as student_dir/student_packet.md)

    The generated packet includes:
    - Student Profile (metadata, including pronouns from professor notes)
    - Academic Performance (from transcript)
    - Teaching Assistant Work (from accomplishments and professor notes)
    - Research Contributions (from accomplishments and professor notes)
    - Goals and Experience Alignment (from statement)
    - Strengths from Professor's Perspective (from professor notes)
    - Additional Information (from all materials)

    After generation, review the packet and verify all information is accurate.

    Examples:

        lor synthesize-packet data/students/jane_smith/

        lor synthesize-packet data/students/john_doe/
    """
    synthesize_student_packet(pathlib.Path(student_dir))


@cli.command()
@click.argument('student_dir', type=click.Path(exists=True))
@click.option('--style-guide', default='data/style_guide/style_guide.md', type=click.Path(exists=True), help='Path to style guide')
@click.option('--output', default='letter_draft.md', help='Output filename')
def generate_letter_cmd(student_dir, style_guide, output):
    """
    Generate letter of recommendation for a student.

    STUDENT_DIR should contain a completed student_packet.md file
    (generated by the 'synthesize-packet' command).

    The script will:
    1. Load the style guide (Professor's writing patterns)
    2. Load the student packet (student's information and professor's assessment)
    3. Combine them with letter generation prompt
    4. Generate letter draft using LLM
    5. Save as markdown in student_dir/output/
    6. Convert to DOCX

    Prerequisites:
    - Style guide must exist (from Phase 1: lor extract-style)
    - Student packet must exist (from Phase 2: lor synthesize-packet)

    After generation, you must:
    1. Review the letter for accuracy
    2. Verify all facts match the student packet
    3. Check that the voice sounds authentic
    4. Edit as needed before sending

    Examples:

        # Generate markdown letter
        lor generate-letter data/students/jane_smith/

        # Generate and convert to DOCX
        lor generate-letter data/students/jane_smith/ --docx

        # Use custom style guide
        lor generate-letter data/students/jane_smith/ --style-guide custom_style.md

        # Custom output filename
        lor generate-letter data/students/jane_smith/ --output letter_stanford.md
    """
    student_path = pathlib.Path(student_dir)
    # Generate letter
    letter_path = generate_letter(
        student_path,
        style_guide_path=pathlib.Path(style_guide),
        output_filename=output
    )
    logger.info("\nConverting to DOCX format...")
    docx_path = convert_markdown_to_docx(letter_path)
    logger.info(f"DOCX saved to: {docx_path}")


@cli.command()
@click.argument('student_dir', type=click.Path(exists=True))
@click.option('--style-guide', default='data/style_guide/style_guide.md', type=click.Path(exists=True), help='Path to style guide')
@click.option('--output', default='letter_draft.md', help='Output filename')
def packet_and_letter(student_dir, style_guide, output):
    """
    Synthesize student packet and generate letter in one command.

    STUDENT_DIR should be a student-specific directory containing an 'input/'
    subdirectory with the student's application materials and professor_notes.md.

    This command combines 'synthesize-packet' and 'generate-letter' into a single
    workflow, using all default settings.

    The script will:
    1. Synthesize student packet from application materials
    2. Generate letter of recommendation using default style guide
    3. Convert letter to DOCX format

    Prerequisites:
    - All input materials must be in student_dir/input/
    - professor_notes.md must be completed (use templates/professor_notes.md)
    - Style guide must exist at data/style_guide/style_guide.md

    Examples:

        lor packet-and-letter data/students/jane_smith/
    """
    student_path = pathlib.Path(student_dir)
    
    logger.info("Step 1: Synthesizing student packet...")
    synthesize_student_packet(student_path)
    
    logger.info("\nStep 2: Generating letter of recommendation...")
    
    letter_path = generate_letter(
        student_path,
        style_guide_path=pathlib.Path(style_guide),
        output_filename=output,
    )
    
    logger.info("\nStep 3: Converting to DOCX format...")
    docx_path = convert_markdown_to_docx(letter_path)
    logger.info(f"DOCX saved to: {docx_path}")
    
    logger.info("\n✓ Complete! Packet and letter generated successfully.")

if __name__ == '__main__':
    cli()
