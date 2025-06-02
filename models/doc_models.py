from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class DocType(str, Enum):
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
    document_class: DocType = Field(description="Class of the document invoice, contract, report or other")
    confidence: float = Field(
        description="Confidence score indicating the probability that the predicted class is correct."
    )


class Invoice(BaseModel):
    vendor: str | None = Field(description="The company or person issued the invoice (the seller)")
    amount: float | None = Field(description="Total invoice amount  (only the number)")
    currency: str | None = Field(description="The specific currency of the invoice. "
                                             "In the invoice the currency can be found  as a currency  symbol (as $)"
                                             " or abbreviation (as USD), "
                                             "either before or after the amount. ")
    due_date: datetime | None = Field(description="The deadline by which the payment must be made (if specified)")
    line_items: list[str] | None = Field(description="List of meaningful individual products or services only (excluding prices), "
                                                     "using the exact phrasing and language from the invoice. "
                                                     "Irrelevant entries are excluded. If multiple identical are in the invoice include the quantity.")
    confidence: float = Field(
        description="Confidence score indicating the likelihood that the extracted invoice information is accurate"
    )


class Report(BaseModel):
    reporting_period: list[datetime] | None = Field(description="Time span the report covers: two dates "
                                                                "in a format [start_date, end_date], not the sign date")
    executive_summary: str | None = Field(description="Summary of the report")
    key_metrics: list[str] | None = Field(description="Key Metrics: Essential numerical indicators "
                                                      "(e.g., Performance indicators, Strategic KPIs, "
                                                      "Quantitative results, Strategic KPIs etc.)")
    confidence: float = Field(
        description="Confidence score indicating the likelihood that the extracted report details are accurate"
    )


class Contract(BaseModel):
    parties: list[str] | None = Field(description="Companies or individuals legally bound by the contract")
    effective_date: datetime | None = Field(description="The date when the contract becomes legally enforceable")
    termination_date: datetime | None = Field(description="The date on which the contract expires or ends")
    key_terms: list[str] | None = Field(description="Core conditions, obligations, or clauses that define the agreement")
    confidence: float = Field(
        description="Confidence score indicating the likelihood that the extracted contract details are accurate."
    )


class PDFDocument(BaseModel):
    document_id: str = Field(description="Unique identifier of the document")
    file_name: str = Field(description="Original name of the uploaded document file")
    status: ProcessingStatus = Field(description="Current processing status of the document")
    page_count: int = Field(description="Total number of pages in the document")
    author: str | None = Field(description="Author of the document, if available")
    classification: Classification | None = Field(description="Predicted document type")
    metadata: Invoice | Contract | Report | None = Field(description="Structured metadata extracted from the document"
                                                                     " using an LLM")
