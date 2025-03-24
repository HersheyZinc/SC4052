import requests, os
import openai_api
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def search_github(query, num_requests=20):

    headers = {'Authorization':f'Bearer {GITHUB_TOKEN}', "Accept": 'application/vnd.github+json'}
    url = f"https://api.github.com/search/repositories?q={query}+in:name+in:description+in:topics+in:readme"

    try:
        response = requests.get(url, headers=headers).json()
        results = response["items"][:num_requests]
    except Exception as e:
        print("Error: ", e)
        print(response)
        results = []

    return results


def get_repo_summary(repo_name):
    headers = {'Authorization':f'Bearer {GITHUB_TOKEN}', "Accept": 'application/vnd.github+json'}

    url = f"https://api.github.com/repos/{repo_name}/contents/"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except:
        return ""
    files = response.json()



    text_content = ""
    for file in files:
        if 'readme' in file['name'].lower():
            try:
                response = requests.get(file['download_url'], headers=headers)
                response.raise_for_status()
                text_content += response.text
            except:
                continue
        

    # if not text_content:
    #     for file in files:
    #         filename = file['name'].lower()
    #         if filename.endswith(".py") or filename.endswith(".ipynb"):
    #             try:
    #                 response = requests.get(file['download_url'], headers=headers)
    #                 response.raise_for_status()
    #                 text_content += response.text
    #             except:
    #                 continue
    if len(text_content) < 50:
        summary = ""
    else:
        summary = openai_api.openai_summarize(text_content)

    return summary