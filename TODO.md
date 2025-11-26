# Letter of Recommendation Generation System - Implementation Plan

## Overview

This system uses LLMs to generate personalized letters of recommendation in your writing style while maintaining strict separation between student data and avoiding common pitfalls like hallucination and context length issues.

## System Architecture

### Folder Structure

```
letter_of_rec/
├── cli.py                          # Main CLI tool
├── pyproject.toml                  # Poetry dependencies
├── .env                            # API keys
├── TODO.md                         # This file
│
├── data/
│   ├── original_letters/           # Original .docx letters (PRIVATE)
│   ├── redacted_letters/           # Redacted .md letters (for style analysis)
│   ├── style_guide/                # Generated style documentation
│   │   └── style_guide.md          # Overall writing style guide
│   │
│   └── students/                   # Student-specific folders (PRIVATE)
│       └── [student_name]/
│           ├── input/              # Raw materials from student
│           │   ├── resume.pdf
│           │   ├── transcript.pdf
│           │   ├── accomplishments.txt
│           │   └── personal_statement.pdf
|           ├── markdown/           # input/ files converted to markdown
│           ├── student_packet.md   # Synthesized student information
│           └── output/
│               ├── letter_draft.md
│               └── letter_final.docx
│
├── prompts/                        # LLM prompt templates
│   ├── extract_style_guide.md      # Prompt for style extraction
│   ├── synthesize_student_packet.md # Prompt for student packet creation
│   └── generate_letter.md          # Prompt for letter generation
│
└── examples/                       # Example files (for documentation)
    ├── style_guide_example.md
    ├── student_packet_example.md
    └── letter_draft_example.md
```

## Workflow Phases

---

## Phase 1: Style Extraction (One-Time Setup)

### Goal
Extract your writing style from historical letters without cross-contaminating student information.

### Steps

1. **Redact Historical Letters**
   ```bash
   lor redact data/original_letters/ 
   ```
   - Converts .docx → Markdown
   - Replaces [STUDENT_NAME], [STUDENT_ID], [STUDENT_EMAIL], etc.
   - Output: `data/redacted_letters/*.md`

2. **Extract Style Guide**
   ```bash
   lor extract-style data/redacted_letters/ --output data/style_guide/
   ```

   **What this produces:**

   a) **Style Guide** - Core writing patterns:
      - Sentence structure preferences (e.g., compound vs. simple sentences)
      - Vocabulary level and technical terminology usage
      - Tone (formal, warm, enthusiastic, measured)
      - Common phrases and transitions
      - How you emphasize strengths
      - How you contextualize weaknesses (if at all)

   b) **Structure Patterns** - Letter organization:
      - Opening paragraph templates
      - Body paragraph organization (chronological, thematic, etc.)
      - How you integrate different types of evidence (grades, TA work, research)
      - Closing paragraph patterns
      - Length guidelines (words per section)

   c) **Example Excerpts** - Reusable phrases:
      - Opening lines (e.g., "I am writing to enthusiastically recommend...")
      - Transition phrases
      - Ways to describe teaching assistant work
      - Ways to describe research contributions
      - Closing statements
      - All with placeholders for student-specific information

### Key Considerations

- **Version control**: Keep style guide in git to track refinements
- **Manual review**: Review and edit the generated style guide to ensure accuracy
- **Privacy**: Redacted letters should have NO identifying information

---

## Phase 2: Student Packet Synthesis (Per Student)

### Goal
Consolidate all student materials into a single, structured Markdown document that's optimized for LLM consumption.

### Input Requirements from Students

Students provide:
1. **Resume** (PDF/DOCX)
2. **Unofficial Transcript**
3. **Accomplishments List** (bulleted, in their words)
4. **Personal Statement** (for program they're applying to)

### Steps

1. **Create Student Folder**
   ```bash
   mkdir -p data/students/jane_smith/input
   # Student uploads files to input/ folder
   ```
2. **Synthesize Student Packet (Auto-Generated)**
   ```bash
   lor synthesize-packet data/students/jane_smith/ 
   ```
   - Handles PDF, DOCX → Markdown
   - Preserves structure (headings, lists, etc.)
   - This creates a student packet with auto-populated sections (a-e) from student materials.

3. **Add Professor's Perspective (Manual)**
   - Open `data/students/jane_smith/student_packet.md`
   - Review auto-generated sections
   - Write the "Strengths from Professor's Perspective" section
   - Include: your observations, comparisons, anecdotes, recommendation strength

   **The complete student packet includes:**

   a) **Student Profile** (structured metadata)
      - Name, email, current status
      - GPA, major, graduation date
      - Courses taken with you + grades (if permitted)
      - Role(s): TA, research assistant, etc.
      - Time period of interaction

   b) **Academic Performance** (extracted from transcript)
      - Relevant coursework with grades
      - Overall academic standing

   c) **Teaching Assistant Work** (from accomplishments)
      - Specific courses and semesters
      - Notable contributions from student's list
      - Responsibilities

   d) **Research Contributions** (from accomplishments)
      - Project descriptions
      - Technical contributions
      - Results (papers, code, etc.)

   e) **Match of Goals and Experience** (from personal statement)
      - Career goals and research / teaching interests

   f) **Strengths from Professor's Perspective** (manually written by you)
      - Your personal observations and assessments
      - Comparison to other students
      - Specific anecdotes or standout moments
      - Growth trajectory you've observed
      - Recommendation strength calibration
      - Any additional context not captured in student materials

