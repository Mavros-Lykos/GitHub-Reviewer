# 🚀 GitHub Reviewer

An AI-powered web application that provides intelligent reviews and analysis of GitHub repositories and user profiles using Google's Gemini AI model.

![GitHub Reviewer Banner](https://via.placeholder.com/800x200/0d6efd/ffffff?text=GitHub+Reviewer+🤖)

## 📸 Screenshots

### Repository Review Interface
![Repository Review](https://via.placeholder.com/800x500/f8f9fa/212529?text=Repository+Review+Interface)

### User Profile Analysis
![User Analysis](https://via.placeholder.com/800x500/f8f9fa/212529?text=User+Profile+Analysis)

### AI-Generated Review Output
![Review Output](https://via.placeholder.com/800x400/ffffff/0d6efd?text=AI+Review+Output+with+Markdown+Support)

## 🎯 Features

- 🔍 **Repository Analysis**: Get comprehensive AI reviews of any public GitHub repository
- 👤 **User Profile Reviews**: Analyze GitHub user profiles and their top repositories  
- 🤖 **AI-Powered**: Leverages Google Gemini AI for intelligent code analysis
- 🎨 **Modern UI**: Clean, responsive web interface with toggle between HTML and Markdown views
- 📋 **Export Options**: Copy reviews to clipboard or download as files
- ⚡ **Fast API**: Built with FastAPI for high performance
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Project Structure

```
github-reviewer/
├── app.py                 # FastAPI application server
├── main.py               # Core logic for GitHub API integration and AI reviews
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create your own)
├── .gitignore           # Git ignore rules
├── policies..txt        # AI review policies/guidelines
├── frontend/
│   ├── index.html       # Main web interface
│   ├── script.js        # Frontend JavaScript logic
│   └── style.css        # Styling and responsive design
└── venv/                # Virtual environment (auto-generated)
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Core programming language
- **Google Gemini AI** - AI model for generating reviews
- **GitHub API** - Fetching repository and user data
- **Uvicorn** - ASGI server for running the application

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript** - Interactive functionality
- **Marked.js** - Markdown rendering support

### APIs & Services
- **GitHub REST API** - Repository and user data
- **Google Gemini API** - AI-powered content generation

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub Personal Access Token
- A Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/Mavros-Lykos/GitHub-Reviewer.git
cd GitHub-Reviewer
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
GITHUB_TOKEN=your_github_personal_access_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application

```bash
# Development mode with auto-reload
uvicorn app:app --reload

# Or run directly
python app.py
```

The application will be available at `http://localhost:8000`

## 🔑 Getting Your API Keys

### GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "GitHub Reviewer App"
4. Select the following scopes:
   - `public_repo` - Access public repositories
   - `read:user` - Read user profile data
5. Click "Generate token"
6. Copy the token immediately (you won't be able to see it again)

### Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Make sure you have access to the Gemini API (may require verification)

## 💻 Local Development

### Running in Development Mode

```bash
# Start the server with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

- `GET /` - Main web interface
- `GET /review/repo/{owner}/{repo}` - Get AI review for a repository
- `GET /review/user/{username}` - Get AI review for a user profile  
- `GET /health` - Health check endpoint
- `GET /static/*` - Static file serving

### Testing the API

You can test the API endpoints directly:

```bash
# Test repository review
curl http://localhost:8000/review/repo/pallets/flask

# Test user review  
curl http://localhost:8000/review/user/torvalds

# Health check
curl http://localhost:8000/health
```

## 📝 Usage Examples

### Repository Review
Navigate to the application and enter:
- **Owner**: `microsoft`
- **Repository**: `vscode`

The AI will analyze the repository structure, code quality, documentation, and provide comprehensive insights.

### User Profile Review
Enter a GitHub username like:
- **Username**: `gaearon`

The AI will review the user's profile, contribution patterns, and top repositories.

## 🐛 Troubleshooting

### Common Issues

**"GITHUB_TOKEN missing" Error**
- Ensure your `.env` file exists and contains a valid GitHub token
- Check that the token has the correct permissions

**"Failed to initialize Gemini client" Error**
- Verify your Gemini API key is correct
- Ensure you have access to the Gemini API

**Repository/User Not Found**
- Check that the repository/user is public
- Verify the owner/repo name spelling
- Ensure your GitHub token has appropriate permissions

**Port Already in Use**
- Change the port: `uvicorn app:app --reload --port 8001`
- Or kill the process using port 8000

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code style
- Add docstrings for new functions
- Keep commits atomic and well-described
- Update documentation for new features
- Test your changes locally before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini** for providing the AI capabilities
- **GitHub API** for repository and user data access
- **FastAPI** community for the excellent framework
- **Inter Font** for the beautiful typography

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Mavros-Lykos/GitHub-Reviewer/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your environment and the issue

## 🚀 Future Roadmap

- [ ] Add support for private repositories
- [ ] Implement caching for faster repeated reviews
- [ ] Add more detailed code quality metrics
- [ ] Support for other AI models (OpenAI, Claude, etc.)
- [ ] Docker containerization
- [ ] Batch processing for multiple repositories
- [ ] Integration with GitHub webhooks
- [ ] Custom review templates and criteria

---

**Made with ❤️ by the GitHub Reviewer team**