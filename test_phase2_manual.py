#!/usr/bin/env python3
"""
Manual test script for Phase 2 student packet synthesis.
This script creates mock student data and tests the synthesis pipeline without API keys.
"""

from pathlib import Path
from unittest.mock import patch
from lor.synthesize_packet import synthesize_student_packet
import tempfile
import shutil


MOCK_RESUME = """# Jane Smith
Email: jsmith@cmu.edu | Phone: (412) 555-1234

## Education
**Carnegie Mellon University**, Pittsburgh, PA
Bachelor of Science in Computer Science
Expected Graduation: May 2024
GPA: 3.85/4.0

## Experience

**Teaching Assistant** - CMU School of Computer Science
10-301 Introduction to Machine Learning (Spring 2023)
10-601 Machine Learning (Fall 2023)
- Held 6 hours of office hours per week
- Graded homework and exams
- Led recitation sections

**Research Assistant** - CMU Machine Learning Department
Summer 2023 - Present
- Working on efficient fine-tuning of large language models
- Implemented LoRA and adapter methods
- Designed experiments comparing 5 different approaches

## Skills
Python, PyTorch, TensorFlow, C++, Java
Machine Learning, Deep Learning, Natural Language Processing
"""

MOCK_TRANSCRIPT = """Carnegie Mellon University
Unofficial Transcript

Student: Jane Smith
Major: Computer Science
GPA: 3.85/4.0

Fall 2022:
- 10-301 Introduction to Machine Learning: A
- 15-213 Introduction to Computer Systems: A
- 21-241 Matrices and Linear Transformations: A-

Spring 2023:
- 10-315 Introduction to Machine Learning (Advanced): A
- 15-451 Algorithm Design and Analysis: A-
- 10-405 Machine Learning with Large Datasets: A

Fall 2023:
- 10-601 Machine Learning: A
- 10-701 Introduction to Machine Learning (PhD): A
- 15-451 Algorithm Design and Analysis: B+

Spring 2024:
- 10-423 Generative AI: A+
- 10-707 Advanced Deep Learning: A
- 11-785 Introduction to Deep Learning: A
"""

MOCK_ACCOMPLISHMENTS = """# Accomplishments and Contributions

## Teaching Assistant Work

### 10-301 Introduction to Machine Learning (Spring 2023)
- Developed new autograder tests that caught common student errors in homework 3
- Created supplementary tutorial materials for neural networks topic
- Identified and fixed bug in homework 3 starter code affecting 50+ students
- Received 4.7/5.0 rating from students

### 10-601 Machine Learning (Fall 2023)
- Led review session before final exam with 100+ attendees
- Created visualization tool for backpropagation that was adopted for future semesters
- Mentored 2 undergraduate TAs in their first semester
- Ranked #1 out of 20 TAs based on student feedback (4.8/5.0 rating)

## Research Contributions

### Efficient Fine-tuning of Large Language Models
Duration: Summer 2023 - Present
Advisor: Professor Matt Gormley

- Implemented parameter-efficient fine-tuning methods (LoRA, adapters, prefix tuning)
- Designed and executed experiments comparing 5 different approaches
- Analyzed results and identified optimal hyperparameters for each method
- Wrote evaluation pipeline that is now used by the entire research group
- Proposed novel hybrid approach combining benefits of different methods
- Achieved 30% reduction in training time with comparable performance to full fine-tuning

Results:
- Co-author on paper submitted to NeurIPS 2024
- Code released as open-source library with 200+ GitHub stars
- Presented poster at CMU ML lunch seminar

## Additional Activities

- Member of CMU AI Club
- Volunteered as ML tutor for underrepresented minority students
- Organized study groups for 10-601
"""

