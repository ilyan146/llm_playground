from .website import Website
from .message_formatter import convert_to_llm_message, website_user_prompt
from openai import OpenAI

SYS_PROMPT = "You are an assitant that analyzes the contents of a website \
and provide a short summary, ignoring the text that might be navigation related. \
Respond in Markdown format."


def summarize_website(url: str):
    website = Website(url)
    response = OpenAI().chat.completions.create(
        model="gpt-4o-mini",
        messages=convert_to_llm_message(
            sys_prompt=SYS_PROMPT,
            messages=website_user_prompt(website)
        ) # type: ignore
    )
    return response.choices[0].message.content
