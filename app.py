from flask import Flask, render_template_string, jsonify
import stripe
import os

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_API_KEY")  # Usa tu clave secreta aquí

@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route("/create-setup-intent")
def create_setup_intent():
    intent = stripe.SetupIntent.create()
    return jsonify(client_secret=intent.client_secret)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