MOCK_STATEMENT = """# Personal Statement - PhD Application

I am applying for the PhD program in Machine Learning at Stanford University to pursue research in efficient and accessible machine learning systems.

## Research Interests

My primary research interest lies at the intersection of machine learning and systems, specifically:
- Efficient training methods for large language models
- Parameter-efficient fine-tuning techniques
- Making ML more accessible through reduced computational requirements
- Applications of ML to scientific domains

## Career Goals

My long-term goal is to become a research scientist in either industry or academia, focusing on making machine learning more efficient and accessible. I am particularly interested in developing methods that allow researchers with limited computational resources to work with state-of-the-art models.

## Why Stanford

Stanford's machine learning program aligns perfectly with my interests. I am particularly interested in working with Professor [Name]'s group on efficient training methods, and I am excited about the interdisciplinary nature of the program that combines ML with systems research.

## Background and Preparation

Through my undergraduate research at CMU, I have gained hands-on experience with large language models, efficient fine-tuning methods, and experimental design. My work as a teaching assistant has strengthened my communication skills and deepened my understanding of ML fundamentals. I am excited to bring this foundation to Stanford's PhD program and contribute to cutting-edge research in efficient ML systems.
"""

def mock_llm_call(messages, model=None, temperature=None):
    """Mock LLM response for testing."""
    return """# Student Packet: Jane Smith

## Student Profile

- **Name**: Jane Smith
- **Email**: jsmith@cmu.edu
- **Current Status**: Senior, Computer Science, Carnegie Mellon University
- **GPA**: 3.85/4.0
- **Graduation**: May 2024
- **Interaction Period**: Fall 2022 - Present
- **Relationship**: Student in 10-301 and 10-601, Teaching Assistant for 10-301 and 10-601, Research Assistant
- **Letter Type**: PhD Application
- **Target Program**: PhD in Machine Learning, Stanford University

## Academic Performance

**Courses with Professor Gormley:**
- 10-301 Introduction to Machine Learning (Fall 2022): A
- 10-601 Machine Learning (Fall 2023): A
- 10-423 Generative AI (Spring 2024): A+

**Other Relevant Coursework:**
- 15-213 Introduction to Computer Systems (Fall 2022): A
- 15-451 Algorithm Design and Analysis (Spring 2023): A-
- 10-405 Machine Learning with Large Datasets (Spring 2023): A
- 10-701 Introduction to Machine Learning (PhD-level, Fall 2023): A
- 10-707 Advanced Deep Learning (Spring 2024): A
- 11-785 Introduction to Deep Learning (Spring 2024): A

**Academic Standing:**
- Overall GPA: 3.85/4.0
- Consistently strong performance in advanced ML courses
- Taken multiple PhD-level courses as undergraduate

## Teaching Assistant Work

**Courses:** 10-301 Introduction to Machine Learning (Spring 2023), 10-601 Machine Learning (Fall 2023)

**Responsibilities:**
- Office hours (6 hours/week)
- Homework and exam grading
- Leading recitation sections

**Accomplishments from Student:**
- Developed new autograder tests that caught common student errors in homework 3
- Created supplementary tutorial materials for neural networks topic that were adopted for future semesters
- Identified and fixed bug in homework 3 starter code affecting 50+ students
- Led review session before final exam with 100+ attendees
- Created visualization tool for backpropagation that was adopted for future semesters
- Mentored 2 undergraduate TAs in their first semester
- Received 4.7/5.0 rating in Spring 2023, 4.8/5.0 rating in Fall 2023
- Ranked #1 out of 20 TAs in Fall 2023 based on student feedback

## Research Contributions

**Project:** Efficient Fine-tuning of Large Language Models
**Duration:** Summer 2023 - Present
**Role:** Research Assistant
**Advisor:** Professor Matt Gormley

**Accomplishments from Student:**
- Implemented parameter-efficient fine-tuning methods including LoRA, adapters, and prefix tuning
- Designed and executed comprehensive experiments comparing 5 different approaches
- Analyzed results and identified optimal hyperparameters for each method
- Wrote evaluation pipeline that is now used by the entire research group
- Proposed novel hybrid approach combining benefits of different methods
- Achieved 30% reduction in training time with comparable performance to full fine-tuning

**Results:**
- Co-author on paper submitted to NeurIPS 2024
- Code released as open-source library with 200+ GitHub stars
- Presented poster at CMU ML lunch seminar

## Goals and Experience Alignment

**Target Program:** PhD in Machine Learning, Stanford University

**Career Goals:**
- Long-term: Research scientist in industry or academia
- Focus area: Making ML more efficient and accessible
- Interest in developing methods for researchers with limited computational resources

**Research Interests:**
- Efficient training methods for large language models
- Parameter-efficient fine-tuning techniques
- Making ML more accessible through reduced computational requirements
- Applications of ML to scientific domains
- Intersection of ML and systems

**Why Stanford:**
- Alignment with efficient training methods research
- Interest in interdisciplinary approach combining ML with systems
- Specific faculty interest in the program

## Strengths from Professor's Perspective

[TO BE COMPLETED MANUALLY BY PROFESSOR]

This section should include:
- **Overall Assessment**: Ranking or comparison to peer group
- **Key Strengths**: 3-5 main strengths with specific evidence
- **Standout Moments**: Specific anecdotes or observations
- **Comparison to Peers**: How student compares to others in similar roles
- **Growth Trajectory**: Development and improvement observed over time
- **Recommendation Strength**: Explicit calibration (e.g., "Tier 1: Exceptional - highest recommendation without reservation")
- **Additional Context**: Any relevant information not captured in student materials
"""


