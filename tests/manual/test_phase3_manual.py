#!/usr/bin/env python3
"""
Manual test script for Phase 3 letter generation.
This script creates a complete mock scenario and tests the letter generation pipeline.
"""

from pathlib import Path
from unittest.mock import patch
from lor.generate_letter import generate_letter
import tempfile
import shutil


MOCK_STUDENT_PACKET = """# Student Packet: Jane Smith

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

## Strengths from Professor's Perspective

**Overall Assessment:**
Jane is among the top 5% of students I have worked with and is ready for PhD-level research.

**Key Strengths:**
- Exceptional TA: Ranked #1 out of 20 TAs in Fall 2023 based on student feedback (4.8/5.0 rating). Her Socratic teaching style helps students discover solutions rather than just giving answers.
- Research trajectory: Clear progression from guided work to independent research. Now operates at early graduate student level - comes to meetings with completed work and thoughtful proposals.
- Technical depth: Strong implementation skills combined with solid theoretical foundations. Comfortable with complex systems (distributed training, large models).

**Standout Moments:**
- During one office hours session, spent 90 minutes patiently helping a struggling student understand backpropagation using hand-drawn diagrams. The student later wrote to say this was the first time the concept truly "clicked."
- When our research server crashed, Jane independently debugged the distributed training code and identified a subtle error in the data preprocessing that none of us had caught.

**Comparison to Peers:**
- Top 3 of 10 PhD applicants I have strongly recommended in past 5 years
- Comparable to successful students now thriving in PhD programs at Stanford and MIT
- Research productivity already at level of strong 2nd-year PhD student

**Recommendation Strength:** Tier 1 (Exceptional - highest recommendation without reservation)
"""

MOCK_LETTER = """__Machine Learning Department__

School of Computer Science

Carnegie Mellon University

5000 Forbes Ave, Pittsburgh, PA 15213

__Matthew R. Gormley__

Associate Teaching Professor

Phone: 412-268-7205

Email: mgormley@cs.cmu.edu

November 27, 2025

Dear Members of the Admissions Committee:

I am writing to express my enthusiastic support for Jane Smith's application to your PhD program in Machine Learning at Stanford University. Jane is currently working towards her Bachelor of Science in Computer Science at Carnegie Mellon University (CMU), with an exceptional GPA of 3.85/4.0 and an expected graduation date of May 2024. I have known Jane since Fall 2022, when she took my course 10-301 Introduction to Machine Learning, and she subsequently served as a teaching assistant (TA) for both 10-301 and 10-601 Machine Learning. Since Summer 2023, Jane has also been working with me as a research assistant on efficient fine-tuning of large language models. She has my strongest recommendation.

Jane's academic performance has been consistently outstanding. In my courses, she earned an A in 10-301 Introduction to Machine Learning (Fall 2022), an A in 10-601 Machine Learning (Fall 2023), and an A+ in 10-423 Generative AI (Spring 2024). Beyond my courses, Jane has taken an impressive courseload, including PhD-level courses such as 10-701 Introduction to Machine Learning and 10-707 Advanced Deep Learning, both of which she completed with A grades. Compared to other undergraduate students in the School of Computer Science at CMU, Jane ranks among the top 5%. Her technical abilities are among the best students I have personally advised, and her research potential is very high.

As a teaching assistant for 10-301 (Spring 2023) and 10-601 (Fall 2023), Jane is one of the most accomplished TAs I have worked with. She consistently went above and beyond her assigned responsibilities, developing new autograder tests that caught common student errors and creating supplementary tutorial materials for neural networks that were adopted for future semesters. Jane also identified and fixed a bug in homework 3 starter code affecting 50+ students, demonstrating both her technical acumen and her commitment to student success. Her teaching effectiveness is evidenced by her student feedback ratings: 4.7/5.0 in Spring 2023 and 4.8/5.0 in Fall 2023, ranking her #1 out of 20 TAs based on student feedback in Fall 2023. During one office hours session, I observed Jane spend 90 minutes patiently helping a struggling student understand backpropagation using hand-drawn diagrams. The student later wrote to say this was the first time the concept truly "clicked." Her Socratic teaching style helps students discover solutions rather than just giving answers.

Since Summer 2023, Jane has been working on a project focused on efficient fine-tuning of large language models. Jane implemented parameter-efficient fine-tuning methods including LoRA, adapters, and prefix tuning, and designed and executed comprehensive experiments comparing five different approaches. She wrote an evaluation pipeline that is now used by the entire research group. Jane's idea was to propose a novel hybrid approach combining benefits of different methods. Our initial results are extremely promising, achieving a 30% reduction in training time with comparable performance to full fine-tuning. Jane prototyped the idea very quickly and was able to demonstrate its promise. Her work has resulted in a co-authored paper submitted to NeurIPS 2024 and code released as an open-source library with 200+ GitHub stars. Jane is clearly on a rapidly rising trajectory. She now operates at an early graduate student level - she comes to meetings with completed work and thoughtful proposals. When our research server crashed, Jane independently debugged the distributed training code and identified a subtle error in the data preprocessing that none of us had caught.

In summary, Jane has the makings of a strong machine learning researcher. She is among the top 3 of 10 PhD applicants I have strongly recommended in the past 5 years, comparable to successful students now thriving in PhD programs at Stanford and MIT. Her research productivity is already at the level of a strong 2nd-year PhD student. She has my strongest recommendation. If I can be of further assistance, please feel free to contact me.

Sincerely,

Matthew R. Gormley

Associate Teaching Professor

Machine Learning Department

School of Computer Science

Carnegie Mellon University
"""


