import tempfile
import webbrowser
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings

EMAIL_TEMPLATES_DIR=settings.EMAIL_TEMPLATES_DIR

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
    
def send_password_reset_email(user_email: str, token: str) -> bool:
    reset_link = f"{token}"

    result = render_email_templates(user_email, reset_link)
    if not result:
        return False

    html_content, plain_text = result

    print(plain_text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
        f.write(html_content)
        temp_path = Path(f.name)

    webbrowser.open(f"file://{temp_path}")

    return True
