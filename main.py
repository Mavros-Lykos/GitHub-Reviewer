import os
import base64
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
        for repo in sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:5]:
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
    try:
        prompt = (
            "You are a technical recruiter and GitHub analyst.\n"
            "Review the following GitHub user's profile and top repositories. Summarize their main programming focus,\n"
            "strengths, and potential areas for improvement.\n\n"
            "Profile:\n"
            f"Name: {user_data['profile']['name']}\n"
            f"Bio: {user_data['profile']['bio']}\n"
            f"Location: {user_data['profile']['location']}\n"
            f"Followers: {user_data['profile']['followers']}\n"
            f"Following: {user_data['profile']['following']}\n\n"
            "Top Repos:\n"
        )
        
        for repo in user_data['top_repos']:
            prompt += (
                f"- {repo['name']} (Stars: {repo['stars']}, Forks: {repo['forks']})\n"
                f"  Description: {repo['description']}\n"
            )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        review_text = response.text if hasattr(response, 'text') else str(response)
        logger.info("Successfully generated user review")
        return review_text
    except Exception as e:
        logger.error(f"Failed to generate user review: {str(e)}")
        raise RuntimeError(f"Failed to generate review: {str(e)}")
        
if __name__ == "__main__":
    #owner = "pallets"
    #repo = "flask "
    thisRepoOwner = "Mavros-Lykos"

    #repo_data = fetch_repo_data(owner, repo)
    #review = generate_repo_review(repo_data)
    user_data = fetch_user_data(thisRepoOwner)
    UserReview = generate_user_review(user_data)
    print("GitHub Reviewer Output:\n", UserReview)
