import os
import re
import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
import uuid

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

openai_api_key = os.getenv("OPENAI_API_KEY")

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

def createTestStore():
    persist_directory = "./chroma_db"
    collection_name = "tax_collection"

    vectorstore = Chroma(
        embedding_function=embd,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )

def set_embeddings():

    persistent_client = chromadb.PersistentClient()
    collection = persistent_client.get_or_create_collection("tax_collection")

    # Docs to index
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

    # Split the cleaned documents
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=100
    )
    doc_splits = text_splitter.split_documents(docs)
    

    doc_texts = [doc.page_content for doc in doc_splits]

    # Generate unique IDs for each document chunk
    doc_ids = [str(uuid.uuid4()) for _ in range(len(doc_texts))]
    # Generate unique IDs for each document chunk
    #doc_ids = [str(uuid.uuid4()) for _ in range(len(doc_splits))]

    # Add the documents and their IDs to the collection
    collection.add(documents=doc_texts, ids=doc_ids)
    #collection.add(documents=doc_splits)
    print("Embeddings have been created and stored persistently.")

def test_vector_client():
    persist_directory = "./chroma_db"
    collection_name = "tax_collection"

 
    # Load the existing vectorstore
    vector_store = Chroma(
        embedding_function=embd,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )
    print("Kto jest zwolniony z podatku")

    results = vector_store.similarity_search(
    "Kto jest zwolniony z podatku",
    k=2,
    #filter={"source": "tweet"},
    )
    print(results)
    for res in results:

        print(res)
        print(f"* {res.page_content} [{res.metadata}]")
        # Create retriever
    #retriever = vectorstore.as_retriever()


if __name__ == "__main__":
    #createTestStore()
    # First, set embeddings and store them persistently
    set_embeddings()
    # Then, test retrieving from the persistent vectorstore
    test_vector_client()
