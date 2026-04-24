import os
import logging
from flask import Flask, request, jsonify, render_template, Response
import google.generativeai as genai
from dotenv import load_dotenv
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from typing import Generator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Security: Add HTTP security headers
# Note: CSP is configured to allow inline scripts/styles for development, 
# but forces HTTPS and adds anti-clickjacking headers.
Talisman(app, content_security_policy=None)

# Security: Rate Limiting to prevent API abuse
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configure Gemini
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
model = None
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    # Using Flash 1.5 for the best balance of speed and intelligence
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def index() -> str:
    """Render the main application page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute") # Specific rate limit for chat API
def chat() -> Response | tuple[Response, int]:
    """Handle incoming chat messages and stream AI responses."""
    if not model:
        logging.error("Gemini API key is missing.")
        return jsonify({"error": "Gemini API key not configured."}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    user_message = data.get("message", "").strip()
    context = data.get("context", "General Inquiry").strip()
    country = data.get("country", "USA").strip()

    # Security: Input Validation
    if not user_message or len(user_message) > 500:
        return jsonify({"error": "Message is empty or too long (max 500 chars)."}), 400
    
    if len(context) > 50 or len(country) > 50:
        return jsonify({"error": "Context or country parameter is too long."}), 400
    
    # Advanced usage: System Instructions for strict grounding
    system_instruction = f"""
    You are 'ElectiBot', a highly secure and intelligent assistant for voters.
    You must ONLY provide information related to elections, voting, and civic duties.
    If a user asks about anything else, politely decline.
    Target Country: {country}.
    User's Current Progress Phase: {context}.
    CRITICAL RULES:
    1. Be ultra-concise. Maximum 40 words.
    2. Use strict {country} electoral laws.
    3. If they ask for dates or booth locations, ALWAYS direct them to: { "www.vote.org" if country == "USA" else "eci.gov.in" }.
    """
    
    # Configure the model for this specific request with system instructions
    request_model = genai.GenerativeModel(
        'gemini-flash-latest',
        system_instruction=system_instruction
    )
    
    def generate() -> Generator[str, None, None]:
        """Generator function to stream AI response chunks."""
        try:
            # Use generate_content with stream=True for high performance UX
            response = request_model.generate_content(user_message, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logging.error(f"Error generating AI content: {str(e)}")
            yield "Error: Failed to generate response from AI service."

    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
