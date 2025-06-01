from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic.tools import parse_obj_as
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid
from models import PDFDocument, ProcessingStatus
import glob
import os
import json

app = FastAPI(
    title="Document Analysis API",
    description="AI-friendly API for document processing and metadata extraction"
)

class ActionStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Action(BaseModel):
    action_id: str
    description: str
    status: ActionStatus
    deadline: Optional[datetime]
    priority: Priority
    assignee: Optional[str]


@app.post("/documents/analyze", response_model=PDFDocument)
async def analyze_document(file: UploadFile = File(...)):
    # Mock implementation
    # TRY to find preprocessed document
    processed_docs = glob.glob("output/*.json")
    file_names = [os.path.basename(path) for path in processed_docs]
    file_name = os.path.basename(file.filename)
    if file_name + ".json" in file_names:
        with open("output/"+file_name + ".json", encoding="utf-8") as f:
            doc_dict = json.load(f)
        doc = parse_obj_as(PDFDocument, doc_dict)
        return doc
    else:
        # Here we should send document to processing query - and return reply with ProcessingStatus = pending
        return HTTPException(status_code=404, detail="Document not found is static examples, please run process_pdf.py")


def load_static_documents(folder="output"):
    processed_docs_jsons = glob.glob(f"{folder}/*.json")
    documents_dict = dict()
    for json_file in processed_docs_jsons:
        with open(json_file, encoding="utf-8") as f:
            doc_dict = json.load(f)
        doc = parse_obj_as(PDFDocument, doc_dict)
        documents_dict[doc.document_id] = doc
    return documents_dict


@app.get("/documents/{document_id}", response_model=PDFDocument)
async def get_document(document_id: str):
    documents = load_static_documents()
    # Mock implementation
    if not document_id in documents.keys():
        raise HTTPException(status_code=404, detail="Document not found")
    return documents[document_id]


@app.get("/documents/{document_id}/download")
async def get_document_download(document_id: str):
    documents = load_static_documents()

    # Check if document_id is valid
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = documents[document_id].file_name

    # Ensure file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Return file as download
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=os.path.basename(file_path)
    )


@app.get("/documents/{document_id}/actions", response_model=List[Action])
async def get_document_actions(
        document_id: str,
        status: Optional[ActionStatus] = None,
        priority: Optional[Priority] = None,
        deadline_before: Optional[datetime] = None
):
    # Mock implementation
    if not document_id:
        raise HTTPException(status_code=404, detail="Document not found")

    actions = [
        Action(
            action_id=str(uuid.uuid4()),
            description="Review document content",
            status=ActionStatus.TODO,
            deadline=datetime.now(),
            priority=Priority.HIGH,
            assignee="jane.doe@example.com"
        ),
        Action(
            action_id=str(uuid.uuid4()),
            description="Update metadata",
            status=ActionStatus.IN_PROGRESS,
            deadline=datetime.now(),
            priority=Priority.MEDIUM,
            assignee="john.doe@example.com"
        )
    ]

    # Apply filters
    if status:
        actions = [a for a in actions if a.status == status]
    if priority:
        actions = [a for a in actions if a.priority == priority]
    if deadline_before:
        actions = [a for a in actions if a.deadline and a.deadline < deadline_before]

    return actions


@app.on_event("startup")
def list_routes():
    print("Registered Endpoints:")
    for route in app.routes:
        methods = ", ".join(route.methods or [])
        print(f"{methods:10} {route.path}")