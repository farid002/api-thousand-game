"""Tbd"""

import os

from github import Github

# Extract issue number from branch name
branch_name = os.getenv("GITHUB_REF")

# Assuming branch name convention is <type>/<issue_number>/<short_desc>
issue_label = branch_name.split("/")[-3]
issue_number = branch_name.split("/")[-2]
short_desc = branch_name.split("/")[-1]

# Initialize PyGithub client
github_token = os.getenv("GITHUB_TOKEN")
g = Github(github_token)

# Get repository
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
print(issue_number)
# Get issue
issue = repo.get_issue(int(issue_number))

# Add comment to issue with a link to the branch
branch_url = f"{repo.html_url}/tree/{branch_name}"
# issue.create_comment(f"This branch is automatically linked to issue [{issue.title}]({branch_url}).")
issue.add_to_labels(issue_label)
