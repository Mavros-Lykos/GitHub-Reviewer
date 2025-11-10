// Global variables to store the raw Markdown content
let repoMarkdown = "";
let userMarkdown = "";

/**
 * MOCK DATA - Represents a 1-second API call for a repo review.
 * Replace this with your actual fetch call.
 */
async function getRepoReview() {
    const owner = document.getElementById("owner").value.trim();
    const repo = document.getElementById("repo").value.trim();
    const output = document.getElementById("repo-output");

    if (!owner || !repo) {
        output.innerHTML = '<p class="placeholder-error">Please enter both owner and repo.</p>';
        return;
    }

    // Show loading state (using the placeholder style)
    output.innerHTML = `<div class="placeholder">
        <svg class="loading-spinner" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="2" x2="12" y2="6"></line>
            <line x1="12" y1="18" x2="12" y2="22"></line>
            <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
            <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
            <line x1="2" y1="12" x2="6" y2="12"></line>
            <line x1="18" y1="12" x2="22" y2="12"></line>
            <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
            <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
        </svg>
        <p>Generating AI review for <strong>${owner}/${repo}</strong>...</p>
    </div>`;

    // --- MOCK DATA SIMULATION ---
    // Remove this setTimeout and uncomment your 'fetch' block for production
/*     setTimeout(() => {
        repoMarkdown = `## 🚀 AI Review: ${owner}/${repo}\n\nThis is a *mocked* AI-powered review. The real review would provide a deep analysis of the repository.\n\n### 1. Project Structure\n* **Clarity:** The structure is clean.\n* **Configuration:** ` + '`package.json`' + ` (or equivalent) seems well-configured.\n\n### 2. Code Quality\n- **Readability:** High.\n- **Best Practices:** Appears to follow modern standards.\n\n### 3. Documentation\nA good **README.md** is present, which is excellent for new contributors.\n\n> **Overall:** This project shows great promise. Keep up the good work!`;
        
        // Render the content based on the toggle's current state
        toggleView('repo');
    }, 1500); // Simulate a 1.5-second network request */

    
    // --- YOUR ORIGINAL FETCH CODE (UNCOMMENT FOR PRODUCTION) ---
    try {
        const res = await fetch(`/review/repo/${owner}/${repo}`);
        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }
        const data = await res.json();

        repoMarkdown = data.review || data.detail || "No review available.";
        toggleView('repo'); // Render based on toggle state
    } catch (err) {
        output.innerHTML = `<p class="placeholder-error">Error fetching review: ${err.message}</p>`;
    }
   
}

/**
 * MOCK DATA - Represents a 1-second API call for a user review.
 * Replace this with your actual fetch call.
 */
async function getUserReview() {
    const username = document.getElementById("username").value.trim();
    const output = document.getElementById("user-output");

    if (!username) {
        output.innerHTML = '<p class="placeholder-error">Please enter a username.</p>';
        return;
    }

    // Show loading state
    output.innerHTML = `<div class="placeholder">
        <svg class="loading-spinner" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="2" x2="12" y2="6"></line>
            <line x1="12" y1="18" x2="12" y2="22"></line>
            <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
            <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
            <line x1="2" y1="12" x2="6" y2="12"></line>
            <line x1="18" y1="12" x2="22" y2="12"></line>
            <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
            <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
        </svg>
        <p>Generating AI review for <strong>${username}</strong>...</p>
    </div>`;

   /*  // --- MOCK DATA SIMULATION ---
    setTimeout(() => {
        userMarkdown = `# 👤 AI Review: ${username}\n\nThis is a *mocked* review of the user's GitHub activity.\n\n### Activity Highlights\n- **Primary Languages:** JavaScript, Python\n- **Contribution Streak:** 42 days (Mock Data)\n- **Top Repos:** 'project-a', 'awesome-tool', 'config-files'\n\n### Summary\nThis user appears to be a consistent contributor with a focus on web technologies. Their activity demonstrates a strong commitment to open source.`;
        
        // Render the content
        toggleView('user');
    }, 1500); */

    
    // --- YOUR ORIGINAL FETCH CODE (UNCOMMENT FOR PRODUCTION) ---
    try {
        const res = await fetch(`/review/user/${username}`);
        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }
        const data = await res.json();

        userMarkdown = data.review || data.detail || "No review available.";
        toggleView('user'); // Render based on toggle state
    } catch (err) {
        output.innerHTML = `<p class="placeholder-error">Error fetching review: ${err.message}</p>`;
    }
    
}

/**
 * Toggles the view between raw Markdown and rendered HTML.
 */
