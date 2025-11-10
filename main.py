import os
import base64
import time
import requests
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # loads .env locally
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN missing")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing")

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Initialize Gemini client
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("Gemini client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {str(e)}")
    raise RuntimeError(f"Failed to initialize Gemini client: {str(e)}")

def fetch_repo_data(owner, repo):
    """Fetch repository data from GitHub API.
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        Dictionary with readme, files, and languages
        
    Raises:
        ValueError: If repository not found or API request fails
    """
    try:
        # README
        readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        readme_resp = requests.get(readme_url, headers=headers, timeout=10)
        if readme_resp.status_code == 200:
            r_json = readme_resp.json()
            if r_json.get("encoding") == "base64":
                try:
                    readme_text = base64.b64decode(r_json["content"]).decode("utf-8", errors="ignore")
                except Exception as e:
                    logger.warning(f"Failed to decode README: {str(e)}")
                    readme_text = ""
            else:
                readme_text = r_json.get("content", "")
        else:
            readme_text = ""

        # Contents
        contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        contents_resp = requests.get(contents_url, headers=headers, timeout=10)
        if contents_resp.status_code == 200:
            files = [item.get("name", "") for item in contents_resp.json() if isinstance(item, dict)]
        else:
            files = []

        # Languages
        languages_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
        lang_resp = requests.get(languages_url, headers=headers, timeout=10)
        languages = lang_resp.json() if lang_resp.status_code == 200 else {}

        logger.info(f"Successfully fetched data for {owner}/{repo}")
        return {
            "readme": readme_text,
            "files": files,
            "languages": languages
        }
    except requests.exceptions.Timeout:
        raise ValueError(f"Request timeout while fetching {owner}/{repo}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch repository data: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error fetching repo data: {str(e)}")
        raise ValueError(f"Unexpected error: {str(e)}")


def generate_repo_review(repo_data):
    """Generate a repo review using the Gemini API.
    
    Args:
        repo_data: Dictionary containing readme, files, and languages
        
    Returns:
        Review text from Gemini
        
    Raises:
        RuntimeError: If API call fails
    """
    try:
        prompt = (
            "You are a **senior software architect** and code quality reviewer. "
            "Analyze the following GitHub repository and produce a concise, structured review "
            "focusing on **quality, complexity, and maintainability**. "
            "Use evidence from the README, files, and languages provided.\n\n"
            "Answer below 300 words use markdown, integrate emojis so that viewer wont be bored"
            
            "### Instructions:\n"
            "- Provide a clear, professional assessment.\n"
            "- Limit the review to 3 main points: Quality, Complexity, Maintainability.\n"
            "- Be objective and evidence-based; do not speculate beyond the provided data.\n"
            "- Suggest **concrete improvements** if any weaknesses are identified.\n\n"
            
            "### Repository Data:\n"
            f"- README (first 5000 chars):\n{repo_data['readme'][:5000]}\n\n"
            f"- Top Files (up to 20): {', '.join(repo_data['files'][:20])}\n"
            f"- Languages: {', '.join(repo_data['languages']) if isinstance(repo_data['languages'], list) else repo_data['languages']}\n"
            
            "### Output Format (Markdown, strict):\n"
            "1. **Quality** – Describe code readability, documentation, and adherence to best practices.\n"
            "2. **Complexity** – Evaluate code structure, modularity, and algorithmic sophistication.\n"
            "3. **Maintainability** – Comment on ease of updates, testing, and potential technical debt.\n"
            "Include **1–2 actionable recommendations** to improve the repository in each category.\n"
        )

        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        review_text = response.text if hasattr(response, 'text') else str(response)
        logger.info("Successfully generated repo review")
        return review_text
    except Exception as e:
        logger.error(f"Failed to generate repo review: {str(e)}")
        raise RuntimeError(f"Failed to generate review: {str(e)}")


def fetch_user_data(username: str):
    """Fetch GitHub user data and top repositories.
    
    Args:
        username: GitHub username
        
    Returns:
        Dictionary with profile and top_repos
        
    Raises:
        ValueError: If user not found or API request fails
    """
    try:
        # Basic profile
        user_url = f"https://api.github.com/users/{username}"
        user_resp = requests.get(user_url, headers=headers, timeout=10)
        if user_resp.status_code != 200:
            raise ValueError(f"User {username} not found")
        user_info = user_resp.json()

        # Public repos
        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_resp = requests.get(repos_url, headers=headers, timeout=10)
        if repos_resp.status_code != 200:
            raise ValueError(f"Failed to fetch repositories for {username}")
        repos = repos_resp.json()

        # Collect top repos info
        top_repos = []
        for repo in sorted(repos, key=lambda x: x["stargazers_count"], reverse=True):
            top_repos.append({
                "name": repo["name"],
                "description": repo["description"],
                "languages_url": repo["languages_url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"]
            })

        logger.info(f"Successfully fetched data for user {username}")
        return {
            "profile": {
                "name": user_info.get("name"),
                "bio": user_info.get("bio"),
                "location": user_info.get("location"),
                "followers": user_info.get("followers"),
                "following": user_info.get("following")
            },
            "top_repos": top_repos
        }
    except requests.exceptions.Timeout:
        raise ValueError(f"Request timeout while fetching user {username}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch user data: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error fetching user data: {str(e)}")
        raise ValueError(f"Unexpected error: {str(e)}")

