from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "placement_prediction_secret"
UPLOAD_FOLDER = "dataset"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER




















os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@app.route("/")
def home():
   return render_template("home.html")




@app.route("/about")
def about():
   return render_template("about.html")


@app.route("/dataset")
def dataset():

    # Check whether the user has uploaded a dataset
    if not session.get("uploaded", False):
        return render_template(
            "dataset.html",
            uploaded=False,
            upload_success=False,
            total_students=0,
            total_features=0,
            missing_values=0,
            duplicate_records=0
        )

    files = [
        f for f in os.listdir(app.config["UPLOAD_FOLDER"])
        if f.endswith(".csv")
    ]

    if not files:
        return render_template(
            "dataset.html",
            uploaded=False,
            upload_success=False,
            total_students=0,
            total_features=0,
            missing_values=0,
            duplicate_records=0
        )

    latest_file = max(
        [os.path.join(app.config["UPLOAD_FOLDER"], f) for f in files],
        key=os.path.getmtime
    )

    df = pd.read_csv(latest_file)

    return render_template(
        "dataset.html",
        uploaded=True,
        upload_success=False,
        total_students=len(df),
        total_features=len(df.columns),
        missing_values=df.isnull().sum().sum(),
        duplicate_records=df.duplicated().sum()
    )

@app.route("/upload_dataset", methods=["POST"])
def upload_dataset():

    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    # Mark this session as uploaded
    session["uploaded"] = True

    df = pd.read_csv(filepath)

    return render_template(
        "dataset.html",
        uploaded=True,
        upload_success=True,
        total_students=len(df),
        total_features=len(df.columns),
        missing_values=df.isnull().sum().sum(),
        duplicate_records=df.duplicated().sum()
    )
@app.route("/dataset_summary")
def dataset_summary():

    files = [
        f for f in os.listdir(app.config["UPLOAD_FOLDER"])
        if f.endswith(".csv")
    ]

    if not files:
        return "No dataset uploaded."

    latest_file = max(
        [os.path.join(app.config["UPLOAD_FOLDER"], f) for f in files],
        key=os.path.getmtime
    )

    df = pd.read_csv(latest_file)

    summary = df.describe(include="all").to_html(classes="table table-bordered")

    return render_template(
        "dataset_summary.html",
        shape=df.shape,
        columns=df.columns,
        summary=summary
    )



@app.route("/view_dataset")
def view_dataset():

    files = [
        f for f in os.listdir(app.config["UPLOAD_FOLDER"])
        if f.endswith(".csv")
    ]

    if not files:
        return "No dataset uploaded."

    latest_file = max(
        [os.path.join(app.config["UPLOAD_FOLDER"], f) for f in files],
        key=os.path.getmtime
    )

    df = pd.read_csv(latest_file)

    table = df.head(100).to_html(classes="table table-striped", index=False)

    return render_template("view_dataset.html", table=table)


@app.route("/preprocessing")
def preprocessing():
   return render_template("preprocessing.html")




@app.route("/visualization")
def visualization():
   return render_template("visualization.html")




@app.route("/models")
def models():
   return render_template("models.html")




@app.route("/prediction")
def prediction():
   return render_template("prediction.html")




@app.route("/dashboard")
def dashboard():
   return render_template("dashboard.html")




@app.route("/reports")
def reports():
   return render_template("reports.html")




@app.route("/contact")
def contact():
   return render_template("contact.html")

@app.route("/profile")
def profile():
   return render_template("profile.html")


if __name__ == "__main__":
   app.run(debug=True)