function toggleView(type) {
    let output, markdown, toggle;

    if (type === 'repo') {
        output = document.getElementById("repo-output");
        markdown = repoMarkdown;
        toggle = document.getElementById("repo-toggle");
    } else {
        output = document.getElementById("user-output");
        markdown = userMarkdown;
        toggle = document.getElementById("user-toggle");
    }

    if (!markdown) {
        // If there's no content, just return. The placeholder is already shown.
        // Or, reset to the initial placeholder.
        output.innerHTML = `<div class="placeholder">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 16c-3.87 0-7 3.13-7 7M12 16c3.87 0 7 3.13 7 7m-7-7v-2m0-4c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"></path>
                <path d="M12 12c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"></path>
            </svg>
            <p>Your AI-powered review will appear here.</p>
        </div>`;
        return;
    }

    if (toggle.checked) {
        // Show HTML preview using marked.js
        output.innerHTML = marked.parse(markdown);
    } else {
        // Show raw Markdown
        // We use textContent to safely render the text, preventing it from being interpreted as HTML.
        output.textContent = markdown;
    }
}

/**
 * Copies the current content (HTML or Markdown) to the clipboard.
 */
function copyToClipboard(type) {
    let toggle, content, outputElem, markdown;

    if (type === 'repo') {
        toggle = document.getElementById("repo-toggle");
        outputElem = document.getElementById("repo-output");
        markdown = repoMarkdown;
    } else {
        toggle = document.getElementById("user-toggle");
        outputElem = document.getElementById("user-output");
        markdown = userMarkdown;
    }

    // Always copy the raw markdown for consistency.
    // Copying innerHTML can be messy.
    // If you truly want to copy HTML, use:
    // content = toggle.checked ? outputElem.innerHTML : markdown;
    
    content = markdown; // Simpler UX: always copy the source markdown

    if (!content) {
        alert("Nothing to copy!");
        return;
    }

    navigator.clipboard.writeText(content)
        .then(() => alert("Markdown copied to clipboard!"))
        .catch(err => alert("Failed to copy: " + err));
}

/**
 * Downloads the content as either a .md or .html file.
 */
function downloadContent(type) {
    let toggle, content, filename, markdown, outputElem;

    if (type === 'repo') {
        toggle = document.getElementById("repo-toggle");
        markdown = repoMarkdown;
        outputElem = document.getElementById("repo-output");
        filename = "repo-review";
    } else {
        toggle = document.getElementById("user-toggle");
        markdown = userMarkdown;
        outputElem = document.getElementById("user-output");
        filename = "user-review";
    }

    if (!markdown) {
        alert("Nothing to download!");
        return;
    }

    if (toggle.checked) {
        // Download as HTML
        content = outputElem.innerHTML;
        filename += ".html";
    } else {
        // Download as Markdown
        content = markdown;
        filename += ".md";
    }

    const blob = new Blob([content], { type: toggle.checked ? "text/html" : "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link); // Required for Firefox
    link.click();
    document.body.removeChild(link);
}

/**
 * Handles switching between the Repository and User tabs.
 * NOTE: This requires a change in your index.html file.
 */
function openTab(eventOrTabId, tabId) {
    // Support two call styles:
    //  - openTab(event, 'tabId')  <- when called from addEventListener
    //  - openTab('tabId')         <- when called inline in HTML (onclick)
    let event = null;
    if (typeof eventOrTabId === 'string') {
        tabId = eventOrTabId;
    } else {
        event = eventOrTabId;
    }

    // Hide all tab content
    const tabs = document.getElementsByClassName("tab-content");
    for (let tab of tabs) {
        if (tab && tab.style) tab.style.display = "none";
    }

    // Show the specific tab content (guard if element not found)
    const target = document.getElementById(tabId);
    if (!target) {
        console.warn(`openTab: tab element not found for id '${tabId}'`);
        return;
    }
    target.style.display = "block";

    // Remove 'active' class from all tab buttons
    const buttons = document.getElementsByClassName("tab-button");
    for (let btn of buttons) {
        btn.classList.remove("active");
    }

    // Add 'active' class to the button that was clicked (if available),
    // otherwise attempt to find the button by its inline onclick attribute.
    if (event && event.currentTarget) {
        event.currentTarget.classList.add("active");
    } else {
        let found = false;
        for (let btn of buttons) {
            try {
                const onclick = btn.getAttribute('onclick') || '';
                if (onclick.includes(`'${tabId}'`) || onclick.includes(`"${tabId}"`)) {
                    btn.classList.add('active');
                    found = true;
                    break;
                }
            } catch (e) {
                // ignore read errors on buttons
            }
        }
        // As a fallback, mark the first tab button active to avoid no-active state
        if (!found && buttons.length > 0) buttons[0].classList.add('active');
    }
}

// Add a little extra CSS for the loading spinner animation and error
const style = document.createElement('style');
style.innerHTML = `
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.loading-spinner {
    animation: spin 1.5s linear infinite;
    stroke: var(--primary-color);
}
.placeholder-error {
    color: #dc3545; /* Red for errors */
    font-weight: 500;
}
`;
document.head.appendChild(style);