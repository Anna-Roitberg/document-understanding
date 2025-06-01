from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class DocType(Enum):
    invoice = "invoice"
    contract = "contract"
    report = "report"
    other = "other"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Classification(BaseModel):
    document_class: DocType = Field(description="Class of the document invoice, contract, earnings or other")
    confidence: float = Field(
        description="How likely (probability) the predictions are correct"
    )


class Invoice(BaseModel):
    vendor: str | None = Field(description="The company or person issued the invoice (the seller)")
    amount: float | None = Field(description="Total invoice amount  (only the number)")
    currency: str | None = Field(description='The specific currency of the invoice')
    due_date: datetime | None = Field(description="The deadline by which the payment must be made (if specified)")
    line_items: list[str] | None = Field(description="Detailed list of individual products or services")


class Report(BaseModel):
    reporting_period: list[datetime] | None = Field(description="Time span the report covers: two dates) "
                                                                "in a format [start_date, end_date], not the sign date")
    executive_summary: str | None = Field(description="Summary of the report")
    key_metrics: list[str] | None = Field(description="Key Metrics: Essential numerical indicators "
                                                      "(e.g., Performance indicators, Strategic KPIs, "
                                                      "Quantitative results, Strategic KPIs etc.)")


class Contract(BaseModel):
    parties: list[str] | None = Field(description="Contract parties")
    amount: float | None = Field(description="Total invoice amount")
    effective_date: datetime | None = Field(description="Contract effective date")
    termination_date: datetime | None = Field(description="Contract termination date")


class PDFDocument(BaseModel):
    document_id: str = Field(description="Document uuid")
    file_name: str = Field(description="Document file name")
    status: ProcessingStatus = Field(description="Document processing status")
    page_count: int = Field(description="Number of pages in document")
    author: str | None = Field(description="Document author")
    classification: Classification | None = Field(description="Document classification")
    metadata: Invoice | Contract | Report | None = Field(description="LLM extracted document metadata")
