import requests, json
from collections import defaultdict

username = input("Enter GitHub username: ")
url = f"https://api.github.com/users/{username}/events"

# Optionally: you can hardcode your GitHub token here
# so you don't have to input it every time.

# token = "ghp_your_personal_access_token_here"

# # (Be careful not to share or upload your token publicly!)
# If you use the hardwire token, comment the token input below.

token = input("Enter GitHub token (or enter for no token): ")

if token == "":
    response = requests.get(url)
else:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)


status_messages = {
    200: "✅ OK — The request succeeded.",
    201: "✅ Created — A new resource was successfully created.",
    202: "🕓 Accepted — The request has been accepted for processing.",
    204: "✅ No Content — The request succeeded, but there’s no data to return.",

    304: "🗂️ Not Modified — The data hasn’t changed since your last request (ETag matched).",

    400: "⚠️ Bad Request — The request was malformed or missing parameters.",
    401: "🔒 Unauthorized — Missing or invalid authentication token.",
    403: "🚫 Forbidden — You don’t have permission, or you’ve hit a rate limit.",
    404: "❓ Not Found — The resource or user doesn’t exist.",
    409: "⚠️ Conflict — There’s a conflict (like duplicate data).",
    422: "⚠️ Unprocessable Entity — The request was well-formed but had semantic errors.",

    429: "⏳ Too Many Requests — You’re being rate-limited. Try again later.",

    500: "💥 Internal Server Error — GitHub’s servers had a problem.",
    502: "💥 Bad Gateway — Invalid response from an upstream server.",
    503: "🧰 Service Unavailable — GitHub is down for maintenance or overloaded.",
    504: "🕒 Gateway Timeout — GitHub didn’t respond in time.",
}
print(status_messages[response.status_code])
if response.status_code == 200:
    data = response.json()
    result = defaultdict(lambda: defaultdict(int))

    for event in data:
        repo = event.get("repo", {}).get("name")
        event_type = event.get("type")
        if repo and event_type:
            result[repo][event_type] += 1

    # convert back to normal dict for JSON serialization
    output = {repo: dict(types) for repo, types in result.items()}

    event_messages = {
        "PushEvent": "Pushed {count} commit(s) to {repo}.",
        "PullRequestEvent": "Opened or updated {count} pull request(s) in {repo}.",
        "IssuesEvent": "Created or modified {count} issue(s) in {repo}.",
        "IssueCommentEvent": "Commented {count} time(s) on issues in {repo}.",
        "WatchEvent": "Starred {repo} {count} time(s).",
        "ForkEvent": "Forked {repo} {count} time(s).",
        "CreateEvent": "Created something new {count} time(s) in {repo} (branch, tag, or repo).",
        "DeleteEvent": "Deleted something {count} time(s) in {repo}.",
        "ReleaseEvent": "Published {count} release(s) in {repo}.",
        "MemberEvent": "Modified members {count} time(s) in {repo}.",
        "PublicEvent": "Made {repo} public {count} time(s).",
        "PullRequestReviewEvent": "Reviewed {count} pull request(s) in {repo}.",
        "PullRequestReviewCommentEvent": "Commented {count} time(s) on PR reviews in {repo}.",
        "CommitCommentEvent": "Commented {count} time(s) on commits in {repo}.",
        "GollumEvent": "Edited the wiki {count} time(s) in {repo}.",
    }

    for repo in output:
        for event_type in output[repo]:
            print(event_messages.get(event_type, "Did {count} {event_type}(s) in {repo}").format(repo=repo, count=output[repo].get(event_type), event_type=event_type))


