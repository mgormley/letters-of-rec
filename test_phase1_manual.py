#!/usr/bin/env python3
"""
Manual test script for Phase 1 style extraction.
This script mocks the LLM call to test the pipeline without API keys.
"""

from pathlib import Path
from unittest.mock import patch
from lor.extract_style import extract_style_guide

def mock_llm_call(messages, model=None, temperature=None):
    """Mock LLM response for testing."""
    return """# Writing Style Guide for Professor Matthew R. Gormley

## 1. Style Guide - Core Writing Patterns

### Sentence Structure
- Predominantly uses compound and complex sentences with multiple clauses
- Average sentence length: 25-35 words, showing sophisticated academic writing
- Frequent use of parenthetical information for additional context (e.g., citations, course numbers)
- Uses em-dashes for clarifications and elaborations

### Vocabulary Level
- Academic and technical vocabulary appropriate for research contexts
- Domain-specific terminology used naturally (e.g., "reinforcement learning", "visual language model", "sample efficiency")
- Precise technical descriptors without oversimplification
- Course codes included for specificity (e.g., "10-703 *Deep Reinforcement Learning*")

### Tone
- Enthusiastic and strongly supportive
- Professional yet warm
- Measured in praise but unambiguous in recommendation strength
- Balances technical detail with accessibility

### Voice
- First person active voice ("I am writing", "I began working with")
- Direct and confident assertions
- Narrative structure that tells the story of student's growth

### Emphasis Techniques
- Superlatives backed by specific rankings ("top 1%", "strongest recommendation")
- Concrete project descriptions with technical details
- Progressive narrative showing trajectory ("rapidly rising trajectory")
- Comparison to peer groups explicitly stated

## 2. Structure Patterns - Letter Organization

### Opening Paragraph (150 words)
**Template:**
- Express "enthusiastic support" for application
- Establish current status of student (degree program, institution)
- State duration and nature of relationship
- End with clear recommendation statement ("strongest recommendation")

**Example Pattern:**
"I am writing to express my enthusiastic support for [STUDENT]'s application. [STUDENT] is currently [STATUS] at [INSTITUTION]. I began working with [STUDENT] in [TIME] on [PROJECT/CONTEXT], and we have [RECENT WORK]. [He/She] has my strongest recommendation."

### Body Paragraph Organization
**Project-Based Structure:**
- Each major project gets dedicated paragraph(s)
- Chronological progression (Fall 2023 → Spring 2024)
- Within each project:
  - Context and motivation
  - Technical approach and student's specific contributions
  - Challenges overcome
  - Results and current status

**Integration of Evidence:**
- Technical details embedded in narrative (not listed)
- Collaborative work acknowledged (co-authors named)
- Both completed work and ongoing research included

### Closing Structure
**Two-Paragraph Close:**

Paragraph 1 (Comparison):
- Explicit ranking among peer group
- Technical abilities assessment
- Research potential evaluation
- Trajectory statement

Paragraph 2 (Interpersonal/Summary):
- Collaboration skills
- Learning approach
- Relationship with literature/field
- Leadership qualities

Final Paragraph:
- Summary statement
- Reiteration of recommendation strength
- Offer to provide more information

### Length Guidelines
- Total: 800-900 words
- Opening: 100-150 words
- Each project paragraph: 150-200 words
- Comparison paragraph: 100 words
- Final summary: 75 words

## 3. Example Excerpts - Reusable Phrases

### Opening Lines
1. "I am writing to express my enthusiastic support for [STUDENT_NAME]'s application."
2. "[STUDENT_NAME] is currently working towards his/her [DEGREE] in [FIELD] at [INSTITUTION]."
3. "I began working with [STUDENT_NAME] in [SEMESTER/YEAR] on [PROJECT/CONTEXT]."
4. "[He/She] has my strongest recommendation."

### Relationship Establishment
1. "I began working with [STUDENT_NAME] in [TIME_PERIOD] on a [PROJECT_TYPE] project"
2. "Since [TIME_PERIOD], [STUDENT_NAME] has been working on [PROJECT]"
3. "We have, more recently, been working together on [PROJECT]"
4. "[STUDENT_NAME] is currently working towards [DEGREE]"

### Academic Strength Descriptions
1. "Compared to other [DEGREE] students in [DEPARTMENT] at [INSTITUTION], [STUDENT_NAME] ranks among the top [X]%"
2. "His/Her technical abilities are among the best students I have personally advised"
3. "[STUDENT_NAME] is clearly on a rapidly rising trajectory"
4. "As an undergrad he/she had done very well in his/her [FIELD] coursework including [COURSES]"
5. "[He/She] also took [COURSE_LEVEL] course, [COURSE_CODE] *[COURSE_NAME]*"
6. "His/Her research potential is very high"
7. "You would be fortunate to have him/her"

### Research Contribution Descriptions
1. "[STUDENT_NAME] prototyped the idea very quickly and was able to demonstrate its promise"
2. "[STUDENT_NAME]'s idea is to [TECHNICAL_APPROACH]"
3. "Our initial results are extremely promising and beat a strong baseline"
4. "[STUDENT_NAME] and his/her collaborator were very effective in the early phases at rapidly moving through the important steps"
5. "This work is ongoing, and we are now pivoting towards [NEXT_PHASE]"
6. "[STUDENT_NAME] established [TECHNICAL_IMPROVEMENT]"
7. "Now [he/she] has pivoted to scaling up the idea to state-of-the-art [CONTEXT]"

### Collaborative and Interpersonal Skills
1. "[STUDENT_NAME] works extremely well with others"
2. "[He/She] is already a highly competent researcher who understands how to read the literature of a subfield deeply"
3. "[He/She] also knows how to learn from my experience in the field"
4. "He/She has collaborated very closely with [COLLABORATOR] on their joint research"
5. "In this collaboration, [he/she] often takes the lead, creatively driving the direction of our work"

### Comparative Statements
1. "Compared to other [DEGREE] students in [DEPARTMENT] at [INSTITUTION], [STUDENT_NAME] ranks among the top [X]%"
2. "His/Her technical abilities are among the best students I have personally advised"

### Transition Phrases
1. "Since [TIME_PERIOD], [STUDENT_NAME] has been working on..."
2. "This work is ongoing, and we are now..."
3. "Our experiments will require [SCOPE]"
4. "Further, [he/she] has..."

### Closing Statements
1. "In summary, [STUDENT_NAME] has the makings of a strong [FIELD] researcher"
2. "[He/She] has my strongest recommendation"
3. "If I can be of further assistance, please feel free to contact me"
4. "You would be fortunate to have him/her"
"""

