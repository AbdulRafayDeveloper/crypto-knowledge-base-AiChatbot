import requests
from langchain_community.document_loaders import WebBaseLoader
from services.groq_llm import llm
from services.prompts import prompt_template
import re
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import HTTPException,status
ETHERSCAN_API_KEY=os.getenv('ETHERSCAN_API_KEY')
WALLET_ADDRESS=os.getenv('WALLET_ADDRESS')
API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=balance&address={WALLET_ADDRESS}&tag=latest&apikey={ETHERSCAN_API_KEY}"


class Application:
    def __init__(self, url):
        self.url = url

    def load_documents(self):
        """Load the documents from the webpage."""
        loader = WebBaseLoader(self.url)
        documents = loader.load()
        return "".join([docs.page_content for docs in documents])

    def answer_question(self, page_data, query):
        """Generate an answer based on the page data and query."""
        prompt = prompt_template.format(page_data=page_data, question=query)
        response = llm.invoke(prompt)
        return response.content

    def run(self,query):
        """Run the application, load documents, and generate a response."""
        page_data = self.load_documents()
        try:
            response = self.answer_question(page_data, query)
            # clean the response using regular expressions
            response = re.sub(r'\n+', ' ', response)
            return response
        except Exception as e:
            return str(e)  # Return the error message

    def __str__(self):
        """Override the string representation of the application."""
        return f"Application to scrape URL: {self.url}"

if __name__ == '__main__':
    pass