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
    
    prompt = f"""
    You are 'ElectiBot', an intelligent assistant for voters.
    Target Country: {country}, User Current Phase: {context}.
    Question: {user_message}.
    
    CRITICAL: Be ultra-concise. Max 40 words.
    Use {country} electoral laws. If asking for dates/booths, point to { "www.vote.org" if country == "USA" else "eci.gov.in" }.
    """
    
    def generate():
        try:
            # Use generate_content with stream=True
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error: {str(e)}"

    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