def main():
    """Run the manual test."""
    print("="*60)
    print("Phase 1 Manual Test: Style Extraction")
    print("="*60)
    print()

    # Setup paths
    redacted_dir = Path("data/redacted_letters")
    output_dir = Path("data/style_guide")

    # Check if redacted letters exist
    if not redacted_dir.exists():
        print(f"ERROR: {redacted_dir} does not exist")
        return

    md_files = list(redacted_dir.glob("*.md"))
    if not md_files:
        print(f"ERROR: No .md files found in {redacted_dir}")
        return

    print(f"Found {len(md_files)} redacted letter(s):")
    for f in md_files:
        print(f"  - {f.name}")
    print()

    # Run extraction with mocked LLM
    print("Running style extraction (with mocked LLM call)...")
    print()

    with patch('lor.extract_style.call_llm', side_effect=mock_llm_call):
        extract_style_guide(redacted_dir, output_dir)

    print()
    print("="*60)
    print("Test completed successfully!")
    print("="*60)
    print()
    print(f"Style guide saved to: {output_dir / 'style_guide.md'}")
    print()
    print("Next steps:")
    print("1. Review the generated style guide")
    print("2. Edit it to ensure accuracy")
    print("3. To run with actual LLM (requires API key):")
    print("   python3 -m lor.cli extract-style data/redacted_letters/")

if __name__ == "__main__":
    main()
