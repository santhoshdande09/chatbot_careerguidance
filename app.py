from flask import Flask, request, render_template, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("message").lower()

        if "college" in user_input:
            prompt = f"Suggest the best colleges in India related to: {user_input}. Only include colleges relevant to this query after class 10."
        elif "course" in user_input or "courses" in user_input:
            prompt = f"List the best or trending courses after class 10 for: {user_input}. Keep it concise and relevant."
        elif "subject" in user_input or "subjects" in user_input:
            prompt = f"What subjects should a student choose after class 10 for a career in: {user_input}? Give short and clear advice."
        else:
            prompt = f"""
You are a career guidance expert for students in India after class 10.

Student asked: "{user_input}"

Reply briefly and specifically. Do not give long general explanations unless clearly requested. Focus only on what the student asked.
"""

        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, something went wrong. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
