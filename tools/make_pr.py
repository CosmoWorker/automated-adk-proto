from google.adk.tools import ToolContext
import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def commit_file_to_branch(
    owner: str,
    repo: str,
    branch_name: str,
    file_path: str,
    file_content: str,
    commit_message: str,
):
    """
    Creates a branch from base_branch and commits a file to it.
    """

    # 1. Get base branch SHA
    ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/main"
    ref_resp = requests.get(ref_url, headers=headers)
    ref_resp.raise_for_status()
    base_sha = ref_resp.json()["object"]["sha"]

    # 2. Create new branch
    branch_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    branch_data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": base_sha,
    }

    requests.post(branch_url, headers=headers, json=branch_data)

    # 3. Commit file
    content_encoded = base64.b64encode(file_content.encode()).decode()

    file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    commit_data = {
        "message": commit_message,
        "content": content_encoded,
        "branch": branch_name,
    }

    commit_resp = requests.put(file_url, headers=headers, json=commit_data)
    commit_resp.raise_for_status()

    return commit_resp.json()


def create_pr(
    owner: str,
    repo: str,
    pr_title: str,
    pr_body: str,
    head_branch: str,
):
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    data = {
        "title": pr_title,
        "body": pr_body,
        "head": head_branch,
        "base": "main",
    }

    pr_resp = requests.post(pr_url, headers=headers, json=data)
    pr_resp.raise_for_status()

    return pr_resp.json()
