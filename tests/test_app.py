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
    # Mock the client to None to trigger the missing key error
    mocker.patch('app.client', None)
    
    response = client.post('/api/chat', 
                           data=json.dumps({"message": "Hello", "context": "Eligibility", "country": "USA"}),
                           content_type='application/json')
    
    # If client is None (mocked), it should return 500 error gracefully
    assert response.status_code == 500
    assert b'Gemini API key not configured' in response.data

def test_chat_api_valid_payload(client, mocker):
    """Test the chat API with a mocked successful Gemini response."""
    # Mock a dummy client and stream
    mock_client = mocker.Mock()
    
    class MockChunk:
        def __init__(self, text):
            self.text = text
            
    mock_client.models.generate_content_stream.return_value = [MockChunk("Mocked AI Response")]

    mocker.patch('app.client', mock_client)
    
    response = client.post('/api/chat', 
                           data=json.dumps({"message": "How do I register?", "context": "Registration", "country": "India"}),
                           content_type='application/json')
    
    assert response.status_code == 200
    # Response is streamed, we can check the text
    assert b'Mocked AI Response' in response.data

