import requests

token = "api_key"

headers = {"Authorization": f"token {token}"}


def getGitHubData(topic):
    url = f"https://api.github.com/search/repositories?q=language:{topic}"
    response = requests.get(url, headers=headers)
    sol = []
    if response.status_code == 200:
        data = response.json()
        for repo in data["items"]:
            output = {}
            if repo["stargazers_count"] > 5000:
                output["name"] = repo["name"]
                output["description"] = repo["description"]
                output["language"] = repo["language"]
                output["stargazers_count"] = repo["stargazers_count"]
                sol.append(output)

        return sol
    else:
        print("error")
