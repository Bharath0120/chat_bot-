 ## Overview
 This project implements an AI-powered question-answering agent that processes help website documentation and answers user queries. It fetches content via web scraping, stores it in a structured format, and uses TF-IDF vectorization for text matching.

 ## Setup Instructions
 1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
 2. Activate the virtual environment:
    - Windows: `venv\Scripts\activate`
    - macOS/Linux: `source venv/bin/activate`
 3. Install dependencies:
    ```bash
    pip install requests beautifulsoup4 pandas scikit-learn
    ```

 ## Dependencies
 - `requests`: For fetching web content.
 - `beautifulsoup4`: For HTML parsing and content extraction.
 - `pandas`: For structured data handling.
 - `scikit-learn`: For TF-IDF vectorization and cosine similarity.

 ## Usage
 Run the script with a help website URL:
 ```bash
 python qa_agent.py --url https://slack.com/help/articles/205239967-Create-a-channel
 ```
 Enter questions in the terminal (e.g., "How do I join a channel in Slack on my desktop?") or type "exit" to quit.

 ## Example Interaction
 ```bash
 $ python qa_agent.py --url https://slack.com/help/articles/205239967-Create-a-channel
 Fetching content from https://slack.com/help/articles/205239967-Create-a-channel...
 Successfully fetched 29 paragraphs from https://slack.com/help/articles/205239967-Create-a-channel.
 Ready to answer questions. Type 'exit' to quit.
 Enter your question: How do I join a channel in Slack on my desktop?
 Answer: Desktop. Mobile. Hover over More. Browse the list of public channels in your workspace, or use the search bar to search by channel name or description. Click Channels. Select a channel from the list to view it. Click on Join channel. Tap the search bar. Tap Channels. Search for a channel and tap the channel name to open it. Tap Join Channel.
 Source: https://slack.com/help/articles/205239967-Create-a-channel

 Enter your question: How do I join a channel in Slack on my phone?
 Answer: Desktop. Mobile. Hover over More. Browse the list of public channels in your workspace, or use the search bar to search by channel name or description. Click Channels. Select a channel from the list to view it. Click on Join channel. Tap the search bar. Tap Channels. Search for a channel and tap the channel name to open it. Tap Join Channel.
 Source: https://slack.com/help/articles/205239967-Create-a-channel

 Enter your question: Who can join public channels in Slack?
 Answer: All members (but not guests) can browse and join public channels in their workspace. For a private channel, you must be added to it by a member of that channel.
 Source: https://slack.com/help/articles/205239967-Create-a-channel

 Enter your question: What is Slack Connect?
 Answer: Tip: If you've been invited to work with another company in a channel using Slack Connect, learn how to accept the invitation.
 Source: https://slack.com/help/articles/205239967-Create-a-channel

 Enter your question: How do I create a channel in Slack?
 Answer: Sorry, I couldn't find any information in the documentation to answer your question.
 ```

 ## Design Decisions
 - **Web Scraping**: Used `requests` and `BeautifulSoup` to fetch and parse content, focusing on `<p>`, `<div>`, and `<li>` tags for broader extraction.
 - **Data Storage**: Stored content in a `pandas` DataFrame for structured access.
 - **Text Matching**: Implemented TF-IDF vectorization with `scikit-learn` to match questions to documentation.
 - **Error Handling**: Added checks for invalid URLs, network issues, and unanswerable questions.

 ## Known Limitations
 - Does not support recursive crawling of nested pages.
 - Only extracts text from specific tags; does not handle dynamic content.
 - Uses basic TF-IDF matching without advanced NLP techniques.
 - No caching or performance optimizations.

 ## Testing
 Run unit tests with:
 ```bash
 python -m unittest test_qa_agent.py
 ```
 Tests cover:
 - Fetching content from valid and invalid URLs.
 - Handling empty documentation.
 - Handling questions with no matching content.

 ## Demo Video
 A 4-minute demo video (`demo.mp4`) is included in the repository.