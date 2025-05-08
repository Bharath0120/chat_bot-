import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse

def fetch_content(url):
    """
    Fetch and process content from a help website URL.
    Args:
        url (str): The URL of the help website to scrape.
    Returns:
        pd.DataFrame: A DataFrame containing the extracted text and source URL.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch content from {url}. Reason: {str(e)}")
        return pd.DataFrame(columns=['text', 'url'])

    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup(['nav', 'header', 'footer', 'script', 'style']):
        tag.decompose()

    # Extract text from <p>, <div>, and <li> tags
    paragraphs = soup.find_all(['p', 'div', 'li'])
    data = []
    for p in paragraphs:
        text = p.get_text().strip()
        # Filter out short or irrelevant text
        if text and len(text.split()) > 5 and "cookie" not in text.lower():
            data.append({'text': text, 'url': url})

    if not data:
        print(f"Warning: No meaningful content found at {url}.")
        return pd.DataFrame(columns=['text', 'url'])

    df = pd.DataFrame(data)
    print(f"Successfully fetched {len(df)} paragraphs from {url}.")
    return df

def answer_question(question, df):
    """
    Answer a user question by finding the most relevant text in the DataFrame.
    Args:
        question (str): The user's question.
        df (pd.DataFrame): DataFrame containing documentation text and URLs.
    Returns:
        tuple: (answer, source_url) where answer is the response text and source_url is the reference URL.
    """
    if df.empty or 'text' not in df.columns:
        return "Sorry, no documentation available to answer your question.", None

    doc_texts = df['text'].tolist()
    if not doc_texts:
        return "Sorry, no documentation available to answer your question.", None

    try:
        vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        doc_vectors = vectorizer.fit_transform(doc_texts)
        question_vector = vectorizer.transform([question])

        # Compute cosine similarity
        similarities = cosine_similarity(question_vector, doc_vectors)[0]
        max_sim_idx = similarities.argmax()
        max_sim = similarities[max_sim_idx]

        # Debug: Print top 3 similarity scores
        print("Debug: Top 3 similarity scores:")
        top_indices = similarities.argsort()[-3:][::-1]
        for idx in top_indices:
            print(f"Score: {similarities[idx]:.4f}, Paragraph: {doc_texts[idx][:100]}...")

        # Threshold for relevance
        if max_sim < 0.3:
            return "Sorry, I couldn't find any information in the documentation to answer your question.", None

        return df.iloc[max_sim_idx]['text'], df.iloc[max_sim_idx]['url']
    except Exception as e:
        print(f"Error in answering question: {str(e)}")
        return "Error processing the question. Please try again.", None

def main():
    """
    Main function to run the Q&A agent via terminal.
    Accepts a URL as input and processes user questions interactively.
    """
    parser = argparse.ArgumentParser(description="AI-powered Q&A Agent for Help Documentation")
    parser.add_argument("--url", required=True, help="URL of the help website (e.g., https://slack.com/help/articles/205239967-Create-a-channel)")
    args = parser.parse_args()

    print(f"Fetching content from {args.url}...")
    df = fetch_content(args.url)
    if df.empty:
        print("No content fetched. Exiting.")
        return

    print("Ready to answer questions. Type 'exit' to quit.")
    while True:
        question = input("Enter your question: ")
        if question.lower() == "exit":
            print("Exiting Q&A agent. Goodbye!")
            break
        if not question.strip():
            print("Please enter a valid question.")
            continue
        answer, source = answer_question(question, df)
        print("\nAnswer:", answer)
        if source:
            print(f"Source: {source}\n")

if __name__ == "__main__":
    main()