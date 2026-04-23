import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the main index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'VoterGuide AI' in response.data

def test_chat_api_missing_key_or_error_handling(client, mocker):
    """Test the chat API endpoint handles requests gracefully."""
    # We test the endpoint to ensure it returns a valid response format 
    # even if the API key is not present or if there's a mocked error.
    
    # Mock the genai model to prevent actual API calls during tests
    mocker.patch('app.model', None)
    
    response = client.post('/api/chat', 
                           data=json.dumps({"message": "Hello", "context": "Eligibility", "country": "USA"}),
                           content_type='application/json')
    
    # If model is None (mocked), it should return 500 error gracefully
    assert response.status_code == 500
    assert b'Gemini API key not configured' in response.data

def test_chat_api_valid_payload(client, mocker):
    """Test the chat API with a mocked successful Gemini response."""
    # Mock a dummy model
    class MockModel:
        def generate_content(self, prompt, stream):
            class MockChunk:
                def __init__(self, text):
                    self.text = text
            return [MockChunk("Mocked AI Response")]

    mocker.patch('app.model', MockModel())
    
    response = client.post('/api/chat', 
                           data=json.dumps({"message": "How do I register?", "context": "Registration", "country": "India"}),
                           content_type='application/json')
    
    assert response.status_code == 200
    # Response is streamed, we can check the text
    assert b'Mocked AI Response' in response.data
