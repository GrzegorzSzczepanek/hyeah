from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_model = "gpt-4o-mini"

print(openai_api_key)

# Initialize the OpenAI LLM (Language Learning Model)
llm = ChatOpenAI(api_key=openai_api_key, model=llm_model, temperature=0.7)

template = """
You are a helpful assistant. Answer the following question:
Question: {question}
Answer:
"""
prompt = PromptTemplate(input_variables=["question"], template=template)

llm_chain = LLMChain(llm=llm, prompt=prompt)


def ask_question(question):
    return llm_chain.run(question)


if __name__ == "__main__":
    question = input("What is your question? ")
    response = ask_question(question)
    print("Response from GPT: ", response)
