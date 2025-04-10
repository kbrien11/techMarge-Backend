import requests

from .serializers import GitHubToolsSerializer
from .models import GitHubTools

token = "api_key"

headers = {"Authorization": f"token {token}"}


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
    url = f"https://api.github.com/search/repositories?q=framework+language:{topic}"
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
            )
            for repo in data["items"]
            if repo["homepage"] != None
            if len(repo["homepage"]) > 0
            if repo["description"] != None
        ]
        GitHubTools.objects.bulk_create(sol)
        return sol
    else:
        print("error")
