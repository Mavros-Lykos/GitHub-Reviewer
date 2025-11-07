from fastapi import FastAPI
from main import fetch_repo_data, generate_review  # Assuming your functions are in main.py
import uvicorn

app = FastAPI(
    title="Github Reviewer API",
    description="Uses Gemini to review GitHub repos and users."
)

@app.get("/review/repo/{owner}/{repo}", tags=["Reviews"])
async def review_repository(owner: str, repo: str):
    """
    Generates an AI-powered review for a specific GitHub repository.
    """
    try:
        # We can 'await' our functions if we make them async,
        # but for simplicity, FastAPI is smart enough to run
        # normal sync functions (like ours) in a separate thread pool.
        repo_data = fetch_repo_data(owner, repo)
        review_text = generate_review(repo_data)
        return {"review": review_text}
    except Exception as e:
        return {"error": str(e)}, 404

# This block allows us to run the app directly for testing
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)