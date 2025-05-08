C4Scale Take-Home Assignment: AI-Powered Q&A Agent
Overview
This project implements an AI-powered question-answering agent that processes help website documentation and answers user queries. It fetches content via web scraping, stores it in a structured format, and uses TF-IDF vectorization for text matching.
Technical Architecture Overview
The Q&A agent is built using a modular architecture with the following components:

Web Scraper: Utilizes requests to fetch HTML content from a given URL and BeautifulSoup to parse and extract relevant text (e.g., <p>, <div>, <li> tags).
Data Storage: Stores extracted text in a pandas DataFrame, with columns for the text content and source URL, enabling structured access for matching.
Text Matching Engine: Employs scikit-learn’s TF-IDF vectorizer to convert text into numerical vectors and computes cosine similarity between the user’s question and the stored documentation to find the best match.
User Interface: A command-line interface (CLI) that accepts user input (questions) and displays answers with their source URLs.

Implementation Approach
The implementation follows these steps:

Content Fetching: The script takes a URL as input (e.g., via --url argument), uses requests to fetch the webpage, and BeautifulSoup to extract text from specific HTML tags (<p>, <div>, <li>).
Data Processing: The extracted text is cleaned (e.g., removing extra whitespace) and stored in a pandas DataFrame for efficient querying.
Text Matching: The user’s question is vectorized using TF-IDF, and cosine similarity is computed against the vectorized documentation. The paragraph with the highest similarity score is selected as the answer.
Error Handling: Includes checks for invalid URLs, network issues (e.g., connection timeouts), and cases where no matching content is found (returning a fallback message like "Sorry, I couldn't find any information...").
CLI Interaction: A loop in the script prompts the user for questions, processes them, and displays answers until the user types "exit."

Setup Instructions

Create a virtual environment:python -m venv venv


Activate the virtual environment:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate


Install dependencies:pip install requests beautifulsoup4 pandas scikit-learn



Dependencies

requests: For fetching web content.
beautifulsoup4: For HTML parsing and content extraction.
pandas: For structured data handling.
scikit-learn: For TF-IDF vectorization and cosine similarity.

Usage
Run the script with a help website URL:
python qa_agent.py --url https://slack.com/help/articles/205239967-Create-a-channel

Enter questions in the terminal (e.g., "How do I join a channel in Slack on my desktop?") or type "exit" to quit.
Example Interaction
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

Testing Approach
Unit tests are implemented in test_qa_agent.py to validate the core functionality:

Test Cases:
Fetching content from valid URLs (e.g., ensuring the scraper extracts text correctly).
Handling invalid URLs (e.g., raising appropriate errors for non-existent pages).
Handling empty documentation (e.g., ensuring the system gracefully handles cases with no extracted content).
Answering questions with no matching content (e.g., returning a fallback message).


Execution: Run the tests using:python -m unittest test_qa_agent.py


Tests use the unittest framework to mock dependencies (e.g., mocked HTTP responses) and verify expected behavior.

Future Improvement Suggestions

Recursive Crawling: Extend the web scraper to recursively crawl nested pages for broader content coverage.
Dynamic Content Handling: Incorporate a headless browser (e.g., Selenium) to handle JavaScript-rendered content.
Advanced NLP: Replace TF-IDF with a more advanced NLP model (e.g., BERT) for better semantic understanding and answer accuracy.
Caching: Implement caching of fetched content to improve performance for repeated queries.
GUI Interface: Add a graphical user interface (e.g., using Flask or tkinter) to make the tool more user-friendly.

Known Limitations

Does not support recursive crawling of nested pages.
Only extracts text from specific tags; does not handle dynamic content.
Uses basic TF-IDF matching without advanced NLP techniques.
No caching or performance optimizations.

Demo Video
A 4-minute demo video is included in the repository as demo.mp4.
