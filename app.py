import os
import stripe
from flask import Flask, render_template_string, jsonify, request

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

@app.route("/guardar_tarjeta", methods=["POST"])
def guardar_tarjeta():
    data = request.get_json()
    payment_method = data.get("payment_method")

    if not payment_method:
        return jsonify({"error": "No se proporcionó payment_method"}), 400

    try:
        # Crear cliente
        customer = stripe.Customer.create(description="Cliente guardado automáticamente")

        # Asociar payment_method al cliente
        stripe.PaymentMethod.attach(
            payment_method,
            customer=customer.id,
        )

        # Establecer método por defecto
        stripe.Customer.modify(
            customer.id,
            invoice_settings={"default_payment_method": payment_method},
        )

        return jsonify({
            "message": "Tarjeta guardada exitosamente.",
            "customer_id": customer.id,
            "payment_method_id": payment_method
        })

    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