def generate_user_review(user_data):
    """Generate a user review using the Gemini API.
    
    Args:
        user_data: Dictionary with profile and top_repos
        
    Returns:
        Review text from Gemini
        
    Raises:
        RuntimeError: If API call fails
    """
    model_primary = "gemini-2.5-flash"
    model_fallback = "gemini-2.5-flash-lite"
    max_retries = 5

    # Build repos section separately to avoid nested f-strings with escapes
    repos = user_data.get('top_repos', [])
    if repos:
        repo_lines = []
        for repo in repos:
            name = repo.get('name', 'N/A')
            stars = repo.get('stars', 0)
            forks = repo.get('forks', 0)
            desc = repo.get('description', 'No description')
            repo_lines.append(f"- **{name}** (Stars: {stars}, Forks: {forks})\n  Description: {desc}")
        repos_section = "\n".join(repo_lines)
    else:
        repos_section = "- No repositories found."

    prompt = (
        
        "You are an **experienced senior technical recruiter and GitHub talent analyst**.  "
        "Your goal is to evaluate the following GitHub developer profile and top repositories "
        "to produce a **career-oriented technical assessment**.\n\n"

        "### 🎯 **Your Objectives**\n"
        "Based only on the provided GitHub data:\n"
        "1. Determine the developer’s **main technical areas** (languages, frameworks, or focus domains).  \n"
        "2. Rate their **demonstrated coding expertise** on a **scale of 1–10**, where:\n"
        "   - 1–3 = Beginner (limited visible work)\n"
        "   - 4–6 = Intermediate (functional but limited complexity)\n"
        "   - 7–8 = Advanced (consistent, strong technical signal)\n"
        "   - 9–10 = Expert (exceptional, high-impact open-source or complex contributions)\n"
        "3. Recommend a **suitable job position or career level** (e.g., “Junior Backend Developer”, “Full-Stack Engineer”, “Data Science Intern”, “Senior DevOps Engineer”).\n"
        "4. Provide **actionable feedback** on how they could enhance their skills or portfolio to reach the *next career level*.\n\n"

        "### 🧩 **Output Format (Strict)**\n"
        "Produce your response in the following markdown sections:\n\n"
        "#### 🧠 Technical Focus\n"
        "Summarize the developer’s core languages, tools, and interests.\n\n"
        "#### 💪 Expertise Assessment (1–10)\n"
        "Provide a 1–10 rating of overall GitHub coding expertise, with a one-line proper justification.\n\n"
        "#### 💼 Suitable Role\n"
        "Suggest one or two realistic job positions or career directions that match the profile.\n\n"
        "#### 🚀 Growth Recommendations\n"
        "Write 2–3 short bullet points with **specific next steps** for improving technical or professional standing.\n\n"

        "### ⚙️ **Tone and Constraints**\n"
        "- Be concise, objective, and professional — like a real recruiter’s feedback summary.\n"
        "- Do **not guess**; if key info is missing, acknowledge it.\n"
        "- Limit the entire output to **under 450 words**.\n"
        "- Use **neutral, evidence-based** language — avoid exaggeration or flattery.\n"
        "- Focus on *visible signals of skill* (e.g., repo activity, stars, clarity, diversity).\n\n"

        "### 👤 **Profile Information**\n"
        f"- Name: {user_data['profile'].get('name', 'N/A')}\n"
        f"- Bio: {user_data['profile'].get('bio', 'N/A')}\n"
        f"- Location: {user_data['profile'].get('location', 'N/A')}\n"
        f"- Followers: {user_data['profile'].get('followers', 0)}\n"
        f"- Following: {user_data['profile'].get('following', 0)}\n\n"

        "### 📦 **Top Repositories**\n"
        + "".join([
            f"- **{repo['name']}** (⭐ {repo.get('stars', 0)}, 🍴 {repo.get('forks', 0)})\n"
            f"  Description: {repo.get('description', 'No description')}\n"
            for repo in user_data.get('top_repos', [])
        ]) or "- No repositories found.\n"

    )
    

    for attempt in range(max_retries):
        model_to_use = model_primary if attempt == 0 else model_fallback
        try:
            response = client.models.generate_content(
                model=model_to_use,
                contents=prompt,
            )
            review_text = getattr(response, 'text', str(response))
            logger.info("Successfully generated user review")
            return review_text
        except Exception as e:
            err_str = str(e)
            # Treat 503 or overload messages as transient and retry with backoff
            if '503' in err_str or 'overload' in err_str.lower():
                wait_time = 2 ** attempt
                logger.warning(f"Model overloaded or service busy. Retrying in {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Failed to generate user review: {err_str}")
                raise RuntimeError(f"Failed to generate review: {err_str}")

    logger.error("All retries failed. Could not generate user review.")
    return "⚠️ Unable to generate review at this time."
        
if __name__ == "__main__":
    #owner = "pallets"
    #repo = "flask "
    thisRepoOwner = "Mavros-Lykos"

    #repo_data = fetch_repo_data(owner, repo)
    #review = generate_repo_review(repo_data)
    user_data = fetch_user_data(thisRepoOwner)
    UserReview = generate_user_review(user_data)
    print("GitHub Reviewer Output:\n", UserReview)
