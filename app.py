from flask import Flask, render_template, request
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_context():
    """Read context from a text file."""
    try:
        with open("rflogy_info.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No context available."

def ask_gpt_mini(question):
    """Function to query the OpenAI gpt-4o-mini model with context."""
    context = get_context()
    try:
        # Use the context and user question in the prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ]
        )
        # Extract and return the model's response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            response = ask_gpt_mini(question)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)

