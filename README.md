# 🐙 GitHub Activity CLI (events → human summary)

A tiny Python CLI that:
1) Fetches a user’s recent GitHub events from  
   `https://api.github.com/users/<username>/events`
2) Prints a clear **status message** for the HTTP response
3) Summarizes the returned events by **repository** and **event type**
4) Outputs human-readable lines like  
   `Pushed 3 commit(s) to octocat/Hello-World.`

---

## ✨ What this script does

- Prompts for **GitHub username**
- Prompts for a **GitHub token** (press Enter to skip)
- Optionally there is a possibility to hardcode the token into activity.py 
- Calls the Events API (unauthenticated or with `Bearer <token>`)
- Maps HTTP **status codes** to friendly messages (e.g., `200 OK`, `403 Forbidden`)
- Aggregates events into `{repo: {event_type: count}}`
- Prints a readable sentence per repo & event type using templates (e.g., `PushEvent`, `WatchEvent`, …)

> Note: The Events API returns the most recent public events (up to 30 by default).  
> This script does **not** paginate or write files — it just summarizes what’s returned.

---

## 📦 Requirements

- Python 3.8+
- Dependency:
  ```bash
  pip install requests
  ```

---

## ▶️ How to run

Save your code as `activity.py` and run:

```bash
python activity.py
```

You’ll see prompts like:

```
Enter GitHub username: octocat
Enter GitHub token (or enter for no token):
```

- Provide a **Personal Access Token (PAT)** for higher rate limits (optional).
- Press **Enter** to skip the token (limited to 60 requests/hour).

---

## 🧪 Example output

```
✅ OK — The request succeeded.
Pushed 3 commit(s) to octocat/Hello-World.
Created or modified 1 issue(s) in octocat/Hello-World.
Starred octocat/Spoon-Knife 2 time(s).
```

If something goes wrong, you’ll get a friendly message, e.g.:

- `🔒 Unauthorized — Missing or invalid authentication token.` (401)  
- `🚫 Forbidden — You don’t have permission, or you’ve hit a rate limit.` (403)  
- `❓ Not Found — The resource or user doesn’t exist.` (404)

---

## 🔐 Tokens & rate limits

- **Unauthenticated**: ~60 requests/hour (per IP)
- **Authenticated** (with PAT): up to ~5,000 requests/hour

Create a token at: GitHub → Settings → Developer settings → **Personal access tokens (classic)**.  
Give it a name and, for public activity, minimal scopes (e.g., `public_repo`).

Paste it into the prompt when asked.

---

## 🧠 How the summary works

- The script loops over each event in the JSON response.
- It counts occurrences by **repo** and **event type** using:
  ```python
  result = defaultdict(lambda: defaultdict(int))
  ```
- It then prints a line per `(repo, event_type)` using this mapping:
  - `PushEvent` → `Pushed {count} commit(s) to {repo}.`
  - `PullRequestEvent` → `Opened or updated {count} pull request(s) in {repo}.`
  - `IssuesEvent` → `Created or modified {count} issue(s) in {repo}.`
  - …and more (fallback: `Did {count} {event_type}(s) in {repo}`)

---

## 🚧 Limitations

- **No pagination**: only summarizes the first page of events returned by the API.
- **Public events only**: private actions aren’t included by this endpoint.
- **No per-file breakdown**: possible for `PushEvent` with extra requests to each commit URL.

## Acknowledgment 

This project was build according to https://roadmap.sh/projects/github-user-activity specifications

