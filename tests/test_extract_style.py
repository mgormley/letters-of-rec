#!/usr/bin/env python3
"""
Tests for style extraction functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from lor.extract_style import find_markdown_files, load_redacted_letters, extract_style_guide


def test_find_markdown_files(tmp_path):
    """Test finding markdown files in a directory."""
    # Create test markdown files
    (tmp_path / "letter1.md").write_text("# Letter 1")
    (tmp_path / "letter2.md").write_text("# Letter 2")
    (tmp_path / "other.txt").write_text("Not a markdown file")

    md_files = find_markdown_files(tmp_path)

    assert len(md_files) == 2
    assert all(f.suffix == ".md" for f in md_files)
    assert sorted([f.name for f in md_files]) == ["letter1.md", "letter2.md"]


def test_find_markdown_files_nonexistent_dir():
    """Test that nonexistent directory raises error."""
    with pytest.raises(FileNotFoundError):
        find_markdown_files(Path("/nonexistent/directory"))


def test_load_redacted_letters(tmp_path):
    """Test loading and combining redacted letters."""
    # Create test files
    letter1 = tmp_path / "letter1.md"
    letter1.write_text("This is letter 1 content.\n\n[STUDENT_NAME] is excellent.")

    letter2 = tmp_path / "letter2.md"
    letter2.write_text("This is letter 2 content.\n\n[STUDENT_NAME] is outstanding.")

    md_files = [letter1, letter2]
    combined = load_redacted_letters(md_files)

    # Check that both letters are included
    assert "letter1" in combined
    assert "letter2" in combined
    assert "This is letter 1 content" in combined
    assert "This is letter 2 content" in combined
    assert "[STUDENT_NAME]" in combined


@patch('lor.extract_style.call_llm')
def test_extract_style_guide_integration(mock_llm, tmp_path):
    """Test the full style extraction pipeline with mocked LLM."""
    # Setup input directory with test letters
    input_dir = tmp_path / "redacted"
    input_dir.mkdir()

    letter = input_dir / "test_letter.md"
    letter.write_text("""
# Letter of Recommendation

Dear Committee,

I am writing to enthusiastically recommend [STUDENT_NAME] for your program.
[STUDENT_NAME] was a student in my course and performed exceptionally well.

In conclusion, I give [STUDENT_NAME] my highest recommendation.

Sincerely,
Professor Smith
""")

    # Setup output directory
    output_dir = tmp_path / "style_guide"

    # Mock LLM response
    mock_style_guide = """# Style Guide

## Writing Style
- Enthusiastic and supportive tone
- Uses phrases like "enthusiastically recommend"

## Structure
- Opening: State purpose
- Body: Provide evidence
- Closing: Recommendation strength
"""
    mock_llm.return_value = mock_style_guide

    # Run extraction
    extract_style_guide(input_dir, output_dir)

    # Verify output file was created
    output_file = output_dir / "style_guide.md"
    assert output_file.exists()

    # Verify content
    content = output_file.read_text()
    assert content == mock_style_guide

    # Verify LLM was called with correct structure
    assert mock_llm.called
    call_args = mock_llm.call_args
    assert "messages" in call_args.kwargs
    messages = call_args.kwargs["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "style" in messages[0]["content"].lower()
    assert messages[1]["role"] == "user"
    assert "test_letter" in messages[1]["content"]
