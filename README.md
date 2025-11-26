# Student Information Redaction Tool

A Python script that automatically redacts student-identifying information from Word documents using OpenAI's GPT models. The script converts `.docx` files to Markdown format and intelligently identifies and replaces student names, IDs, emails, and other personal information with standardized placeholders.

## Features

- Processes single `.docx` files or recursively scans directories
- Converts Word documents to clean Markdown format
- Uses OpenAI GPT models for intelligent redaction
- Replaces student information with standardized all-caps placeholders:
  - `[STUDENT_NAME]` - Student names
  - `[STUDENT_ID]` - Student ID numbers
  - `[STUDENT_EMAIL]` - Student email addresses
  - `[STUDENT_INFO]` - Other personal identifiers
- Preserves document structure and formatting
- Comprehensive error handling and logging
- Dry-run mode for preview without API calls

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

After installing with Poetry, you can use the `lor` command:

```bash
# Process a single file
lor redact letter.docx

# Process all .docx files in a directory recursively
lor redact ./letters/

# Use a specific OpenAI model
lor redact ./letters/ --model gpt-4-turbo

# Pass API key directly
lor redact letter.docx --api-key YOUR_API_KEY

# Dry run (preview without making changes)
lor redact ./letters/ --dry-run

# Enable verbose logging
lor redact ./letters/ --verbose

# View help
lor --help
lor redact --help
```

If using Poetry without installing globally:
```bash
poetry run lor redact letter.docx
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