### Example Student Packet Structure

```markdown
# Student Packet: [STUDENT_NAME]

## Metadata
- **Name**: Jane Smith
- **Email**: jsmith@university.edu
- **Current Status**: Senior, Computer Science
- **GPA**: 3.85/4.0
- **Graduation**: May 2024
- **Interaction Period**: Fall 2022 - Spring 2024
- **Relationship**: Teaching Assistant (10-301, 10-601), Research Assistant
- **Letter Type**: PhD Application
- **Target Program**: PhD in Machine Learning, Stanford University

## Academic Performance

**Courses with Professor Gormley:**
- 10-301 Introduction to Machine Learning (Fall 2022): A
- 10-601 Machine Learning (Fall 2023): A
- 10-423 Generative AI (Spring 2024): A+

**Other Relevant Coursework:**
- 15-213 Introduction to Computer Systems: A
- 15-451 Algorithm Design and Analysis: A-
- 10-405 Machine Learning with Large Datasets: A

**Academic Standing:**
- Overall GPA: 3.85/4.0
- Major GPA: 3.90/4.0

## Teaching Assistant Work

**Courses:** 10-301 (Spring 2023), 10-601 (Fall 2023)

**Responsibilities:**
- Office hours (6 hrs/week)
- Homework and exam grading
- Recitation sections

**Accomplishments from Student:**
- Developed new autograder tests that caught common student errors
- Created supplementary tutorial materials for neural networks topic
- Identified and fixed bug in homework 3 starter code affecting 50+ students
- Led review session before final exam with 100+ attendees
- Created visualization tool for backpropagation that was adopted for future semesters
- Mentored 2 undergraduate TAs in their first semester

## Research Contributions

**Project:** Efficient Fine-tuning of Large Language Models
**Duration:** Summer 2023 - Present

**Accomplishments from Student:**
- Implemented parameter-efficient fine-tuning methods (LoRA, adapters)
- Designed and executed experiments comparing 5 approaches
- Analyzed results and identified optimal hyperparameters
- Wrote evaluation pipeline used by entire research group
- Proposed novel hybrid approach combining benefits of different methods
- Achieved 30% reduction in training time with comparable performance

**Results:**
- Co-author on paper submitted to NeurIPS 2024
- Code released as open-source library with 200+ GitHub stars

## Match of Goals and Experience

**Target Program:** PhD in Machine Learning

**Career Goals:** (from personal statement)
- Research scientist in industry or academia
- Focus on making ML more accessible and efficient

**Research Interests:** (from personal statement)
- Efficient training methods for large models
- Applications of ML to scientific domains
- Intersection of ML and systems

## Strengths from Professor's Perspective

[This section is manually written by Professor Gormley]

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
```

### Key Considerations for Student Packets

