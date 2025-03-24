from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

def openai_query(messages, model="gpt-4o-mini", temperature=0, max_tokens=4096):

    response = OpenAI().chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    reply = response.choices[0].message.content

    return reply


def openai_summarize(content):

    system_prompt = "You are a helpful AI assistant. Summarize the user's query into 2 sentences or less."
    messages = [{"role":"system", "content": system_prompt}, {"role":"user","content":content}]
    
    summary = openai_query(messages, model="gpt-4o-mini", temperature=0, max_tokens=4096)

    return summary


def openai_get_tags(content):
    system_prompt = "You are a helpful AI assistant. Extract important tags from the user's query and format them as a comma separated list. Example: Python, LLM, OpenAI"
    messages = [{"role":"system", "content": system_prompt}, {"role":"user","content":content}]
    
    tags = openai_query(messages, model="gpt-4o-mini", temperature=0, max_tokens=400)

    return tags