from langchain_community.document_loaders import WebBaseLoader
from services.groq_llm import llm
from services.prompts import prompt_template


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
            answer = self.answer_question(page_data, query)
            return answer  # Return the answer for further use
        except Exception as e:
            return str(e)  # Return the error message

    def __str__(self):
        """Override the string representation of the application."""
        return f"Application to scrape URL: {self.url}"


if __name__ == '__main__':
    pass