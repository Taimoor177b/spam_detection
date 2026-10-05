import os
import pandas as pd
from email import policy
from email.parser import BytesParser

ham_path = "spam_detection/dataset/easy_ham"
spam_path = "spam_detection/dataset/spam"

def read_email(file_path):

    with open(file_path, "rb") as file:
        email = BytesParser(policy=policy.default).parse(file)

    subject = email["subject"]

    body = ""

    if email.is_multipart():

        for part in email.walk():

            if part.get_content_type() == "text/plain":

                try:
                    body = part.get_content()
                except LookupError:
                    payload = part.get_payload(decode=True)
                    body = payload.decode("latin-1", errors="ignore")

                break

    else:

        try:
            body = email.get_content()
        except LookupError:
            payload = email.get_payload(decode=True)
            body = payload.decode("latin-1", errors="ignore")

    return subject, body

subjects = []
messages = []
labels = []

ham_files = os.listdir(ham_path)

for file_name in ham_files:
    file_path = os.path.join(ham_path, file_name)
    subject, body = read_email(file_path)
    subjects.append(subject)
    messages.append(body)
    labels.append("ham")

spam_files = os.listdir(spam_path)

for file_name in spam_files:
    file_path = os.path.join(spam_path, file_name)
    subject, body = read_email(file_path)
    subjects.append(subject)
    messages.append(body)
    labels.append("spam")

df = pd.DataFrame({
    "subject": subjects,
    "message": messages,
    "label": labels
})

df["text"] = df["subject"].fillna("") + " " + df["message"].fillna("")

df.to_csv("spam_detection/dataset/emails.csv", index=False)
# print(df.head())
# print(df["text"])
# print("\nShape:", df.shape)
# print("\nLabels:")
# print(df["label"].value_counts())