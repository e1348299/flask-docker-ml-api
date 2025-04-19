from flask import Flask, request, jsonify
import statsmodels.api as sm
import numpy as np
import pandas as pd

app = Flask(__name__)

# Training data
# Treatment (W), Sustainability Spending (X)
X_data = np.array([
    [0, 19.8], [1, 23.4], [1, 27.7], [1, 24.6], [0, 21.5], [1, 25.1], [1, 22.4], [0, 29.3],
    [0, 20.8], [1, 20.2], [1, 27.3], [0, 24.5], [0, 22.9], [1, 18.4], [0, 24.2], [1, 21.0],
    [0, 25.9], [0, 23.2], [1, 21.6], [1, 22.8]
])
# Engagement Score
y_data = np.array([
    137, 118, 124, 124, 120, 129, 122, 142, 128, 114,
    132, 130, 130, 112, 132, 117, 134, 132, 121, 128
])

# Add intercept and fit model
X_data_sm = sm.add_constant(X_data)
model = sm.OLS(y_data, X_data_sm).fit()

# Extract coefficients and ATE (τ) p-value
alpha = model.params[0]
tau = model.params[1]
beta = model.params[2]
tau_pval = model.pvalues[1]

#endpoint to retun ATE and statistical significance of treatment effect
@app.route("/get_ate", methods=["GET"])
def get_ate():
    return jsonify({
        "intercept (alpha)": round(alpha, 3),
        "treatment_effect (tau)": round(tau, 3),
        "sustainability_spending_effect (beta)": round(beta, 3),
        "tau_p_value": round(tau_pval, 5),
        "statistical_significance": "significant" if tau_pval < 0.05 else "not significant"
    })

#endpoint to return predicted engagement score for a given treatment and sustainability spending amount.
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        treatment = data.get("treatment")  # 0 or 1
        spending = data.get("spending")    # float

        if treatment is None or spending is None:
            return jsonify({"error": "Missing 'treatment' or 'spending' field"}), 400

        input_array = np.array([[1, treatment, spending]])  # add constant term manually
        prediction = model.predict(input_array)[0]
        return jsonify({"predicted_engagement": round(prediction, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            treatment = int(request.form.get("treatment"))
            spending = float(request.form.get("spending"))

            input_array = np.array([[1, treatment, spending]])
            prediction = model.predict(input_array)[0]
            prediction_rounded = round(prediction, 2)

            # Write to output.txt
            with open("output.txt", "w") as f:
                f.write(f"Predicted Engagement Score: {prediction_rounded}\n")

            return f"""
                <h2>Predicted Engagement Score: {prediction_rounded}</h2>
                <p>Saved to output.txt</p>
                <a href="/">Back</a>
            """
        except Exception as e:
            return f"<p>Error: {e}</p><a href='/'>Back</a>"

    return """
        <h2>Engagement Score Predictor</h2>
        <form method="post">
            <label>Treatment (0 or 1):</label><br>
            <input type="number" name="treatment" required><br><br>
            <label>Sustainability Spending:</label><br>
            <input type="number" step="any" name="spending" required><br><br>
            <input type="submit" value="Predict">
        </form>
    """
#main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
