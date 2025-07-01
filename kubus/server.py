from flask import Flask, render_template, request, redirect, url_for, flash
from os import getenv
from dotenv import load_dotenv
import smtplib
from project import Project
import os
OWN_EMAIL ="office@kubus.rs"
OWN_PASSWORD="" #app key
load_dotenv()
CONFIRMATION_EMAIL = """
Subject: Potvrda o popunjenom uputu – Kubus

Poštovani,

Potvrđujemo da je uput uspešno popunjena. Hvala Vam na saradnji!

Ukoliko imate dodatnih pitanja, slobodno nas kontaktirajte:
📧 Email: info@kubus.rs  
📞 Telefon: +381 11 123 4567  
📍 Lokacija: Bulevar Oslobođenja 123, Beograd

Srdačan pozdrav,
Kubus tim
"""
project_folders = os.listdir("static")
PROJECTS = [Project(f"static/{x}") for x in project_folders if x != "media"]
PROJECTS.sort(key=lambda x:x.data["project importance"], reverse=True)
for project in PROJECTS:
    project.set_id(PROJECTS.index(project)+1)


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods= ["GET", "POST"])
def contact():
    if request.method == "POST":
        email_message = "Subject:Neko je popunio formular preko sajta\n\n"
        for key, value in request.form.items():
            email_message+= f"{key}: {value}\n"
        message_status = "Success"

        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(OWN_EMAIL, OWN_PASSWORD)
                connection.sendmail(OWN_EMAIL, str(request.form["email_input"]), CONFIRMATION_EMAIL)
                connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)
        except:
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