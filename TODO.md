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
│   │   ├── style_guide.md          # Overall writing style guide
│   │   ├── structure_patterns.md   # Common letter structures
│   │   └── example_excerpts.md     # Anonymized example phrases/paragraphs
│   │
│   └── students/                   # Student-specific folders (PRIVATE)
│       └── [student_name]/
│           ├── input/              # Raw materials from student
│           │   ├── resume.pdf
│           │   ├── transcript.pdf
│           │   ├── accomplishments.txt
│           │   └── personal_statement.pdf
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
   lor redact data/original_letters/ --model gpt-4
   ```
   - Converts .docx → Markdown
   - Replaces [STUDENT_NAME], [STUDENT_ID], [STUDENT_EMAIL], etc.
   - Output: `data/redacted_letters/*.md`

2. **Extract Style Guide**
   ```bash
   lor extract-style data/redacted_letters/ --output data/style_guide/
   ```

   **What this produces:**

   a) **style_guide.md** - Core writing patterns:
      - Sentence structure preferences (e.g., compound vs. simple sentences)
      - Vocabulary level and technical terminology usage
      - Tone (formal, warm, enthusiastic, measured)
      - Common phrases and transitions
      - How you emphasize strengths
      - How you contextualize weaknesses (if at all)

   b) **structure_patterns.md** - Letter organization:
      - Opening paragraph templates
      - Body paragraph organization (chronological, thematic, etc.)
      - How you integrate different types of evidence (grades, TA work, research)
      - Closing paragraph patterns
      - Length guidelines (words per section)

   c) **example_excerpts.md** - Reusable phrases:
      - Opening lines (e.g., "I am writing to enthusiastically recommend...")
      - Transition phrases
      - Ways to describe teaching assistant work
      - Ways to describe research contributions
      - Closing statements
      - All with placeholders for student-specific information

### Key Considerations

- **Multiple passes**: Run style extraction separately for MS vs PhD letters if patterns differ
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
2. **Unofficial Transcript** + grade permission
3. **Accomplishments List** (bulleted, in their words)
4. **Personal Statement** (for program they're applying to)

### Steps

1. **Create Student Folder**
   ```bash
   mkdir -p data/students/jane_smith/input
   # Student uploads files to input/ folder
   ```

2. **Convert Documents to Text**
   ```bash
   lor convert data/students/jane_smith/input/ --output-format markdown
   ```
   - Handles PDF, DOCX → Markdown
   - Preserves structure (headings, lists, etc.)

3. **Synthesize Student Packet (Auto-Generated)**
   ```bash
   lor synthesize-packet data/students/jane_smith/ \
       --courses "10-301, 10-601" \
       --role "Teaching Assistant" \
       --letter-type phd
   ```

   This creates a student packet with auto-populated sections (a-e) from student materials.

4. **Add Professor's Perspective (Manual)**
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

   e) **Program Fit** (from personal statement)
      - Target program and institution
      - Career goals and research interests

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

## Program Fit

**Target Program:** PhD in Machine Learning, Stanford University

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
- **Length**: Aim for 800-1200 words (excluding professor's section) - much shorter than previous version
- **Separation**: Each student packet is completely isolated from others
- **Professor input required**: The "Strengths from Professor's Perspective" section must be written manually by you after reviewing the auto-generated sections

---

## Phase 3: Letter Generation (Per Student, Per Program)

### Goal
Generate a complete letter of recommendation by combining style guide, student packet, and program-specific instructions.

### Steps

1. **Generate Letter Draft**
   ```bash
   lor generate-letter data/students/jane_smith/ \
       --program "PhD, Stanford, Machine Learning" \
       --length 600 \
       --model gpt-4
   ```

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
   - Length: ~600 words (2 pages)
   - Focus areas: Research potential, TA effectiveness, academic strength
   - Tone: Enthusiastic but measured
   - Structure: Opening (relationship), Body (evidence), Closing (recommendation strength)

   Key points to emphasize:
   1. Research contributions and independence
   2. Teaching effectiveness and student impact
   3. Technical depth and breadth

   Output format: Markdown
   ```

2. **Review and Refine**
   ```bash
   # Human reviews letter_draft.md
   # Makes edits as needed
   ```

3. **Convert to DOCX**
   ```bash
   lor convert-to-docx data/students/jane_smith/output/letter_draft.md \
       --template letterhead \
       --output letter_final.docx
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

## Phase 4: Quality Control & Iteration

### Validation Checklist

Before sending any letter, verify:

- [ ] All factual claims are accurate (cross-check with student packet)
- [ ] No hallucinated details (courses, grades, accomplishments)
- [ ] Writing style matches your voice
- [ ] No generic or cliché phrases
- [ ] Appropriate recommendation strength
- [ ] No identifying information from other students
- [ ] Proper formatting and structure
- [ ] Contact information correct
- [ ] Date and addressee correct
- [ ] Letter is program-appropriate

### Iterative Refinement

If letter quality is unsatisfactory:

1. **First iteration**: Edit specific sections manually
2. **Second iteration**: Regenerate with more specific instructions
   ```bash
   lor generate-letter data/students/jane_smith/ \
       --program "PhD, Stanford, Machine Learning" \
       --focus "research,independence,technical_depth" \
       --avoid "generic_phrases" \
       --regenerate "body_paragraph_3"
   ```
3. **Style guide update**: If systematic issues, update style guide and regenerate

### Feedback Loop

After each letter generation:
- Note what worked well / what didn't
- Update prompts or style guide if patterns emerge
- Track time savings vs manual writing
- Collect any new example phrases for style guide

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

---

## Implementation Roadmap

### Milestone 1: Setup & Redaction ✓
- [x] Poetry project structure
- [x] CLI framework with Click
- [x] Redaction subcommand working
- [ ] Collect 10-20 historical letters (diverse: MS, PhD, TA, research)
- [ ] Redact all historical letters

### Milestone 2: Style Extraction
- [ ] Create `lor extract-style` subcommand
- [ ] Implement style guide generation prompt
- [ ] Implement structure pattern extraction
- [ ] Implement example excerpt extraction
- [ ] Generate initial style guide
- [ ] Manual review and refinement

### Milestone 3: Student Packet Synthesis
- [ ] Create `lor convert` subcommand (PDF/DOCX → Markdown)
- [ ] Create `lor synthesize-packet` subcommand
- [ ] Design student packet template
- [ ] Implement synthesis prompt

### Milestone 4: Letter Generation
- [ ] Create `lor generate-letter` subcommand
- [ ] Design letter generation prompt
- [ ] Implement context assembly (style + packet + instructions)

### Milestone 5: Conversion & Formatting
- [ ] Create `lor convert-to-docx` subcommand
- [ ] Implement Markdown → DOCX conversion with formatting
- [ ] Create letterhead template

### Milestone 6: End-to-End Testing
- [ ] Test with 2-3 real student datasets (anonymized)
- [ ] Generate 2-3 test letters
- [ ] Compare generated letters with hand-written letters
- [ ] Refine packet structure based on testing results
- [ ] Iterate on prompts and style guide
- [ ] Test output formatting
- [ ] Validate full workflow

### Milestone 7: Production Use
- [ ] Create end-to-end documentation
- [ ] Generate first production letter
- [ ] Establish feedback/improvement process
- [ ] Document time savings and quality metrics

---

## Example Commands (Full Workflow)

```bash
# One-time setup: Extract your writing style
lor redact data/original_letters/ --output data/redacted_letters/
lor extract-style data/redacted_letters/ --output data/style_guide/

# Per student: Generate a letter
# 1. Student provides materials → data/students/jane_smith/input/

# 2. Convert to markdown
lor convert data/students/jane_smith/input/

# 3. Auto-generate student packet
lor synthesize-packet data/students/jane_smith/ \
    --courses "10-301, 10-601" \
    --role "TA, Research Assistant" \
    --letter-type phd

# 4. MANUAL: Edit data/students/jane_smith/student_packet.md
#    Add "Strengths from Professor's Perspective" section

# 5. Generate letter
lor generate-letter data/students/jane_smith/ \
    --program "PhD, Stanford, Machine Learning" \
    --length 600

# 6. Review data/students/jane_smith/output/letter_draft.md
#    Make any edits needed

# 7. Convert to DOCX
lor convert-to-docx data/students/jane_smith/output/letter_draft.md

# 8. Final review and send letter_final.docx
```

---

## Estimated Time Savings

### Traditional Process (Manual)
- Initial draft: 60-90 minutes
- Revision: 15-30 minutes
- **Total: 75-120 minutes per letter**

### LLM-Assisted Process
- Setup (per student): 5 minutes (organize files)
- Synthesis: 2 minutes (automated)
- Generation: 2 minutes (automated)
- Review & editing: 15-30 minutes
- **Total: 25-40 minutes per letter**

**Time savings: 50-80 minutes per letter (60-70% reduction)**

With 20 letters per year: **16-26 hours saved annually**

---

## Success Metrics

Track these metrics over first 10 letters:

1. **Time per letter** (setup + review + editing)
2. **Edit distance** (how much manual editing required)
3. **Factual errors** (hallucinations caught in review)
4. **Style consistency** (subjective 1-5 rating)
5. **Recipient feedback** (if available)
6. **Reuse of style guide** (needed updates or stable)

Target goals after refinement:
- < 30 minutes per letter
- < 20% of content manually edited
- Zero factual errors
- 4/5+ style consistency
- Style guide stable (no major updates needed)

---

## Next Steps

1. Collect and redact 10-20 historical letters
2. Implement `extract-style` subcommand
3. Test style extraction on redacted letters
4. Review and manually refine generated style guide
5. Implement `synthesize-packet` subcommand
6. Test with 1-2 real student datasets
7. Implement `generate-letter` subcommand
8. Generate and review first test letter
9. Iterate based on results
10. Document any additional refinements needed