def create_mock_student_data(temp_dir: Path):
    """Create mock student data files."""
    student_dir = temp_dir / "test_student"
    input_dir = student_dir / "input"
    input_dir.mkdir(parents=True)

    # Create mock files
    (input_dir / "resume.txt").write_text(MOCK_RESUME)
    (input_dir / "transcript.txt").write_text(MOCK_TRANSCRIPT)
    (input_dir / "accomplishments.txt").write_text(MOCK_ACCOMPLISHMENTS)
    (input_dir / "statement.txt").write_text(MOCK_STATEMENT)

    return student_dir


def main():
    """Run the manual test."""
    print("="*60)
    print("Phase 2 Manual Test: Student Packet Synthesis")
    print("="*60)
    print()

    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create mock student data
        print("Creating mock student data...")
        student_dir = create_mock_student_data(temp_path)
        print(f"  Created test data in: {student_dir}")
        print()

        # List files
        print("Mock files created:")
        for file in (student_dir / "input").iterdir():
            print(f"  - {file.name}")
        print()

        # Run synthesis with mocked LLM
        print("Running student packet synthesis (with mocked LLM call)...")
        print()

        with patch('lor.synthesize_packet.call_llm', side_effect=mock_llm_call):
            synthesize_student_packet(student_dir)

        print()
        print("="*60)
        print("Test completed successfully!")
        print("="*60)
        print()

        # Check outputs
        markdown_dir = student_dir / "markdown"
        packet_file = student_dir / "student_packet.md"

        if markdown_dir.exists():
            md_files = list(markdown_dir.glob("*.md"))
            print(f"Converted markdown files ({len(md_files)}):")
            for f in md_files:
                print(f"  - {f.name} ({f.stat().st_size} bytes)")
            print()

        if packet_file.exists():
            print(f"Student packet created: {packet_file.name}")
            print(f"Size: {packet_file.stat().st_size} bytes")
            print()
            print("First 500 characters:")
            print("-" * 60)
            print(packet_file.read_text()[:500])
            print("...")
            print("-" * 60)
        else:
            print("ERROR: Student packet was not created!")

        print()
        print("Next steps:")
        print("1. To run with actual LLM, create student directory:")
        print("   mkdir -p data/students/jane_smith/input")
        print("2. Add student materials to input/ directory")
        print("3. Run: python3 -m lor.cli synthesize-packet data/students/jane_smith/")


if __name__ == "__main__":
    main()
