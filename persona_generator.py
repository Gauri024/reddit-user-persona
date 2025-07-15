import os
from dotenv import load_dotenv
import cohere

# Load API key from .env
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("❌ COHERE_API_KEY not found in .env")

co = cohere.Client(api_key)

def load_text(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()

def build_prompt(posts, comments, username="UnknownUser"):
    return f"""
You are a research assistant generating a detailed user persona for the Reddit user **{username}** based on the posts and comments provided.

For each characteristic, provide:
- The characteristic description
- Cite the posts or comments (direct quotes or paraphrases) that support this trait.

Structure your output with clear bullet points or short paragraphs.

Posts:
{posts}

Comments:
{comments}
"""

def generate_persona_with_cohere(prompt):
    try:
        response = co.chat(
            message=prompt,
            model="command-light",
            temperature=0.7,
            max_tokens=700  # increased for detail and citations
        )
        return response.text.strip()
    except Exception as e:
        print("❌ Cohere API error:", e)
        return ""

def save_persona(username, persona_text):
    os.makedirs("output", exist_ok=True)
    filename = f"output/{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Persona for {username} saved to {filename}")

if __name__ == "__main__":
    # For demonstration, let's assume posts/comments files per user:
    user_data = {
        "kojied": {
            "posts_file": "data/kojied_posts.txt",
            "comments_file": "data/kojied_comments.txt",
        },
        "Hungry-Move-6603": {
           "posts_file": "data/Hungry-Move-6603_posts.txt",
            "comments_file": "data/Hungry-Move-6603_comments.txt",
        }
    }

    for username, files in user_data.items():
        posts = load_text(files["posts_file"])
        comments = load_text(files["comments_file"])

        if not posts or not comments:
            print(f"❌ Missing data for {username}, skipping.")
            continue

        print(f"🧠 Generating persona for user: {username} ...")
        prompt = build_prompt(posts, comments, username)
        persona = generate_persona_with_cohere(prompt)

        print(f"\n===== 🧾 Generated User Persona for {username} (Cohere) =====\n")
        print(persona)

        save_persona(username, persona)
