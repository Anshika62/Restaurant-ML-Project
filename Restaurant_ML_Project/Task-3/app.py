from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("Dataset .csv")
df["Cuisines"] = df["Cuisines"].fillna("")

# Recommendation Function
def recommend_restaurants(cuisine, price, delivery):
    result = df[
        (df["Cuisines"].str.contains(cuisine, case=False, na=False)) &
        (df["Price range"] == int(price)) &
        (df["Has Online delivery"] == delivery)
    ]
    return result[["Restaurant Name", "Cuisines", "Price range"]].head(5)

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = None

    if request.method == "POST":
        cuisine = request.form["cuisine"]
        price = request.form["price"]
        delivery = request.form["delivery"]

        results = recommend_restaurants(cuisine, price, delivery)
        recommendations = results.to_dict(orient="records")

    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)