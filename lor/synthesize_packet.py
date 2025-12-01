#!/usr/bin/env python3
"""
Module for synthesizing student packets from application materials.

This module:
1. Finds student materials in input/ directory
2. Converts them to markdown
3. Sends them to LLM with synthesis prompt
4. Generates structured student packet
"""

import logging
from pathlib import Path
from typing import Dict, Optional
from lor.llm import call_llm
from lor.file_utils import (
    find_student_materials,
    convert_file_to_markdown,
    save_markdown
)

logger = logging.getLogger(__name__)


def load_prompt_template() -> str:
    """Load the student packet synthesis prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "synthesize_student_packet.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def convert_materials_to_markdown(student_dir: Path) -> Dict[str, str]:
    """
    Find and convert all student materials to markdown.

    Args:
        student_dir: Student directory containing input/ subfolder

    Returns:
        Dictionary mapping material type to markdown content
    """
    input_dir = student_dir / "input"
    markdown_dir = student_dir / "markdown"
    markdown_dir.mkdir(parents=True, exist_ok=True)

    # Find student materials
    materials = find_student_materials(input_dir)

    if not materials:
        raise ValueError(f"No student materials found in {input_dir}")

    logger.info(f"Found {len(materials)} material(s): {', '.join(materials.keys())}")

    # Convert each material to markdown
    markdown_contents = {}

    for material_type, file_path in materials.items():
        logger.info(f"Processing {material_type}: {file_path.name}")

        # Convert to markdown
        markdown_content = convert_file_to_markdown(file_path)

        # Save to markdown/ directory
        output_filename = f"{material_type}.md"
        output_path = markdown_dir / output_filename
        save_markdown(markdown_content, output_path)

        # Store content
        markdown_contents[material_type] = markdown_content

    return markdown_contents


def combine_materials_for_prompt(materials: Dict[str, str], prompt_template: str) -> str:
    """
    Combine the prompt template with student materials.

    Args:
        materials: Dict mapping material type to markdown content
        prompt_template: The synthesis prompt template

    Returns:
        Complete prompt with materials appended
    """
    sections = []

    # Add each material with clear labels
    material_labels = {
        'resume': 'Resume/CV',
        'transcript': 'Academic Transcript',
        'accomplishments': 'Accomplishments List',
        'statement': 'Personal Statement'
    }

    for material_type in ['resume', 'transcript', 'accomplishments', 'statement']:
        if material_type in materials:
            label = material_labels.get(material_type, material_type.title())
            content = materials[material_type]
            sections.append(f"## {label}\n\n{content}")
        else:
            label = material_labels.get(material_type, material_type.title())
            sections.append(f"## {label}\n\n[NOT PROVIDED]")

    combined_materials = "\n\n" + ("="*80 + "\n\n").join(sections)

    full_prompt = f"{prompt_template}\n\n{'='*80}\n\n# Student Materials\n{combined_materials}"

    logger.info(f"Combined prompt size: {len(full_prompt.split())} words")
    return full_prompt


def synthesize_student_packet(student_dir: Path) -> None:
    """
    Synthesize a student packet from materials in the student directory.

    Args:
        student_dir: Path to student directory (e.g., data/students/jane_smith/)

    Expected structure:
        student_dir/
        ├── input/
        │   ├── resume.pdf
        │   ├── transcript.pdf
        │   ├── accomplishments.txt
        │   └── statement.pdf
        ├── markdown/          # Created by this function
        │   ├── resume.md
        │   ├── transcript.md
        │   ├── accomplishments.md
        │   └── statement.md
        └── student_packet.md  # Created by this function
    """
    logger.info(f"{'='*60}")
    logger.info(f"Synthesizing student packet for: {student_dir.name}")
    logger.info(f"{'='*60}")

    # Load prompt template
    prompt_template = load_prompt_template()
    logger.info("Loaded synthesis prompt template")

    # Convert materials to markdown
    logger.info("Converting student materials to markdown...")
    markdown_contents = convert_materials_to_markdown(student_dir)

    # Combine with prompt
    full_prompt = combine_materials_for_prompt(markdown_contents, prompt_template)

    # Call LLM to synthesize packet
    logger.info("Sending materials to LLM for synthesis...")
    logger.info("This may take a minute as the LLM analyzes the materials...")

    student_packet = call_llm(
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting and organizing information from student application materials. You provide accurate, well-structured analysis without hallucinating details."
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        temperature=0.3,  # Lower temperature for factual extraction
    )

    logger.info("Successfully received student packet from LLM")

    # Save student packet
    output_path = student_dir / "student_packet.md"
    save_markdown(student_packet, output_path)

    logger.info(f"Student packet saved to: {output_path}")
    logger.info(f"Size: {len(student_packet.split())} words")
    logger.info(f"\n{'='*60}")
    logger.info("Student packet synthesis complete!")
    logger.info("Next steps:")
    logger.info(f"1. Review the generated packet: {output_path}")
    logger.info("2. Add 'Strengths from Professor's Perspective' section")
    logger.info("3. Verify all information is accurate")
    logger.info(f"{'='*60}")
