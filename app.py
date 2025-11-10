from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging
from main import fetch_repo_data, generate_repo_review, fetch_user_data, generate_user_review
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


frontend_dir = "frontend"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitHub Reviewer API",
    description="Uses Gemini to review GitHub repos and users."
)

@app.get("/review/repo/{owner}/{repo}", tags=["Reviews"])
async def review_repository(owner: str, repo: str):
    """
    Generates an AI-powered review for a specific GitHub repository.
    
    Args:
        owner: GitHub repository owner
        repo: GitHub repository name
        
    Returns:
        JSON with review text
    """
    try:
        if not owner or not repo:
            raise ValueError("Owner and repo cannot be empty")
        
        logger.info(f"Fetching review for repo: {owner}/{repo}")
        repo_data = fetch_repo_data(owner, repo)
        
        if not repo_data.get('readme') and not repo_data.get('files'):
            raise ValueError(f"Repository {owner}/{repo} not found or is empty")
        
        review_text = generate_repo_review(repo_data)
        return {
            "owner": owner,
            "repo": repo,
            "review": review_text
        }
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error reviewing repo {owner}/{repo}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Failed to review repository: {str(e)}")

@app.get("/review/user/{username}", tags=["Reviews"])
async def review_user(username: str):
    """
    Generates an AI-powered review for a GitHub user profile and top repositories.
    
    Args:
        username: GitHub username
        
    Returns:
        JSON with review text
    """
    try:
        if not username:
            raise ValueError("Username cannot be empty")
        
        logger.info(f"Fetching review for user: {username}")
        user_data = fetch_user_data(username)
        
        if not user_data.get('top_repos'):
            raise ValueError(f"User {username} has no public repositories")
        
        review_text = generate_user_review(user_data)
        return {
            "username": username,
            "review": review_text
        }
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error reviewing user {username}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Failed to review user: {str(e)}")

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Serve index.html on root
@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)

# This block allows us to run the app directly for testing
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)