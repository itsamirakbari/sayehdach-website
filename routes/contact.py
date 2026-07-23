from flask import Blueprint, request, flash, redirect, url_for
import logging

from services.email_service import send_contact_email
from utils.file_validator import is_allowed_file


logger = logging.getLogger(__name__)


contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        logger.warning("Contact form submitted with missing required fields")
        flash("Bitte füllen Sie alle Pflichtfelder aus.")
        return redirect(url_for("home"))

    files = [
        file for file in request.files.getlist("file")
        if file.filename
    ]

    if len(files) > 5:
        logger.warning("Too many files uploaded")
        flash("Es können maximal 5 Dateien hochgeladen werden.")
        return redirect(url_for("home"))

    for file in files:
        if not is_allowed_file(file):
            logger.warning("Invalid file upload attempt: %s", file.filename)
            flash("Eine hochgeladene Datei ist nicht erlaubt.")
            return redirect(url_for("home"))

    subject = f"Neue Anfrage von {name}"

    success = send_contact_email(
        name=name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
        attachments=files,
    )

    if success:
        logger.info("Contact request processed successfully from %s", name)
        flash("Vielen Dank für Ihre Anfrage. Wir melden uns schnellstmöglich.")
    else:
        logger.error("Failed processing contact request from %s", name)
        flash("Es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.")

    return redirect(url_for("home"))