from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import cohere
import os

app = Flask(__name__)
CORS(app)

co = cohere.Client("wfz8h6JRR5xcp3Gzno7BWaPXHSlmxzBRztjK8Pb5")  # Replace with your Cohere API key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_prompt", methods=["POST"])
def generate_prompt():
    data = request.json
    category = data.get("category", "")
    user_input = data.get("user_input", "")
    prompt = f"Generate a highly creative and visually rich prompt in the category '{category}' based on this idea: '{user_input}'"

    try:
        response = co.chat(
            message=prompt,
            temperature=0.9,
            max_tokens=600  # Increased for longer prompts
        )
        return jsonify({"prompt": response.text.strip()})
    except Exception as e:
        return jsonify({"prompt": f"Error: {str(e)}"}), 500

@app.route("/modify_prompt", methods=["POST"])
def modify_prompt():
    data = request.json
    prompt_text = data.get("prompt", "")
    message = f"Enhance and expand the following prompt with more vivid detail and imagination:\n{prompt_text}"

    try:
        response = co.chat(
            message=message,
            temperature=0.9,
            max_tokens=600  # Also longer modifications
        )
        return jsonify({"modified_prompt": response.text.strip()})
    except Exception as e:
        return jsonify({"modified_prompt": f"Error: {str(e)}"}), 500

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ✅ New route to serve robots.txt
@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path), 'robots.txt')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
