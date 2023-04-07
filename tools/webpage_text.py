
import requests
from bs4 import BeautifulSoup
from langchain.requests import RequestsWrapper
from langchain.tools.base import BaseTool
from langchain.tools.requests.tool import RequestsGetTool

def strip_html_tags(html_string):
    # Parse HTML string using BeautifulSoup
    soup = BeautifulSoup(html_string, 'html.parser')
    # Find the body tag
    body = soup.find('body')
    if body:
        # Extract text from the body tag
        stripped_string = body.get_text(strip=True)
    else:
        stripped_string = ""
    # Strip any extra white space and return the extracted text
    return stripped_string.strip()


class RequestsGetTextTool(RequestsGetTool):

    def _run(self, url: str) -> str:
        # Send a GET request to the URL and get the response
        response = requests.get(url, headers=self.requests_wrapper.headers)
        if response.status_code != 200:
            # Return empty string if response status code is not 200
            return ""
        # Parse HTML response and extract text using `strip_html_tags` function
        text = strip_html_tags(response.text)
        return text

    async def _arun(self, url: str) -> str:
        # TODO: implement async version with aiohttp to care 200 status code
        return await self.requests_wrapper.aget(url)


def get_requests_text_tool() -> BaseTool:
    # Return an instance of `RequestsGetTextTool` with an instance of `RequestsWrapper`
    return RequestsGetTextTool(requests_wrapper=RequestsWrapper())
