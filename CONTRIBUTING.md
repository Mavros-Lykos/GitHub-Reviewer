# 🤝 Contributing to GitHub Reviewer

Thank you for your interest in contributing to GitHub Reviewer! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Pull Request Process](#pull-request-process)

## 🤗 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful** and inclusive of all contributors
- **Be constructive** in your feedback and criticism
- **Focus on what's best** for the community and project
- **Show empathy** towards other community members
- **No harassment, discrimination, or inappropriate behavior**

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account
- Basic knowledge of FastAPI and JavaScript
- Familiarity with AI/ML concepts (helpful but not required)

### First-Time Contributors

1. **Fork** the repository to your GitHub account
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GitHub-Reviewer.git
   cd GitHub-Reviewer
   ```
3. **Add upstream** remote:
   ```bash
   git remote add upstream https://github.com/Mavros-Lykos/GitHub-Reviewer.git
   ```

## 💻 Development Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # If available
```

### 2. Environment Variables

Create a `.env` file with your API keys:

```env
GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Verify Setup

```bash
# Run the application
uvicorn app:app --reload

# Test the health endpoint
curl http://localhost:8000/health
```

## 🔄 Contributing Process

### 1. Choose an Issue

- Browse [open issues](https://github.com/Mavros-Lykos/GitHub-Reviewer/issues)
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to express interest and get assigned

### 2. Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write clean, readable code
- Follow existing code patterns and style
- Add tests for new functionality
- Update documentation as needed

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: brief description of what you did"
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## 📝 Coding Standards

### Python Code Style

- Follow **PEP 8** conventions
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

#### Example:

```python
def fetch_repo_data(owner: str, repo: str) -> dict:
    """
    Fetch repository data from GitHub API.
    
    Args:
        owner: Repository owner username
        repo: Repository name
        
    Returns:
        Dictionary containing repo data including readme, files, and languages
        
    Raises:
        ValueError: If repository not found or API request fails
    """
    # Implementation here...
```

### JavaScript Code Style

- Use **ES6+** features where appropriate
- Follow **consistent naming conventions**
- Add **JSDoc comments** for functions
- Use **const/let** instead of var
- Keep functions pure when possible

#### Example:

```javascript
/**
 * Fetch AI review for a GitHub repository
 * @param {string} owner - Repository owner
 * @param {string} repo - Repository name  
 * @returns {Promise<Object>} Review data
 */
async function getRepoReview(owner, repo) {
    // Implementation here...
}
```

### CSS/Styling Guidelines

- Use **CSS custom properties** (variables) for consistency
- Follow **BEM methodology** for class naming
- Ensure **responsive design** principles
- Maintain **accessibility** standards

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run Python tests (if available)
python -m pytest tests/

# Run frontend tests (if available)  
npm test
```

### Writing Tests

- Write **unit tests** for new functions
- Include **integration tests** for API endpoints
- Test **error conditions** and edge cases
- Ensure **good test coverage**

### Test Structure

```python
import pytest
from main import fetch_repo_data

def test_fetch_repo_data_success():
    """Test successful repository data fetch."""
    # Arrange
    owner = "test-owner"
    repo = "test-repo"
    
    # Act
    result = fetch_repo_data(owner, repo)
    
    # Assert
    assert "readme" in result
    assert "files" in result
    assert "languages" in result
```

## 📚 Documentation

### Code Documentation

- **Docstrings**: All functions and classes should have clear docstrings
- **Type Hints**: Use type annotations for better code clarity
- **Comments**: Explain complex logic with inline comments

### README Updates

- Update README.md for new features
- Add examples for new functionality
- Update installation instructions if needed

### API Documentation

- FastAPI automatically generates API docs
- Ensure endpoint descriptions are clear
- Add example requests and responses

## 🐛 Reporting Issues

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check the latest version** to see if the issue still exists
3. **Gather relevant information** about your environment

### Issue Template

When creating an issue, include:

```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen

## Actual Behavior  
What actually happened

## Environment
- OS: [e.g., Windows 10, macOS 12.1]
- Python Version: [e.g., 3.9.7]
- Browser: [e.g., Chrome 95.0]

## Additional Context
Any other relevant information, screenshots, or logs
```

## 💡 Feature Requests

### Proposing New Features

1. **Check existing issues** for similar requests
2. **Open a discussion** before implementing large features
3. **Explain the use case** and benefit to users
4. **Consider implementation complexity**

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why would this feature be useful?

## Proposed Solution
How do you envision this working?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Any other relevant information or examples
```

## 🔍 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] New tests added (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Review Process

1. **Automated checks** must pass (if configured)
2. **Code review** by maintainers
3. **Address feedback** if requested
4. **Final approval** and merge

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `documentation` - Improvements to documentation
- `question` - Further information is requested
- `wontfix` - This will not be worked on

## 🎯 Priority Levels

- **High**: Security issues, critical bugs
- **Medium**: Feature requests, non-critical bugs
- **Low**: Nice-to-have improvements, minor issues

## 💬 Communication

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Code Reviews**: For feedback on implementations

### Response Times

- **Issues**: We aim to respond within 2-3 days
- **Pull Requests**: Initial review within 1 week
- **Security Issues**: Within 24 hours

## 🙏 Recognition

Contributors will be:

- **Listed** in the project's contributors section
- **Credited** in release notes for significant contributions
- **Invited** to become maintainers based on sustained contributions

## 📞 Questions?

If you have questions about contributing:

1. Check this document first
2. Search existing issues and discussions
3. Create a new discussion or issue
4. Tag maintainers if urgent

---

**Thank you for contributing to GitHub Reviewer! 🎉**

Your contributions help make this project better for everyone in the community.