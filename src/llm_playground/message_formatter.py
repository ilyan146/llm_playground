from .website import Website

# Modified user prompt
def website_user_prompt(website: Website) -> str:
    user_prompt =  f"You are looking at a website titled '{website.title}'\n\nThe content of this website is as follows:\n{website.text}\n\nPlease provide a concise summary of the main points. \
    If there are news or announcements, then summarize these too. \n\n"
    return user_prompt


def convert_to_llm_message(sys_prompt: str, messages: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": messages}
    ]