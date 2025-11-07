import os
import base64
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # loads .env locally
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN missing")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing")

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_repo_data(owner, repo):
    # README
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    readme_resp = requests.get(readme_url, headers=headers)
    if readme_resp.status_code == 200:
        r_json = readme_resp.json()
        if r_json.get("encoding") == "base64":
            try:
                readme_text = base64.b64decode(r_json["content"]).decode("utf-8", errors="ignore")
            except Exception:
                readme_text = ""
        else:
            readme_text = r_json.get("content", "")
    else:
        readme_text = ""

    # Contents
    contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    contents_resp = requests.get(contents_url, headers=headers)
    if contents_resp.status_code == 200:
        files = [item.get("name", "") for item in contents_resp.json() if isinstance(item, dict)]
    else:
        files = []

    # Languages
    languages_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    lang_resp = requests.get(languages_url, headers=headers)
    languages = lang_resp.json() if lang_resp.status_code == 200 else {}

    return {
        "readme": readme_text,
        "files": files,
        "languages": languages
    }


def generate_review(repo_data):
    """Generate a review using the Gemini API."""
    prompt = (
        "You are a senior software architect. "
        "Analyze the following GitHub repository data and provide a 3-point review "
        "covering quality, complexity, and maintainability:\n\n"
        f"README: {repo_data['readme'][:5000]}\n\n"
        f"Files: {', '.join(repo_data['files'][:20])}\n\n"
        f"Languages: {repo_data['languages']}\n"
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    return response.text if hasattr(response, 'text') else str(response)


if __name__ == "__main__":
    owner = "pallets"
    repo = "flask"

    repo_data = fetch_repo_data(owner, repo)
    review = generate_review(repo_data)
    print("GitHub Reviewer Output:\n", review)
