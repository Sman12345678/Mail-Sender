from flask import Flask, request, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
SUBJECT = "QUICK MAIL"

app = Flask(__name__)

# Function to send email
def send_mail(sender_email, password, receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Add email body
        msg.attach(MIMEText(body, "plain"))

        # Set up SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Encrypt connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return "🎉 Email Sent Successfully"
    except Exception as e:
        return f"Error Occurred: {e}"

# Flask routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send-mail", methods=["POST"])
def send_message():
    receiver_email = request.form.get("receiver_email")
    body = request.form.get("body")
    result = send_mail(SENDER_EMAIL, PASSWORD, receiver_email, SUBJECT, body)
    return render_template("index.html", message=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=3000)
