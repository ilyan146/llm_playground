import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class Website:

    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            }

        self.title = None
        self.text = None

    def fetch_website_contents(self):
        response = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            # Remove irrelevant
            for irrelevant in soup.body(["script", "style", "img", "input"]): # type: ignore
                irrelevant.decompose()
            self.text = soup.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        return (self.title + "\n\n" + self.text)[:2_000]


    def fetch_website_links(self):
        response = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return [link for link in links if link]

