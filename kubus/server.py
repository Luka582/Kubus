from flask import Flask, render_template, request, redirect, url_for, flash
from os import getenv
from dotenv import load_dotenv
import smtplib
from project import Project
import os
from email.message import EmailMessage
from email.policy import SMTP
OWN_EMAIL ="office@kubus.rs"
OWN_PASSWORD= getenv("OWN_PASSWORD") #app key
load_dotenv()
CONFIRMATION_EMAIL = """
Poštovani,

Potvrđujemo da je uput uspešno popunjen. Hvala Vam na saradnji!

Ukoliko imate dodatnih pitanja, slobodno nas kontaktirajte:
  Email: info@kubus.rs  
  Telefon: +381 11 123 4567  
  Lokacija: Bulevar Oslobođenja 123, Beograd

Srdačan pozdrav,
Kubus tim
"""

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

project_folders = os.listdir(app.static_folder)
PROJECTS = [Project(f"{app.static_folder}/{x}", app.static_folder) for x in project_folders if x != "media"]

PROJECTS.sort(key=lambda x:x.data["project importance"], reverse=True)
for project in PROJECTS:
    project.set_id(PROJECTS.index(project)+1)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods= ["GET", "POST"])
def contact():
    if request.method == "POST":
        email_message = ""
        for key, value in request.form.items():
            email_message+= f"{key}: {value}\n"
        confirmation_msg= EmailMessage(policy=SMTP)
        confirmation_msg["From"] = OWN_EMAIL
        confirmation_msg["To"] = str(request.form["email_input"])
        confirmation_msg["Subject"]="Potvrda o popunjenom uputu Kubus"
        confirmation_msg.set_content(CONFIRMATION_EMAIL)

        data_msg= EmailMessage(policy=SMTP)
        data_msg["From"] = OWN_EMAIL
        data_msg["To"] = OWN_EMAIL
        data_msg["Subject"]="Neko je popunio formular"
        data_msg.set_content(email_message)
        
        message_status = "Success"

        try:
            with smtplib.SMTP_SSL("mail.kubus.rs", port=465) as connection:
                connection.login(OWN_EMAIL, OWN_PASSWORD)
                connection.send_message(confirmation_msg)
                connection.send_message(data_msg)
        except Exception as e:
            print(f"\n\nReason for the failed email:\n\n{e}\n\n\n\n")
            message_status = "Error"
        
        flash(message_status)
        return  redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/projects", methods=["GET", "POST"])
def projects():
    return render_template("projects.html",projects=PROJECTS)

@app.route("/projects/<int:index>")
def project_details(index):
    return render_template("project_details.html", this_project = PROJECTS[index-1])


if __name__ == "__main__":
    app.run(debug = True)