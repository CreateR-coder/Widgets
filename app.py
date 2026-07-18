import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Groq client
# It automatically looks for the GROQ_API_KEY environment variable
client = Groq()

@app.route('/')
def index():
    """Renders the main grid interface."""
    return render_template('index.html')

@app.route('/generate-widget', methods=['POST'])
def generate_widget():
    """
    Receives the user prompt and asks the LLM to generate 
    a self-contained HTML/CSS/JS snippet for the widget.
    """
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    system_instruction = (
        "You are an expert web developer. The user wants to create a mini widget box. "
        "Respond ONLY with valid, clean, self-contained HTML. Include any necessary inline <style> "
        "or <script> tags inside the HTML. Do not wrap the code in markdown code blocks like ```html. "
        "The widget must look modern, functional, and fully responsive to fit its container. "
        "Since you don't have real-time API access for things like 'current song' or 'most visited website', "
        "mock the data realistically using JavaScript so it looks alive and dynamic."
    )

    try:
        # Calling the specified model via Groq
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Create this widget: {prompt}"}
            ],
            temperature=0.2,
        )
        
        widget_html = completion.choices[0].message.content.strip()
        return jsonify({'html': widget_html})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)