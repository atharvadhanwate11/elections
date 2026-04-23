import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure Gemini
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
model = None
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    # Using Flash 1.5 for the best balance of speed and intelligence
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({"error": "Gemini API key not configured. Please set GEMINI_API_KEY in .env"}), 500
    
    data = request.json
    user_message = data.get("message", "")
    context = data.get("context", "General Inquiry") 
    country = data.get("country", "USA")
    
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
    
    def generate():
        try:
            # Use generate_content with stream=True
            response = request_model.generate_content(user_message, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error: {str(e)}"

    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
