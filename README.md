# Document Understanding

An intelligent document processing system that uses AI to analyze and extract information from PDF documents. The system can classify documents into different types (Invoice, Contract, Report) and extract relevant metadata based on the document type.

## Features

- PDF document loading and processing
- Automatic document classification
- Structured information extraction based on document type
- Support for multiple document types:
  - Invoices
  - Contracts
  - Reports
- Cost tracking for API usage
- JSON output generation

## Prerequisites

- Python 3.x
- OpenAI API key (for GPT-4 access)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-understanding.git
cd document-understanding
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
```

## Project Structure

- `process_pdf.py` - Main script for processing PDF documents
- `models/` - Contains data models and document type definitions
- `api/` - API-related code
- `input/` - Directory for input PDF files
- `output/` - Directory for processed JSON output files
- `run_server.py` - Server application entry point

## Usage

To process a PDF document:

```bash
python process_pdf.py -i path/to/your/document.pdf
```

The processed results will be saved as a JSON file in the `output/` directory.

## API Server

To run the API server:

```bash
python run_server.py
```

## API Playground

The project includes an API playground script (`api_playground.py`) that demonstrates how to interact with the API endpoints. This script is useful for testing and understanding the API functionality.

To run the API playground script:

```bash
python api_playground.py -i path/to/your/document.pdf
```

The script demonstrates the following API endpoints:

1. Document Analysis (`POST /documents/analyze`)
   - Uploads and analyzes a PDF document
   - Returns document metadata and classification results

2. Get Document Metadata (`GET /documents/{document_id}`)
   - Retrieves metadata for a specific document

3. Download Document (`GET /documents/{document_id}/download`)
   - Downloads the original document

4. Get Document Actions (`GET /documents/{document_id}/actions`)
   - Retrieves available actions for a specific document

The script outputs the results of each API call in a formatted JSON structure.

Note: Make sure the API server is running (`python run_server.py`) before using the playground script. By default, the script connects to `http://localhost:8000`.

## API Documentation

Detailed API documentation is available in the `docs/api_docs.md` file. The API provides the following endpoints:

### Document Analysis Endpoints

1. `POST /documents/analyze`
   - Upload and analyze PDF documents
   - Returns document metadata and analysis results

2. `GET /documents/{document_id}`
   - Retrieve document metadata
   - Returns classification and extracted information

3. `GET /documents/{document_id}/download`
   - Download the original document

4. `GET /documents/{document_id}/actions`
   - Get available actions for a document
   - Supports filtering by status, priority, and deadline

To view the complete API documentation, see `docs/api_docs.md` in the project repository.


