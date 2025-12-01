#!/usr/bin/env python3
"""
Module for generating letters of recommendation.

This module:
1. Loads style guide and student packet
2. Combines them with letter generation prompt
3. Calls LLM to generate letter
4. Saves draft as markdown
5. Optionally converts to DOCX
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from lor.llm import call_llm

logger = logging.getLogger(__name__)


def load_prompt_template() -> str:
    """Load the letter generation prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "generate_letter.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_style_guide(style_guide_path: Path) -> str:
    """Load the style guide."""
    if not style_guide_path.exists():
        raise FileNotFoundError(f"Style guide not found at {style_guide_path}")

    with open(style_guide_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_student_packet(student_dir: Path) -> str:
    """Load the student packet."""
    packet_path = student_dir / "student_packet.md"

    if not packet_path.exists():
        raise FileNotFoundError(
            f"Student packet not found at {packet_path}\n"
            f"Run 'lor synthesize-packet {student_dir}' first."
        )

    with open(packet_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if professor's perspective is completed
    if "[TO BE COMPLETED MANUALLY BY PROFESSOR]" in content:
        logger.warning(
            "\n" + "="*60 +
            "\nWARNING: Student packet contains placeholder text:\n"
            "'[TO BE COMPLETED MANUALLY BY PROFESSOR]'\n"
            "\nThe generated letter may be incomplete without the professor's\n"
            "personal observations and assessment. Consider completing this\n"
            "section before generating the letter.\n" +
            "="*60
        )

    return content


def combine_for_letter_generation(
    prompt_template: str,
    style_guide: str,
    student_packet: str
) -> str:
    """
    Combine prompt, style guide, and student packet for letter generation.

    Args:
        prompt_template: The letter generation prompt
        style_guide: Professor's writing style guide
        student_packet: Student's information packet

    Returns:
        Complete prompt for LLM
    """
    full_prompt = f"""{prompt_template}

{'='*80}

# STYLE GUIDE

{style_guide}

{'='*80}

# STUDENT PACKET

{student_packet}

{'='*80}

Now, generate a complete letter of recommendation in Professor Gormley's style for this student.

Remember:
- Use ONLY information from the student packet above
- Write in Professor Gormley's distinctive voice using the style guide
- Include specific details, course numbers, and concrete examples
- Follow the structural patterns from the style guide
- Output in Markdown format with proper letterhead
- Current date: {datetime.now().strftime("%B %d, %Y")}
"""

    logger.info(f"Combined prompt size: {len(full_prompt.split())} words")
    return full_prompt


def generate_letter(
    student_dir: Path,
    style_guide_path: Path,
    output_filename: str = "letter_draft.md"
) -> Path:
    """
    Generate a letter of recommendation for a student.

    Args:
        student_dir: Path to student directory containing student_packet.md
        style_guide_path: Path to style guide (defaults to data/style_guide/style_guide.md)
        output_filename: Name for output file (default: letter_draft.md)

    Returns:
        Path to generated letter

    Expected structure:
        student_dir/
        ├── student_packet.md     # Must exist
        └── output/
            └── letter_draft.md   # Created by this function
    """
    logger.info(f"{'='*60}")
    logger.info(f"Generating letter for: {student_dir.name}")
    logger.info(f"{'='*60}")

    # Load components
    logger.info("Loading letter generation prompt template...")
    prompt_template = load_prompt_template()

    logger.info(f"Loading style guide from: {style_guide_path}")
    style_guide = load_style_guide(style_guide_path)
    logger.info(f"Style guide loaded ({len(style_guide.split())} words)")

    logger.info(f"Loading student packet from: {student_dir / 'student_packet.md'}")
    student_packet = load_student_packet(student_dir)
    logger.info(f"Student packet loaded ({len(student_packet.split())} words)")

    # Combine for prompt
    full_prompt = combine_for_letter_generation(
        prompt_template,
        style_guide,
        student_packet
    )

    # Call LLM to generate letter
    logger.info("Sending to LLM for letter generation...")
    logger.info("This may take 1-2 minutes as the LLM crafts the letter...")

    letter = call_llm(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at writing letters of recommendation that "
                    "authentically capture a professor's distinctive writing style while "
                    "accurately representing student qualifications. You never hallucinate "
                    "or invent details not provided in the source materials."
                )
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        temperature=0.7,  # Balanced between creativity (style) and consistency (facts)
    )

    logger.info("Successfully received letter from LLM")

    # Create output directory and save
    output_dir = student_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / output_filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(letter)

    logger.info(f"Letter saved to: {output_path}")
    logger.info(f"Size: {len(letter.split())} words")

    # Log completion with next steps
    logger.info(f"\n{'='*60}")
    logger.info("Letter generation complete!")
    logger.info(f"{'='*60}")
    logger.info("\nNext steps:")
    logger.info(f"1. Review the generated letter: {output_path}")
    logger.info("2. Verify all facts are accurate")
    logger.info("3. Check that the writing sounds authentic")
    logger.info("4. Edit as needed for voice and content")
    logger.info("5. Convert to DOCX if needed")
    logger.info(f"{'='*60}")

    return output_path
