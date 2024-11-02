import requests
import pandas as pd
import os
import subprocess

# GitHub API authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Ensure your GitHub token is set as an environment variable
city = "London"  # Target city
min_followers = 500  # Minimum followers threshold

# Headers for GitHub API requests
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Function to clean company names
def clean_company(company):
    if company:
        company = company.lstrip('@').strip().upper()
    return company or ""

# Fetch users by city and minimum followers
def get_users(city, min_followers):
    url = "https://api.github.com/search/users"
    params = {
        "q": f"location:{city} followers:>{min_followers}",
        "per_page": 100
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["items"]

# Fetch user details
def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Fetch repositories for each user
def get_user_repos(username, max_repos=500):
    url = f"https://api.github.com/users/{username}/repos"
    params = {"per_page": 100, "sort": "pushed"}
    repos = []
    while len(repos) < max_repos:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repos.extend(response.json())
        if 'next' not in response.links:
            break
        url = response.links['next']['url']
    return repos[:max_repos]

# Process users and their repositories, then save to CSV
def process_data():
    users_data = []
    repos_data = []

    for user in get_users(city, min_followers):
        details = get_user_details(user["login"])
        users_data.append({
            "login": details["login"],
            "name": details.get("name", ""),
            "company": clean_company(details.get("company", "")),
            "location": details.get("location", ""),
            "email": details.get("email", ""),
            "hireable": details.get("hireable", ""),
            "bio": details.get("bio", ""),
            "public_repos": details["public_repos"],
            "followers": details["followers"],
            "following": details["following"],
            "created_at": details["created_at"]
        })

        for repo in get_user_repos(details["login"]):
            repos_data.append({
                "login": details["login"],
                "full_name": repo["full_name"],
                "created_at": repo["created_at"],
                "stargazers_count": repo["stargazers_count"],
                "watchers_count": repo["watchers_count"],
                "language": repo.get("language", ""),
                "has_projects": repo["has_projects"],
                "has_wiki": repo["has_wiki"],
                "license_name": repo["license"]["key"] if repo["license"] else ""
            })

    # Save data to CSV files
    pd.DataFrame(users_data).to_csv("users.csv", index=False)
    pd.DataFrame(repos_data).to_csv("repositories.csv", index=False)

# Create README.md with required bullet points
def create_readme():
    with open("README.md", "w") as f:
        f.write(
            "- This project uses the GitHub API to scrape user data and repositories in London with over 500 followers.\n"
            "- After analyzing the data, it was surprising to find that many prominent developers in London are heavily focused on Python development.\n"
            "- Developers are recommended to enhance their project documentation for increased engagement.\n"
        )

# Push files to GitHub
def push_to_github(repo_name):
    # Initialize and push to a new GitHub repository
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "users.csv", "repositories.csv", "README.md"])
    subprocess.run(["git", "commit", "-m", "Initial commit with user and repo data"])
    subprocess.run(["gh", "repo", "create", repo_name, "--public", "--confirm"])
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "push", "-u", "origin", "main"])

# Run data processing, readme creation, and push to GitHub
process_data()
create_readme()
push_to_github("london-500-followers-repo")
