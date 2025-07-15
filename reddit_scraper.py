print("Script started")

import praw
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get Reddit API credentials from .env
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username_env = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("USER_AGENT")

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username_env,
    password=password,
    user_agent=user_agent
)

# Test: Print your own username
print("Logged in as:", reddit.user.me())

def get_redditor_content(username, limit=10):
    redditor = reddit.redditor(username)
    posts = []
    comments = []

    for submission in redditor.submissions.new(limit=limit):
        posts.append({
            'title': submission.title,
            'selftext': submission.selftext
        })

    for comment in redditor.comments.new(limit=limit):
        comments.append(comment.body)

    return posts, comments

def save_user_data(username, posts, comments):
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    posts_path = f"data/{username}_posts.txt"
    comments_path = f"data/{username}_comments.txt"

    with open(posts_path, "w", encoding="utf-8") as f:
        f.write(f"Recent posts by {username}:\n\n")
        for post in posts:
            f.write(f"- {post['title']}\n")
            if post['selftext']:
                f.write(f"  {post['selftext']}\n\n")

    with open(comments_path, "w", encoding="utf-8") as f:
        f.write(f"Recent comments by {username}:\n\n")
        for comment in comments:
            f.write(f"- {comment.strip()[:250]}\n")

    print(f"✅ Posts saved to {posts_path}")
    print(f"✅ Comments saved to {comments_path}")

if __name__ == "__main__":
    usernames = ["kojied", "Hungry-Move-6603"]
    limit_per_user = 10

    for user in usernames:
        print(f"🔍 Fetching content for: {user}")
        posts, comments = get_redditor_content(user, limit=limit_per_user)
        save_user_data(user, posts, comments)
