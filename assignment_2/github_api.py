import requests, os
import openai_api
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def search_github(query, num_requests=20):
    # Search and returns repositories relevant to input qeury
    headers = {'Authorization':f'Bearer {GITHUB_TOKEN}', "Accept": 'application/vnd.github+json'}
    url = f"https://api.github.com/search/repositories?q={query}+in:name+in:description+in:topics+in:readme"

    # Get the first n requests
    try:
        response = requests.get(url, headers=headers).json()
        results = response["items"][:num_requests]

    # raise exception if API returns a different status code
    except Exception as e:
        print("Error: ", e)
        print(response)
        results = []

    return results


def get_repo_summary(repo_name):
    # Acceses the repository to compile and summarize the text content of all readme files
    headers = {'Authorization':f'Bearer {GITHUB_TOKEN}', "Accept": 'application/vnd.github+json'}

    # Access repo via full repo name
    url = f"https://api.github.com/repos/{repo_name}/contents/"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except:
        return ""
    files = response.json()


    # Iterates through each file in repo, and extracts text content if file is a readme
    text_content = ""
    for file in files:
        if 'readme' in file['name'].lower():
            try:
                response = requests.get(file['download_url'], headers=headers)
                response.raise_for_status()
                text_content += response.text
            except:
                continue
        
    if len(text_content) < 50:
        summary = ""
    else:
        summary = openai_api.openai_summarize(text_content)

    return summary