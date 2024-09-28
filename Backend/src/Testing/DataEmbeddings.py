import os
import re
import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import uuid

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI Embeddings
embd = OpenAIEmbeddings(model="text-embedding-ada-002")  # Adjust model if necessary

# Function to clean excessive whitespace, newlines, and irrelevant navigation content from document text
def clean_document_text(text):
    # Remove excessive newlines and multiple spaces
    text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
    text = re.sub(r'\s{2,}', ' ', text)  # Remove multiple spaces
    text = text.strip()  # Remove leading/trailing white spaces
    # Remove any remaining large blocks of empty lines
    text = re.sub(r'\n\s*\n', '\n', text)  # Replace multiple newlines with a single newline
    return text

def set_embeddings():
    persist_directory = "./chroma_db"
    collection_name = "tax_collection"

    # Initialize the Chroma vector store with the embedding function
    vector_store = Chroma(
        embedding_function=embd,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )

    # URLs to index
    urls = [
        "https://www.podatki.gov.pl/pcc-sd/rozliczenie-podatku-pcc-od-pozyczki/",
        "https://www.podatki.gov.pl/pcc-sd/rozliczenie-podatku-pcc-od-innych-czynnosci/",
        "https://www.podatki.gov.pl/pcc-sd/rozliczenie-podatku-pcc-od-kupna-samochodu/",
    ]

    # Load documents from URLs
    docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        docs.extend(loader.load())

    # Clean the documents
    for doc in docs:
        doc.page_content = clean_document_text(doc.page_content)

    # Split the cleaned documents into chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=100
    )
    doc_splits = text_splitter.split_documents(docs)

    # Generate unique IDs for each document chunk
    doc_ids = [str(uuid.uuid4()) for _ in range(len(doc_splits))]

    # Add the documents and their IDs to the vector store (embeddings are generated here)
    vector_store.add_documents(doc_splits, ids=doc_ids)

    print("Embeddings have been created and stored persistently.")

def test_vector_client():
    persist_directory = "./chroma_db"
    collection_name = "tax_collection"

    # Load the existing vector store with the same embedding function
    vector_store = Chroma(
        embedding_function=embd,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )
    print("Query: Kto jest zwolniony z podatku")

    # Perform a similarity search
    results = vector_store.similarity_search(
        "Kto jest zwolniony z podatku",
        k=3,
    )

    # Print the results
    for res in results:
        print(f"\nResult:")
        print(f"Content: {res.page_content}")
        print(f"Metadata: {res.metadata}")

if __name__ == "__main__":
    # First, set embeddings and store them persistently
    set_embeddings()
    # Then, test retrieving from the persistent vector store
    test_vector_client()
