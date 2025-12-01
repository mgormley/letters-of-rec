#!/usr/bin/env python3
"""
Module for extracting writing style from redacted letters.

This module:
1. Reads redacted .md files from a directory
2. Sends them to an LLM with the style extraction prompt
3. Generates a comprehensive style guide
"""

import logging
from pathlib import Path
from typing import List
from lor.llm import call_llm

logger = logging.getLogger(__name__)


def load_prompt_template(prompt_path: Path) -> str:
    """Load the style extraction prompt template."""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def find_markdown_files(directory: Path) -> List[Path]:
    """Find all .md files in the given directory."""
    if not directory.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist")

    if not directory.is_dir():
        raise ValueError(f"Path '{directory}' is not a directory")

    md_files = sorted(directory.glob("*.md"))
    return md_files


def load_redacted_letters(md_files: List[Path]) -> str:
    """Load and concatenate all redacted letters with separators."""
    letters = []

    for md_file in md_files:
        logger.info(f"Loading: {md_file.name}")
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add separator and filename for context
        letters.append(f"# Letter: {md_file.stem}\n\n{content}")

    combined = "\n\n" + "="*80 + "\n\n".join(letters)
    logger.info(f"Loaded {len(md_files)} redacted letters ({len(combined.split())} words)")
    return combined


def extract_style_guide(redacted_letters_dir: Path, output_dir: Path) -> None:
    """
    Extract style guide from redacted letters.

    Args:
        redacted_letters_dir: Directory containing redacted .md files
        output_dir: Directory where style_guide.md will be saved
    """
    logger.info(f"{'='*60}")
    logger.info(f"Extracting style guide from: {redacted_letters_dir}")
    logger.info(f"{'='*60}")

    # Load prompt template
    prompt_path = Path(__file__).parent.parent / "prompts" / "extract_style_guide.md"
    prompt_template = load_prompt_template(prompt_path)
    logger.info("Loaded style extraction prompt template")

    # Find and load all redacted letters
    md_files = find_markdown_files(redacted_letters_dir)
    if not md_files:
        raise ValueError(f"No .md files found in {redacted_letters_dir}")

    redacted_letters = load_redacted_letters(md_files)

    # Combine prompt with letters
    full_prompt = f"{prompt_template}\n\n---\n\n## Redacted Letters to Analyze\n{redacted_letters}"

    # Call LLM to extract style
    logger.info("Sending letters to LLM for style extraction...")
    logger.info("This may take a minute as the LLM analyzes the writing patterns...")

    style_guide = call_llm(
        messages=[
            {
                "role": "system",
                "content": "You are an expert at analyzing writing style and creating comprehensive style guides. You provide detailed, structured analysis."
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    logger.info("Successfully received style guide from LLM")

    # Save style guide
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "style_guide.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(style_guide)

    logger.info(f"Style guide saved to: {output_path}")
    logger.info(f"Size: {len(style_guide.split())} words")
    logger.info(f"\n{'='*60}")
    logger.info("Style extraction complete!")
    logger.info("Please review and edit the style guide to ensure accuracy.")
    logger.info(f"{'='*60}")
