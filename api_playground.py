import requests
from typing import Dict, List
from pprint import pprint
import argparse
from models import PDFDocument
# Base URL - replace with your actual API base URL
BASE_URL = "http://localhost:8000"  # Change this to match your API server


def test_analyze_document(file_path: str) -> Dict:
    """Test the document analysis endpoint by sending a file."""
    url = f"{BASE_URL}/documents/analyze"
    
    # Prepare the file for upload
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/pdf')}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("✅ Document analysis successful!")
        return response.json()
    else:
        print(f"❌ Error analyzing document: {response.status_code}")
        print(response.text)
        return {}


def test_get_document(document_id: str) -> Dict:
    """Test retrieving metadata for a specific document by ID."""
    url = f"{BASE_URL}/documents/{document_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        print("✅ Document retrieved successfully!")
        return response.json()
    else:
        print(f"❌ Error retrieving document: {response.status_code}")
        print(response.text)
        return {}


def test_get_document_download(document_id: str):
    """Test downloading a specific document by ID."""
    url = f"{BASE_URL}/documents/{document_id}/download"
    response = requests.get(url)

    if response.status_code == 200:
        if response.content:
            print("✅ Document downloaded successfully!")
        return {}
    else:
        print(f"❌ Error retrieving document: {response.status_code}")
        print(response.text)


def test_get_document_actions(document_id: str) -> List:
    """Test retrieving actions for a specific document."""
    url = f"{BASE_URL}/documents/{document_id}/actions"

    response = requests.get(url)
    
    if response.status_code == 200:
        print("✅ Document actions retrieved successfully!")
        return response.json()
    else:
        print(f"❌ Error retrieving document actions: {response.status_code}")
        print(response.text)
        return []


def main():
    parser = argparse.ArgumentParser(description='LLM analyze API test example')

    parser.add_argument("-i", "--input_file", type=str, default="input/Earnings.PDF", help="Input PDF")
    args = parser.parse_args()

    print("\n1. Testing document analysis endpoint...")
    analysis_response = test_analyze_document(args.input_file)
    analysis_result = PDFDocument(**analysis_response)
    document_id = analysis_result.document_id
    pprint(analysis_result.model_dump_json(indent=2))
    
    print("\n2. Testing get document endpoint...")
    document_response = test_get_document(document_id)
    document_result = PDFDocument(**document_response)
    pprint(document_result.model_dump_json(indent=2))

    print("\n3. Testing download document endpoint...")
    document_response = test_get_document_download(document_id)
    pprint(document_response)
    
    print("\n4. Testing get document actions endpoint...")
    actions_result = test_get_document_actions(document_id)
    pprint(actions_result)


if __name__ == "__main__":
    main()
