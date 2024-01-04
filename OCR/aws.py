from flask import Flask, request, render_template
import boto3
from decouple import config
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS Textract and AWS Medical Comprehension Configuration
AWS_REGION = config("AWS_REGION")

# Load IAM user credentials
aws_access_key_id = config("AWS_ACCESS_KEY_ID")
aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    # Save file to local storage
    file_path = os.path.join(
        # os.path.dirname(__file__), "static", secure_filename(file.filename)
        "static",
        secure_filename(file.filename),
    )
    file.save(file_path)

    # Analyze text using Textract directly
    textract = boto3.client(
        "textract",
        region_name=AWS_REGION,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Reopen the file in read mode
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Start synchronous text detection
    response = textract.detect_document_text(Document={"Bytes": file_content})

    # Extract text content from Textract response
    text_content = ""
    for block in response.get("Blocks", []):
        if block["BlockType"] == "WORD":
            text_content += block["Text"] + " "

    # Extract medical entities using Medical Comprehend
    medical_comprehend = boto3.client(
        "comprehendmedical",
        region_name=AWS_REGION,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    medical_results = medical_comprehend.detect_entities(Text=text_content)

    # Save Textract response to a JSON file
    with open("textract_response.json", "w") as json_file:
        json.dump(response, json_file, indent=2)

    # Save Medical Comprehend response to a JSON file
    with open("comprehend_response.json", "w") as json_file:
        json.dump(medical_results, json_file, indent=2)

    return render_template(
        "result.html", medical_results=medical_results, image_url=file_path
    )


if __name__ == "__main__":
    app.run(debug=True)
