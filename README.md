# Reddit Multi-Sub Link Poster

A lightweight Python automation bot that posts a single **link + title** to multiple subreddits, optionally applying flairs and auto replying with a comment. Built using **PRAW** and **dotenv** for secure Reddit API access. 

---

# Features

* Multi-subreddit posting in one run
* Optional flair selection
* Automatic comment on each post
* Handles banned/private subs safely
* Configurable via `.env` + `subs.json`

---

# Setup

```bash
pip install praw python-dotenv
```

Create a `.env` (copy from `.env.example`):

```
CLIENT_ID=...
CLIENT_SECRET=...
USER=...
PASSWORD=...
USER_AGENT=...
```

Create `subs.json` (copy from `subs.example.json`):

```json
{
  "working_subreddits": { "subA": "flair", "subB": null },
  "banned_in": {},
  "banned_or_priv": {}
}
```

---

# Usage

Edit the constants in `main.py`:

```python
TITLE = "Your title"
URL = "https://your.link"
COMMENT = "Optional comment"
```

Then run:

```bash
python main.py
```

---