def mock_llm_call(messages, model=None, temperature=None):
    """Mock LLM response for testing."""
    return MOCK_LETTER


def create_mock_scenario(temp_dir: Path):
    """Create mock student data and style guide."""
    # Create student directory
    student_dir = temp_dir / "test_student"
    student_dir.mkdir()

    # Create student packet
    (student_dir / "student_packet.md").write_text(MOCK_STUDENT_PACKET)

    # Create mock style guide
    style_guide_path = temp_dir / "style_guide.md"
    style_guide_path.write_text("# Mock Style Guide\n\nThis is a simplified style guide for testing.")

    return student_dir, style_guide_path


def main():
    """Run the manual test."""
    print("="*60)
    print("Phase 3 Manual Test: Letter Generation")
    print("="*60)
    print()

    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create mock scenario
        print("Creating mock scenario...")
        student_dir, style_guide_path = create_mock_scenario(temp_path)
        print(f"  Student directory: {student_dir}")
        print(f"  Style guide: {style_guide_path}")
        print()

        # Run letter generation with mocked LLM
        print("Running letter generation (with mocked LLM call)...")
        print()

        with patch('lor.generate_letter.call_llm', side_effect=mock_llm_call):
            letter_path = generate_letter(
                student_dir,
                style_guide_path=style_guide_path
            )

        print()
        print("="*60)
        print("Test completed successfully!")
        print("="*60)
        print()

        # Check outputs
        if letter_path.exists():
            print(f"Letter created: {letter_path.name}")
            print(f"Size: {letter_path.stat().st_size} bytes")
            content = letter_path.read_text()
            word_count = len(content.split())
            print(f"Word count: {word_count} words")
            print()
            print("First 600 characters:")
            print("-" * 60)
            print(content[:600])
            print("...")
            print("-" * 60)
        else:
            print("ERROR: Letter was not created!")

        print()
        print("Next steps:")
        print("1. To test with real data:")
        print("   - Ensure Phase 1 complete (style guide exists)")
        print("   - Ensure Phase 2 complete (student packet exists)")
        print("   - Complete 'Strengths from Professor's Perspective' section")
        print("2. Run: python3 -m lor.cli generate-letter data/students/jane_smith/")
        print("3. Add --docx flag to also generate DOCX format")


if __name__ == "__main__":
    main()
