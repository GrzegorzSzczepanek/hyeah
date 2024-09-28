from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os

# Replace with your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

print(openai_api_key)

# Initialize the OpenAI LLM (Language Learning Model)
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.7)

# Create a PromptTemplate
template = """
You are a helpful assistant. Answer the following question:
Question: {question}
Answer:
"""
prompt = PromptTemplate(input_variables=["question"], template=template)

# Create an LLMChain (this will connect the language model with the prompt)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Example usage: Ask a question and get a response
def ask_question(question):
    return llm_chain.run(question)

if __name__ == "__main__":
    question = input("What is your question? ")
    response = ask_question(question)
    print("Response from GPT: ", response)
