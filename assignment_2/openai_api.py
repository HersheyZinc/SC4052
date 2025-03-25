from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

def openai_query(messages, model="gpt-4o-mini", temperature=0, max_tokens=4096):
    # basic function to query OpenAI's models
    response = OpenAI().chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    reply = response.choices[0].message.content

    return reply


def openai_summarize(content):
    # summarizes input string
    system_prompt = "You are a helpful AI assistant. The user has collated a repository's readme files. Your task is to summarize it into 2 sentences or less. Avoid using technical jargon and use simple English to describe the concepts"
    messages = [{"role":"system", "content": system_prompt}, {"role":"user","content":content}]
    
    summary = openai_query(messages, model="gpt-4o-mini", temperature=0, max_tokens=4096)

    return summary


# def openai_get_tags(content):
#     system_prompt = "You are a helpful AI assistant. Extract important tags from the user's query and format them as a comma separated list. Example: Python, LLM, OpenAI"
#     messages = [{"role":"system", "content": system_prompt}, {"role":"user","content":content}]
    
#     tags = openai_query(messages, model="gpt-4o-mini", temperature=0, max_tokens=400)

#     return tags