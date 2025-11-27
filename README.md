# Letter of Recommendation Generation System

A comprehensive system for generating personalized letters of recommendation using LLMs while maintaining strict separation between student data and capturing your authentic writing style.

The system consists of three phases:
1. **Phase 1: Style Extraction** - Extract your writing style from historical letters (one-time setup)
2. **Phase 2: Student Packet Synthesis** - Consolidate student materials into structured documents (per student)
3. **Phase 3: Letter Generation** - Generate personalized letters combining style and student data (per student, per program)

Current Status: **Phases 1 & 2 Complete**

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

# 2. Synthesize student packet
python3 -m lor.cli synthesize-packet data/students/jane_smith/

# 3. Review data/students/jane_smith/student_packet.md
# 4. Add "Strengths from Professor's Perspective" section
```

**Note**: Test without API key: `python3 test_phase2_manual.py`

## Features

### Phase 1: Style Extraction
- **Redaction**: Automatically redacts student-identifying information from Word documents
- **Style Analysis**: Uses LLM to extract writing patterns, structure, and voice from redacted letters
- **Privacy-Focused**: Ensures no student information contaminates the style guide
- **Comprehensive Style Guide**: Captures sentence structure, vocabulary, tone, common phrases, and letter organization

### Phase 2: Student Packet Synthesis
- **Multi-Format Support**: Converts PDF, DOCX, TXT files to markdown
- **Intelligent Extraction**: Uses LLM to extract and organize information from student materials
- **Structured Output**: Creates organized packet with sections for academics, TA work, research, goals
- **Privacy Separation**: Each student packet is isolated (never mixed with other students)
- **Professor Input**: Includes placeholder for professor's unique perspective and assessment

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

### Using Poetry (Recommended)

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

### Using pip (Alternative)

If you prefer not to use Poetry:

1. Clone or download this repository

2. Install dependencies:
```bash
pip install python-docx mammoth openai python-dotenv click
```

3. Set up your OpenAI API key (same as above)

## Usage

This tool provides two interfaces:
1. **CLI tool** (`lor` command) - Recommended, supports multiple subcommands
2. **Standalone script** (`redact_student_info.py`) - Direct script execution

### CLI Usage (Recommended)

The `lor` command provides multiple subcommands for different phases:

#### Phase 1: Style Extraction (One-Time Setup)

**Step 1: Redact historical letters**
```bash
# Redact student information from original letters
python3 -m lor.cli redact data/original_letters/

# Output: data/redacted_letters/*.md
```

**Step 2: Extract writing style**
```bash
# Extract style guide from redacted letters
python3 -m lor.cli extract-style data/redacted_letters/

# Output: data/style_guide/style_guide.md
```

**Step 3: Review and refine**
- Open `data/style_guide/style_guide.md`
- Review the extracted style patterns
- Edit to ensure accuracy and completeness
- Keep in version control for future refinements

#### Phase 2: Student Packet Synthesis (Per Student)

**Step 1: Organize student materials**
```bash
# Create student directory
mkdir -p data/students/jane_smith/input

# Student provides these files (any of .pdf, .docx, .txt):
# - resume.pdf or cv.pdf
# - transcript.pdf
# - accomplishments.txt or achievements.txt
# - statement.pdf or personal_statement.pdf
```

**Step 2: Synthesize packet**
```bash
# Auto-generate student packet from materials
python3 -m lor.cli synthesize-packet data/students/jane_smith/

# Output: data/students/jane_smith/student_packet.md
# Also creates: data/students/jane_smith/markdown/ (converted files)
```

**Step 3: Add professor's perspective**
- Open `data/students/jane_smith/student_packet.md`
- Review auto-generated sections for accuracy
- Complete the "Strengths from Professor's Perspective" section:
  - Overall assessment and ranking
  - Key strengths with specific evidence
  - Standout moments and anecdotes
  - Comparison to peers
  - Growth trajectory
  - Recommendation strength calibration

#### View Available Commands
```bash
python3 -m lor.cli --help
python3 -m lor.cli redact --help
python3 -m lor.cli extract-style --help
python3 -m lor.cli synthesize-packet --help
```

### Standalone Script Usage

You can also run the script directly:

```bash
# Process a single file
python redact_student_info.py letter.docx

# Process a directory
python redact_student_info.py ./letters/

# With options
python redact_student_info.py ./letters/ --model gpt-4-turbo --dry-run
```

## How It Works

1. **File Discovery**: Finds all `.docx` files in the specified path (skips temporary files like `~$filename.docx`)

2. **Conversion**: Converts each Word document to Markdown format using the `mammoth` library

3. **Redaction**: Sends the Markdown to OpenAI's API with specific instructions to identify and replace student information with placeholders

4. **Output**: Saves the redacted content as a `.md` file with the same name as the original document

## Output

For each input file `document.docx`, the script creates `document.md` in the same directory containing the redacted content.

Example:
```
letters/
├── recommendation_john_doe.docx
├── recommendation_john_doe.md    # ← Generated (redacted)
├── recommendation_jane_smith.docx
└── recommendation_jane_smith.md  # ← Generated (redacted)
```

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies (managed by Poetry or installed manually):
  - `python-docx` - Reading Word documents
  - `mammoth` - Converting Word to Markdown
  - `openai` - OpenAI API client
  - `python-dotenv` - Environment variable management
  - `click` - CLI framework

## Security Notes

- Your OpenAI API key should be kept confidential
- The `.env` file is gitignored by default (add it to `.gitignore` if not already present)
- Redacted documents should be reviewed before sharing to ensure complete redaction
- Original `.docx` files are never modified by this script

## Troubleshooting

**Error: "OpenAI API key not found"**
- Ensure you've created a `.env` file with your API key, or pass it via `--api-key`

**Error: "No .docx files found"**
- Check that the path is correct and contains `.docx` files
- Ensure files don't start with `~$` (temporary files)

**Conversion warnings**
- Some complex Word formatting may not convert perfectly to Markdown
- Review the output files to ensure acceptable formatting

**API rate limits**
- If processing many files, you may hit OpenAI rate limits
- The script will report errors for failed files and continue with others

## Cost Considerations

This script makes API calls to OpenAI, which incur costs based on token usage. Factors affecting cost:
- Document length (longer documents = more tokens)
- Model selection (GPT-4 is more expensive than GPT-3.5-turbo)
- Number of documents processed

Use `--dry-run` to preview before processing to estimate the number of documents.

## Testing

The project includes system tests to verify functionality:

### Run Mock Test (No API Key Required)
Tests document creation, conversion, and script execution without making API calls:
```bash
python3 tests/test_redaction_mock.py
```

### Run Full Test (Requires API Key)
Tests the complete redaction workflow including OpenAI API calls:
```bash
# Set your API key first
export OPENAI_API_KEY=your_key_here

# Run the test
python3 tests/test_redaction.py
```

The full test creates a sample document with student information, runs the redaction script, and verifies that:
- Student names, emails, and IDs are properly redacted
- Redaction placeholders are inserted correctly
- Non-student information (like professor names) is preserved

## License

This tool is provided as-is for educational and professional use.
# letters-of-rec
