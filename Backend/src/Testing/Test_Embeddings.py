import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb

openai_api_key = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def createTestStore():
    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",
    )


def testVectorClient():
    persistent_client = chromadb.PersistentClient()
    collection = persistent_client.get_or_create_collection("example_collection")
    collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name="example_collection",
        embedding_function=embeddings,
    )

    print(vector_store_from_client.get())


if __name__ == "__main__":
    testVectorClient()
