import asyncio
import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_community.callbacks.manager import get_openai_callback
import uuid
import os
from models import *

llm = init_chat_model("gpt-4o", model_provider="openai")

classification_prompt = ChatPromptTemplate.from_template(
    """
Given the extracted text content of a PDF document, classify it into one of the following categories {data_type}:

Passage:
{input}
"""
)

tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the properties mentioned in the {data_type} function form the document.
If some information isn't mentioned put None
The document:
{input}
    """
    )


type2struct = {DocType.invoice: ("'Invoice'", Invoice),
               DocType.contract: ("'Contract'", Contract),
               DocType.report: ("'Report'", Report)}


async def load_pdf(pdf_path: str):
    # PyPDFLoader.load() is not async, so we should run it in a separate thread
    loader = PyPDFLoader(pdf_path)
    # Use asyncio.to_thread for CPU-bound operations
    pages = await asyncio.to_thread(loader.load)

    if pages:
        print(f"Metadata for first page: {pages[0].metadata}\n")
    else:
        print("No pages found in the PDF")
    print(f"{pages[0].metadata}\n")

    return pages


async def process(file_name):

    try:
        data = await load_pdf(file_name)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return

    assert len(data) > 0
    document = PDFDocument(document_id=uuid.uuid4().hex, file_name=file_name, page_count=len(data),
                           status=ProcessingStatus.COMPLETED,
                           author=None, classification=None, metadata=None)

    structured_llm = llm.with_structured_output(Classification)

    document.author = data[0].metadata.get('author', None)
    inp = "\n\n".join([p.page_content for p in data])

    inp_fp = data[0].page_content  # First page

    prompt = classification_prompt.invoke({"input": inp_fp, "data_type": "'Classification'"})
    cost_analyze = 0
    with get_openai_callback() as cb:
        response = structured_llm.invoke(prompt)
        cost_classification = cb.total_cost

    print("response: ", response)
    document.classification = response
    if response.document_class != DocType.other:
        structured_llm = llm.with_structured_output(type2struct[response.document_class][1])
        prompt = tagging_prompt.invoke({"input": inp, "data_type": type2struct[response.document_class][0]})
        with get_openai_callback() as cb:
            response = structured_llm.invoke(prompt)
            cost_analyze = cb.total_cost
        print(response)
        document.metadata = response
    print("Estimated cost", cost_classification + cost_analyze)
    return document


def main():
    parser = argparse.ArgumentParser(description='LLM analyze documents')

    parser.add_argument("-i", "--input_file", type=str, help="Input PDF")
    args = parser.parse_args()

    file_location = args.input_file
    file_name = os.path.basename(file_location)  # eds_report.csv
    doc_data = asyncio.run(process(file_location))
    if doc_data:
        with open("output/"+file_name+".json", "w", encoding="utf-8") as f:
            f.write(doc_data.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