- **Factual accuracy**: All information from student materials must be verifiable from source documents
- **No hallucination**: If information isn't in source materials, mark as [TO_VERIFY] or omit
- **Structured format**: Use consistent headings for easy extraction during letter generation
- **Specificity**: Include concrete examples from student's accomplishments list
- **Length**: Aim for 800 words (excluding professor's section)
- **Separation**: Each student packet is completely isolated from others
- **Professor input required**: The "Strengths from Professor's Perspective" section must be written manually by you after reviewing the auto-generated sections

---

## Phase 3: Letter Generation (Per Student, Per Program)

### Goal
Generate a complete letter of recommendation by combining style guide, student packet, and program-specific instructions.

### Steps

**Generate Letter Draft**
```bash
lor generate-letter data/students/jane_smith/ 
```
- Output as Markdown
- Then convert to docx

**LLM Context Structure** (optimized for token efficiency):

```
[SYSTEM PROMPT]
You are writing a letter of recommendation on behalf of Professor Matt Gormley.
Write in his style, using the style guide and examples provided.

[STYLE GUIDE] (2000 tokens)
[Include key sections from style_guide.md and structure_patterns.md]

[EXAMPLE EXCERPTS] (1000 tokens)
[Select relevant examples from example_excerpts.md]

[STUDENT PACKET] (3000 tokens)
[Full student_packet.md]

[INSTRUCTIONS] (500 tokens)
Write a letter of recommendation for [STUDENT_NAME] applying to:
- Program: PhD in Machine Learning
- Institution: Stanford University

Letter requirements:
- Length: ~500 words (1.5 pages)
- Focus areas: Research potential, TA effectiveness, academic strength
- Tone: Enthusiastic but measured
- Structure: Opening (relationship), Body (evidence), Closing (recommendation strength)

Key points to emphasize:
1. Research contributions and independence
2. Teaching effectiveness and student impact
3. Technical depth and breadth

Output format: Markdown
```

### Letter Structure Template

Based on typical academic rec letters:

```markdown
# Letter of Recommendation for [STUDENT_NAME]

[Letterhead: Professor Matt Gormley, Carnegie Mellon University]

[Date]

Dear Members of the Admissions Committee,

## Opening Paragraph (100 words)
- State purpose: recommending [STUDENT] for [PROGRAM] at [INSTITUTION]
- Establish relationship: how you know the student, how long, in what capacity
- Headline statement: overall assessment (e.g., "one of the strongest students I've worked with")

## Body Paragraph 1: Academic Performance (150 words)
- Courses taken, grades received
- Academic standing relative to peers
- Intellectual qualities demonstrated in coursework
- Specific examples: outstanding homework, insightful questions, exam performance

## Body Paragraph 2: Teaching Assistant Work (150 words)
- Scope and responsibilities
- Effectiveness and impact on students
- Specific contributions or innovations
- Comparison to other TAs
- Evidence: student feedback, your observations, concrete examples

## Body Paragraph 3: Research Experience (150 words)
- Project overview and student's role
- Technical contributions and skills demonstrated
- Level of independence and initiative
- Results and impact (papers, code, insights)
- Trajectory: growth over time

## Closing Paragraph (50 words)
- Summary: strongest attributes
- Explicit recommendation strength (e.g., "highest recommendation without reservation")
- Offer for follow-up questions
- Contact information

Sincerely,

Professor Matt Gormley
[Title, Department, Institution]
[Email, Phone]
```

### Key Considerations for Letter Generation

- **Consistent voice**: Every sentence should sound like you wrote it
- **Evidence-based**: All claims must be supported by information in student packet
- **No generic phrases**: Avoid "hard-working," "team player" without specific examples
- **Appropriate strength**: Match recommendation strength to student's actual qualifications
- **Program-specific**: Tailor emphasis to PhD vs MS, research vs industry programs
- **Length discipline**: Stay within typical bounds (500-700 words)
- **Proofread carefully**: LLMs can generate grammatical errors or awkward phrasings

---

## Anti-Patterns & Pitfalls to Avoid

### 1. Context Length Explosion
**Problem**: Feeding entire history of letters + all student materials
**Solution**:
- Use only redacted letters for style extraction
- Synthesize student materials into focused packet (2000-3000 words)
- Include only relevant style guide excerpts (not entire guide)
- Total context: ~7000 tokens, well within limits

### 2. Information Cross-Contamination
**Problem**: LLM conflates details from different students
**Solution**:
- Complete isolation: one student packet per conversation
- Clear conversation boundaries (new chat per letter)
- Explicit instruction: "Write only about [STUDENT_NAME] using only the information provided"
- Validation: cross-check generated letter against packet

### 3. Hallucination / Fabrication
**Problem**: LLM invents accomplishments, grades, or experiences
**Solution**:
- Explicit instruction: "Do not invent any details. Use only information from student packet."
- Structured packet format makes fact-checking easier
- Include [TO_VERIFY] markers in packet for uncertain information
- Human review focuses on factual accuracy first

### 4. Generic/Robotic Writing
**Problem**: Letter sounds AI-generated or template-filled
**Solution**:
- High-quality style guide with specific examples
- Include your unique phrases and vocabulary
- Iterate on prompts to emphasize "write in Professor Gormley's distinctive style"
- Manual editing of final output for voice consistency
- Consider few-shot examples in prompt

### 5. Style Drift Over Time
**Problem**: Generated letters gradually diverge from your authentic voice
**Solution**:
- Periodic review of style guide against your recent manual letters
- Version control for style guide
- A/B comparison: generated vs hand-written letters
- Update style guide with new patterns or preferences

### 6. Inappropriate Recommendation Strength
**Problem**: LLM is too enthusiastic or too tepid
**Solution**:
- Explicit calibration in student packet: "Comparison to peers: Top 10%"
- Instruction: "Recommendation strength: Strong (not highest tier)"
- Style guide includes examples at different strength levels
- Manual review of closing paragraph particularly carefully

### 7. Program Mismatch
**Problem**: PhD letter sent for MS application (or vice versa)
**Solution**:
- Explicit letter-type parameter in command
- Different emphasis in prompts (research vs coursework)
- Validation checklist includes program type
- Separate style examples for MS vs PhD letters

### 8. Security & Privacy Leaks
**Problem**: Student data exposed or mixed
**Solution**:
- Local processing only (no data sent to third parties beyond OpenAI API)
- Separate folders per student, never merged
- .gitignore includes data/students/ and data/original_letters/
- Regular cleanup of old student data
- Explicit instructions to students about data handling

