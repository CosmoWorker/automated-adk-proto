import requests
import os
from dotenv import load_dotenv
import base64
import logging

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
github_token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def commit_file_to_branch(
    branch_name: str,
    file_path: str,
    file_content: str,
    commit_message: str,
):
    # Get base branch SHA
    ref_url = "https://api.github.com/repos/cosmoworker/automated-adk-proto/git/ref/heads/main"
    ref_resp = requests.get(ref_url, headers=headers)
    ref_resp.raise_for_status()
    base_sha = ref_resp.json()["object"]["sha"]

    branch_url = "https://api.github.com/repos/cosmoworker/automated-adk-proto/git/refs"
    branch_data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": base_sha,
    }
    logger.info("Creating a branch")
    requests.post(branch_url, headers=headers, json=branch_data)

    logger.info("Committing file")
    content_encoded = base64.b64encode(file_content.encode()).decode()

    file_url = f"https://api.github.com/repos/cosmoworker/automated-adk-proto/contents/{file_path}"

    commit_data = {
        "message": commit_message,
        "content": content_encoded,
        "branch": branch_name,
    }

    commit_resp = requests.put(file_url, headers=headers, json=commit_data)
    commit_resp.raise_for_status()

    return commit_resp.json()


def create_pr(
    pr_title: str,
    pr_body: str,
    head_branch: str,
):
    pr_url = "https://api.github.com/repos/cosmoworker/automated-adk-proto/pulls"

    data = {
        "title": pr_title,
        "body": pr_body,
        "head": head_branch,
        "base": "main",
    }

    pr_resp = requests.post(pr_url, headers=headers, json=data)
    pr_resp.raise_for_status()

    return pr_resp.json()


def post_pr(
    branch_name: str,
    filename: str,
    file_path: str,
    file_content: str,
    pr_title: str,
    pr_body: str,
    commit_message: str,
) -> str:
    '''
    Creates a new branch, commits the generated YAML file to the 'nursery/' directory, and opens a Pull Request.
    Refer the rules or examples for creating a filename.yml as per format.md file
    pr_body: short description in points what has been done. Provide references (with links) if found.
    '''
    file_path = filename if filename.startswith("nursery/") else f"nursery/{filename}"
    logger.info(f"file path: {file_path}, branch name: {branch_name}")
    try:
        commit_file_to_branch(branch_name, file_path, file_content, commit_message)

        pr_response = create_pr(pr_title, pr_body, branch_name)

        return f"Success! PR created at: {pr_response.get('html_url')}"
    except Exception as e:
        logger.error(f"Failure during PR creation. Error: {e}")
        return f"Failure during PR creation. Error: {e}"
