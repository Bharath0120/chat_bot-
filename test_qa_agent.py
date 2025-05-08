import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import requests  # Added missing import
from qa_agent import fetch_content, answer_question

class TestQAAgent(unittest.TestCase):
    def setUp(self):
        # Sample HTML content for mocking
        self.sample_html = """
        <html>
            <body>
                <p>Sample paragraph 1: This is a test.</p>
                <div>Sample paragraph 2: Another test paragraph.</div>
                <li>Sample paragraph 3: A list item test.</li>
                <p>Cookie policy: ignore this.</p>
            </body>
        </html>
        """
        self.sample_df = pd.DataFrame([
            {'text': 'Sample paragraph 1: This is a test.', 'url': 'https://example.com'},
            {'text': 'Sample paragraph 2: Another test paragraph.', 'url': 'https://example.com'},
            {'text': 'Sample paragraph 3: A list item test.', 'url': 'https://example.com'}
        ])

    @patch('requests.get')
    def test_fetch_content_valid_url(self, mock_get):
        # Mock a successful HTTP response
        mock_response = MagicMock()
        mock_response.text = self.sample_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        df = fetch_content('https://example.com')
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 3)  # 3 paragraphs after filtering
        self.assertEqual(df.iloc[0]['text'], 'Sample paragraph 1: This is a test.')
        self.assertEqual(df.iloc[0]['url'], 'https://example.com')

    @patch('requests.get')
    def test_fetch_content_invalid_url(self, mock_get):
        # Mock a failed HTTP response
        mock_get.side_effect = requests.exceptions.RequestException("Failed to connect")
        
        df = fetch_content('https://invalid-url.com')
        self.assertTrue(df.empty)
        self.assertEqual(list(df.columns), ['text', 'url'])

    def test_answer_question_empty_documentation(self):
        # Test with empty DataFrame
        df = pd.DataFrame(columns=['text', 'url'])
        answer, source = answer_question("What is this?", df)
        self.assertEqual(answer, "Sorry, no documentation available to answer your question.")
        self.assertIsNone(source)

    def test_answer_question_no_match(self):
        # Test with documentation but no matching content
        df = self.sample_df
        answer, source = answer_question("What is Dropbox?", df)
        self.assertEqual(answer, "Sorry, I couldn't find any information in the documentation to answer your question.")
        self.assertIsNone(source)

if __name__ == '__main__':
    unittest.main()