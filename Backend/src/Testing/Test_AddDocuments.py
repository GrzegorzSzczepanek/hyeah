import getpass
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import re
import getpass
import os

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

openai_api_key = os.getenv("OPENAI_API_KEY")


# Function to clean excessive whitespace, newlines, and irrelevant navigation content from document text
def clean_document_text(text):
    
    # Remove excessive newlines and multiple spaces
    text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
    text = re.sub(r'\s{2,}', ' ', text)  # Remove multiple spaces
    text = text.strip()  # Remove leading/trailing white spaces
    
    # Remove any remaining large blocks of empty lines
    text = re.sub(r'\n\s*\n', '\n', text)  # Replace multiple newlines with a single newline
    
    return text

# Set embeddings

def set_embeddings():
    embd = OpenAIEmbeddings()

    # Docs to index
    urls = [
        "https://www.podatki.gov.pl/pcc-sd/rozliczenie-podatku-pcc-od-pozyczki/",
        "https://www.podatki.gov.pl/pcc-sd/rozliczenie-podatku-pcc-od-innych-czynnosci/",
        "https://www.podatki.gov.pl/pcc-sd/rozliczenie-podatku-pcc-od-kupna-samochodu/",
    ]

    # Load
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    # Clean the documents

    for doc in docs_list:
        doc.page_content = clean_document_text(doc.page_content)

    # Split the cleaned documents
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=100
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorstore
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embd,
    )

    # Create retriever
    retriever = vectorstore.as_retriever()

    for i, doc in enumerate(doc_splits[:2]):  # Print first 5 chunks
        print(f"Chunk {i+1}: {doc.page_content}")

    # Example query to test retrieval
    query = "Kto jest zwolniony z podatku"
    retrieved_docs = retriever.get_relevant_documents(query)

    # Print the retrieved documents
    for i, doc in enumerate(retrieved_docs[:3]):  # Limit to first 3 results
        print(f"Retrieved Document {i+1}: {doc.page_content}\n")

if __name__ == "__main__":
    set_embeddings()
        