# Letter of Recommendation Generation System

A comprehensive system for generating personalized letters of recommendation using LLMs while maintaining strict separation between student data and capturing your authentic writing style.

The system consists of three phases:
1. **Phase 1: Style Extraction** - Extract your writing style from historical letters (one-time setup)
2. **Phase 2: Student Packet Synthesis** - Consolidate student materials into structured documents (per student)
3. **Phase 3: Letter Generation** - Generate personalized letters combining style and student data (per student, per program)

## Quick Start - Phase 1

Phase 1 is a one-time setup to extract your writing style from historical letters:

```bash
# 1. Place your original .docx letters in data/original_letters/
# 2. Redact student information
python3 -m lor.cli redact data/original_letters/

# 3. Extract your writing style
python3 -m lor.cli extract-style data/redacted_letters/

# 4. Review and edit data/style_guide/style_guide.md
```

**Note**: If you don't have an API key set up, see the [Installation](#installation) section below. You can test without an API key using the mock test: `python3 test_phase1_manual.py`

## Quick Start - Phase 2

Phase 2 creates a structured student packet from application materials (done per student):

```bash
# 1. Create student directory and add their materials
mkdir -p data/students/jane_smith/input
# Place resume.pdf, transcript.pdf, accomplishments.txt, statement.pdf in input/

# 2. Copy professor notes template and fill it in
cp templates/professor_notes.md data/students/jane_smith/input/professor_notes.md
# Edit professor_notes.md with your observations, assessment, and contextual information

# 3. Synthesize student packet
python3 -m lor.cli synthesize-packet data/students/jane_smith/

# 4. Review data/students/jane_smith/student_packet.md
```

**Note**: Test without API key: `python3 test_phase2_manual.py`

## Quick Start - Phase 3

Phase 3 generates the actual letter by combining style guide and student packet (done per student):

```bash
# 1. Ensure student packet is complete and accurate
# 2. Generate letter
python3 -m lor.cli generate-letter data/students/jane_smith/

# 3. Review data/students/jane_smith/output/letter_draft.md and letter_draft.docx
# 4. Edit as needed and send!
```

## Note: Single command for Phase 2 and Phase 3

You can run both Phase 2's packet creation and Phase 3's letter generation with a single command:

```bash
python3 -m lor.cli packet-and-letter data/students/jane_smith/
```

**Note**: Test without API key: `python3 test_phase3_manual.py`

## Features

### Phase 1: Style Extraction
- **Redaction**: Automatically redacts student-identifying information from Word documents
- **Style Analysis**: Uses LLM to extract writing patterns, structure, and voice from redacted letters
- **Privacy-Focused**: Ensures no student information contaminates the style guide
- **Comprehensive Style Guide**: Captures sentence structure, vocabulary, tone, common phrases, and letter organization

### Phase 2: Student Packet Synthesis
- **Multi-Format Support**: Converts PDF, DOCX, TXT, MD files to markdown
- **Professor Notes Template**: Provides structured template for professor's observations and assessment
- **Intelligent Extraction**: Uses LLM to extract and organize information from student materials and professor notes
- **Structured Output**: Creates organized packet with sections for academics, TA work, research, goals, and professor's perspective
- **Privacy Separation**: Each student packet is isolated (never mixed with other students)
- **Complete Integration**: Professor's assessment integrated during synthesis (no manual post-processing needed)

### Phase 3: Letter Generation
- **Style-Guided Generation**: Combines style guide with student packet to create authentic letters
- **Anti-Hallucination**: Explicit instructions prevent LLM from inventing details
- **Multiple Formats**: Generates markdown and automatically converts to DOCX
- **Customizable**: Options for custom output filenames and style guides
- **Complete Workflow**: Ready-to-send letters combining professor's voice with accurate student information

### Document Processing
- Processes single `.docx` files or recursively scans directories
- Converts Word documents to clean Markdown format
- Uses LLM for intelligent analysis and redaction
- Replaces student information with standardized placeholders:
  - `[STUDENT_NAME]` - Student names
  - `[STUDENT_ID]` - Student ID numbers
  - `[STUDENT_EMAIL]` - Student email addresses
  - `[STUDENT_INFO]` - Other personal identifiers
- Preserves document structure and formatting
- Comprehensive error handling and logging

## Installation

### Prerequisites
- Python 3.7 or higher
- [Poetry](https://python-poetry.org/docs/#installation) (recommended) or pip

### Using Poetry 

1. Clone or download this repository

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Set up your OpenAI API key:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Get your API key from: https://platform.openai.com/api-keys
```

### View Available Commands
```bash
python3 -m lor.cli --help
python3 -m lor.cli redact --help
python3 -m lor.cli extract-style --help
python3 -m lor.cli synthesize-packet --help
python3 -m lor.cli generate-letter --help
```
