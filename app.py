from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re
import os

app = Flask(__name__)
genai.configure(api_key="AIzaSyC7iaJKq0BBUxTdOODLGUPpYZyu_0rV09c")

model = genai.GenerativeModel("models/gemma-3-27b-it")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"response": "⚠️ No message received."})
    
    try:
        res = model.generate_content(prompt)
        raw_text = res.text

        # 👇 Auto replace names here
        final_response = (
            raw_text
            .replace("Gemma", "Nova AI")
            .replace("gemma", "Nova AI")
            .replace("Google DeepMind", "Arvindra Studio")
            .replace("DeepMind", "Arvindra")
        )
        final_response = format_markdown(final_response)

        return jsonify({"response": final_response})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"})

def format_markdown(text):
    # Convert **bold**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    # Convert *italic*
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    return text

    
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # get port from Render
    app.run(host="0.0.0.0", port=port)
