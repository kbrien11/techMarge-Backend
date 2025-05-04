import base64
import json
import requests
from decouple import config
from .serializers import GitHubToolsSerializer
from .models import GitHubTools
import firebase_admin
from firebase_admin import messaging


token = config("GITHUB_API_KEY")
GOOSE_API_KEY = config("GOOSE_API_KEY")

headers = {
    "Authorization": f"token {token}",
    "Content-Type": "application/vnd.github+json",
}


def determinePopularity(count):
    if count < 10000:
        return "low"
    elif count > 10000 and count < 50000:
        return "medium"
    elif count > 50000 and count < 100000:
        return "high"
    else:
        return "Super"


def getGitHubData(topic):
    url = f"https://api.github.com/search/repositories?q=language:{topic}&sort=stars&order=desc"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        sol = [
            GitHubTools(
                name=repo["name"].capitalize(),
                description=repo["description"],
                language=repo["language"],
                stargazers_count=repo["stargazers_count"],
                popularity=determinePopularity(repo["stargazers_count"]),
                created_at=repo["created_at"],
                homepage=repo["homepage"],
                owner=repo["owner"]["login"],
                type="framework",
                location="backend",
            )
            for repo in data["items"]
            if repo["homepage"] != None
            if len(repo["homepage"]) > 0
            if repo["description"] != None
            if repo["name"] != "framework"
        ]

        GitHubTools.objects.bulk_create(sol)
        return sol
    else:
        print("error")


def getToolData(topic):
    url = f"https://api.github.com/search/topics"
    params = {"q": f"{topic}"}
    local_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.github.mercy-preview+json",
    }
    response = requests.get(url, headers=local_headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for tool in data.get("items"):
            print(tool)
            if tool.get("name").lower() == topic.lower():
                return tool

    else:
        print("error")


def getReadMeContents(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        print(content)
        return content
    else:
        return "error"


def call_gpt(prompt):

    api_url = "https://openrouter.ai/api/v1/completions"
    # test = "https://api.goose.ai/v1/engines"
    local_headers = {
        "Authorization": f"Bearer {GOOSE_API_KEY}",
        "content-type": "application/json",
    }

    payload = {
        "model": "google/gemini-2.0-flash-001",
        "prompt": prompt,
        "max_tokens": 400,
        "temperature": 0.3,
        "top_p": 0.5,
    }
    print(json.dumps(payload))

    response = requests.post(api_url, headers=local_headers, json=payload)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "").strip()

    if response.status_code == 400:
        print(response.text)
        data = response.json()
        print(data)
    if response.status_code == 401:
        data = response.json()
        print(data)
    if response.status_code == 429:
        data = response.json()
        print(data)

    else:
        return "error"


# myapp/utils.py (or wherever you keep your utility functions)
