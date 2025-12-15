from llm_playground.website import Website
# from .message_formatter import convert_to_llm_message, website_user_prompt
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv(override=True)

class BrochureGenerator:
    MODEL = "gpt-4o-mini"
    openai = OpenAI()
    SYS_PROMPT = """
    You are provided with a list of links found on a webpage.
    You are able to decide which of the links would be most relevant to include in a brochure about the company,
    such as links to an About page, or a Company page, or Careers/Jobs pages.
    You should respond in JSON as in this example:

    {
        "links": [
            {"type": "about page", "url": "https://full.url/goes/here/about"},
            {"type": "careers page", "url": "https://another.full.url/careers"}
        ]
    }
    """
    BROCHURE_SYS_PROMPT = """
    You are an assistant that analyzes the contents of several relevant pages from a company website
    and creates a short brochure about the company for prospective customers, investors and recruits.
    Respond in markdown without code blocks.
    Include details of company culture, customers and careers/jobs if you have the information.
    """

    def __init__(self, url: str):
        self.url = url
        self.website = Website(url)

    def create_brochure(self, company_name: str):
        stream = self.openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": self.BROCHURE_SYS_PROMPT},
                {"role": "user","content": self.get_brochure_user_prompt(company_name)},
            ],
            stream=True
        )

        response=""
        for chunk in stream:
            if chunk.choices and hasattr(chunk.choices[0].delta, "content"):
                response += chunk.choices[0].delta.content or ""
                print(response, end="", flush=True)
        # result = response.choices[0].message.content
        return response


    def get_brochure_user_prompt(self, company_name: str):
        user_prompt = f"""
        You are looking at a company called: {company_name}
        Here are the contents of its landing page and other relevant pages;
        use this information to build a short brochure of the company in markdown without code blocks.\n\n
        """
        user_prompt += self.fetch_page_and_relevant_links()
        user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
        return user_prompt

    def fetch_page_and_relevant_links(self):
        contents = self.website.fetch_website_contents()
        relevant_links = self.select_relevant_links()
        result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
        for link in relevant_links["links"]:
            result += f"\n\n### Link: {link['type']}\n"
            # new website instance for each link
            link_website = Website(link["url"])
            result += link_website.fetch_website_contents()
        return result

    def select_relevant_links(self):
        print(f"Selecting relevant links for {self.url} by calling {self.MODEL}")
        response = self.openai.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.SYS_PROMPT},
                {"role": "user", "content": self.get_links_user_prompt()},
            ],
            response_format={"type": "json_object"},
        )
        result = response.choices[0].message.content
        links = json.loads(result)
        print(f"Found {len(links['links'])} relevant links")
        return links

    def get_links_user_prompt(self):
        user_prompt = f"""
        Here is the list of links on the website {self.url} -
        Please decide which of these are relevant web links for a brochure about the company, 
        respond with the full https URL in JSON format.
        Do not include Terms of Service, Privacy, email links.

        Links (some might be relative links):

        """
        links = self.website.fetch_website_links()
        user_prompt += "\n".join(links)
        return user_prompt





