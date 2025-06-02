# Document Analysis API

AI-friendly API for document processing and metadata extraction


# APIs

## POST /documents/analyze

Analyze a document

Analyze a PDF document using LLM.




### Request Body

[Body_analyze_document_documents_analyze_post](#body_analyze_document_documents_analyze_post)







### Responses

#### 200


Successful Response








#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /documents/{document_id}

Get Document Metadata

Retrieve the metadata of a document by its unique document_id.


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| document_id | string | True | Unique document id |


### Responses

#### 200


Successful Response


[PDFDocument](#pdfdocument)







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /documents/{document_id}/download

Download Document

Download a document by its unique document_id.


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| document_id | string | True | The unique identifier of the document to retrieve. |


### Responses

#### 200


Successful Response








#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /documents/{document_id}/actions

Get Document Actions



### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| document_id | string | True | Unique document id |
| status |  | False |  |
| priority |  | False |  |
| deadline_before |  | False |  |


### Responses

#### 200


Successful Response


array







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







# Components



## Action



| Field | Type | Description |
|-------|------|-------------|
| action_id | string | Unique action id |
| description | string | Action description |
| status |  | Action status |
| deadline |  | Action deadline |
| priority |  | Action priority |
| assignee |  | Action assigned to |


## ActionStatus





## Body_analyze_document_documents_analyze_post



| Field | Type | Description |
|-------|------|-------------|
| file | string | A PDF file to analyze and extract metadata |


## Classification



| Field | Type | Description |
|-------|------|-------------|
| document_class |  | Class of the document invoice, contract, report or other |
| confidence | number | Confidence score indicating the probability that the predicted class is correct. |


## Contract



| Field | Type | Description |
|-------|------|-------------|
| parties |  | Companies or individuals legally bound by the contract |
| effective_date |  | The date when the contract becomes legally enforceable |
| termination_date |  | The date on which the contract expires or ends |
| key_terms |  | Core conditions, obligations, or clauses that define the agreement |
| confidence | number | Confidence score indicating the likelihood that the extracted contract details are accurate. |


## DocType





## HTTPValidationError



| Field | Type | Description |
|-------|------|-------------|
| detail | array |  |


## Invoice



| Field | Type | Description |
|-------|------|-------------|
| vendor |  | The company or person issued the invoice (the seller) |
| amount |  | Total invoice amount  (only the number) |
| currency |  | The specific currency of the invoice. In the invoice the currency can be found  as a currency  symbol (as $) or abbreviation (as USD), either before or after the amount.  |
| due_date |  | The deadline by which the payment must be made (if specified) |
| line_items |  | List of meaningful individual products or services only (excluding prices), using the exact phrasing and language from the invoice. Irrelevant entries are excluded. If multiple identical are in the invoice include the quantity. |
| confidence | number | Confidence score indicating the likelihood that the extracted invoice information is accurate |


## PDFDocument



| Field | Type | Description |
|-------|------|-------------|
| document_id | string | Unique identifier of the document |
| file_name | string | Original name of the uploaded document file |
| status |  | Current processing status of the document |
| page_count | integer | Total number of pages in the document |
| author |  | Author of the document, if available |
| classification |  | Predicted document type |
| metadata |  | Structured metadata extracted from the document using an LLM |


## Priority





## ProcessingStatus





## Report



| Field | Type | Description |
|-------|------|-------------|
| reporting_period |  | Time span the report covers: two dates in a format [start_date, end_date], not the sign date |
| executive_summary |  | Summary of the report |
| key_metrics |  | Key Metrics: Essential numerical indicators (e.g., Performance indicators, Strategic KPIs, Quantitative results, Strategic KPIs etc.) |
| confidence | number | Confidence score indicating the likelihood that the extracted report details are accurate |


## ValidationError



| Field | Type | Description |
|-------|------|-------------|
| loc | array |  |
| msg | string |  |
| type | string |  |
