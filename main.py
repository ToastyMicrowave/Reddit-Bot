import dotenv
import os
import json
from time import sleep
from praw import Reddit, reddit
dotenv.load_dotenv()


SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
USER_AGENT = os.getenv("USER_AGENT")

SUBREDDIT_JSON = os.path.abspath(r"./subs.json")

TITLE = '''something'''
URL = 'ofvalue.com'
COMMENT = """this is a placeholder"""


def post_to_sub(sub_name, reddit_instance, flair=None):
    subreddit = reddit.Subreddit(reddit_instance, display_name=sub_name)
    if subreddit.user_is_banned:
        remove_from_json(sub_name, True)
        print(f"User is banned in {sub_name}, moved to banned_in")
        return
    else:
        if flair is not None:
            flairs = list(subreddit.flair.link_templates.user_selectable())
            for flair_data in flairs:
                if flair_data["flair_text"].lower().startswith(flair):
                    flair_id = flair_data["flair_template_id"]
        else:
            flair_id = None
        submission = subreddit.submit(
            title=TITLE, url=URL, nsfw=False, flair_id=flair_id)
        return submission


def reply_to_post(submission=None):
    if submission is not None:
        submission.reply(COMMENT)


def remove_from_json(sub_name, move_to_banned, json_location=SUBREDDIT_JSON):
    with open(json_location, "r+", encoding="utf-8") as file:
        file_dict = json.loads(file.read())
        file.seek(0)
        flair = file_dict["working_subreddits"].pop(sub_name)
        if move_to_banned:
            file_dict["banned_in"][sub_name] = flair
        else:
            file_dict["banned_or_priv"][sub_name] = flair
        file.write(json.dumps(file_dict, indent=2))
        file.truncate()


if __name__ == '__main__':
    bot = Reddit(client_id=CLIENT_ID, client_secret=SECRET, username=USERNAME,
                password=PASSWORD, user_agent=USER_AGENT, ratelimit_seconds=120)

    with open(SUBREDDIT_JSON, encoding="utf-8") as file:
        subs = json.loads(file.read())["working_subreddits"]

    for sub in subs:
        try:
            post = post_to_sub(sub, bot, subs[sub])
            reply_to_post(post)
            print(f'Successfully posted to {sub}')
        except Exception as e:
            if "403" in str(e) or "404" in str(e):
                remove_from_json(sub, False)
                print(f"{sub} either banned or privated, adding to banned_or_priv")
            else:
                print(f"Sub: {sub}, Error: {e}")
            