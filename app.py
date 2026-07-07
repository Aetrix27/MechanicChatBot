from flask import Flask, request, render_template, session
from main import askQuestion
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Required for Flask sessions
    app.secret_key = "replace_this_with_a_random_secret_key"

    @app.route("/", methods=["GET", "POST"])
    def base():
        # Initialize chat history
        if "chat_history" not in session:
            session["chat_history"] = []

        if request.method == "POST":
            prompt = request.form.get("prompt")

            if prompt:
                output = askQuestion(prompt)

                history = session["chat_history"]
                history.append({
                    "prompt": prompt,
                    "output": output
                })

                session["chat_history"] = history

        return render_template(
            "base.html",
            chat_history=session["chat_history"]
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)