from pydantic import BaseModel
from fastapi import FastAPI
import tensorflow as tf
import joblib
import os
from email import policy
from email.parser import Parser

from src.preprocess import preprocess_text

app = FastAPI()

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = tf.keras.models.load_model(
    os.path.join(base_path, "ANN", "ann_model.keras")
)

vectorizer = joblib.load(
    os.path.join(base_path, "ANN", "ann_vectorizer.pkl")
)


class Email(BaseModel):
    email: str


@app.get("/")
def home():
    return {
        "message": "spam detection api is running"
    }


@app.post("/predict")
def predict_email(email: Email):

    message = Parser(policy=policy.default).parsestr(email.email)

    subject = message.get("subject", "")

    if message.is_multipart():
        body = ""

        for part in message.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = message.get_content()

    text = subject + " " + body

    clean_text = preprocess_text(text)

    vector = vectorizer.transform([clean_text])
    vector = vector.toarray()

    prediction = model.predict(vector, verbose=0)[0][0]

    if prediction >= 0.5:
        result = "spam"
    else:
        result = "ham"

    return {
        "prediction": result
    }

