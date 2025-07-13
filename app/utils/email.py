import smtplib
import tempfile
import webbrowser
from pathlib import Path
from urllib.parse import urljoin
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings

GMAIL_USER=settings.GMAIL_USER
GMAIL_PASS=settings.GMAIL_PASS

EMAIL_TEMPLATES_DIR=settings.EMAIL_TEMPLATES_DIR
EMAIL_FROM_NAME=settings.EMAIL_FROM_NAME

FRONTEND_URL=settings.FRONTEND_URL
RESET_PASSWORD_URL=settings.RESET_PASSWORD_URL

EMAIL_RESET_URL = urljoin(settings.FRONTEND_URL + "/", settings.RESET_PASSWORD_URL.lstrip("/"))

def render_email_templates(user_email: str, reset_link: str) -> tuple[str, str] | bool:
    try:
        env = Environment(loader=FileSystemLoader(EMAIL_TEMPLATES_DIR))
        html_template = env.get_template("password_reset.html")
        txt_template = env.get_template("password_reset.txt")

        variables = {
            "user_email": user_email,
            "reset_link": reset_link
        }

        html_content = html_template.render(**variables)
        txt_content = txt_template.render(**variables)
        return html_content, txt_content
    except Exception as e:
        return False

def send_password_reset_email(to_email: str, token: str) -> bool:
    if not GMAIL_USER or not GMAIL_PASS:
        return False
    
    reset_link = f"{EMAIL_RESET_URL}/{token}"

    rendered = render_email_templates(to_email, reset_link)
    if not rendered:
        return False

    html_content, plain_text = rendered

    msg = EmailMessage()
    msg["Subject"] = f"Restablecimiento de contraseña - {EMAIL_FROM_NAME}"
    msg["From"] = f"{EMAIL_FROM_NAME} <{GMAIL_USER}>"
    msg["To"] = to_email
    msg.set_content(plain_text)
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        return False
    
def test_password_reset_email(user_email: str, token: str) -> bool:
    reset_link = f"{EMAIL_RESET_URL}/{token}"

    result = render_email_templates(user_email, reset_link)
    if not result:
        return False

    html_content, plain_text = result

    #print(plain_text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
        f.write(html_content)
        temp_path = Path(f.name)

    webbrowser.open(f"file://{temp_path}")

    return True
