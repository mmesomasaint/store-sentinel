# app/services/alert_service.py
import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os
from app.config import settings

class AlertService:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "../templates")
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    async def send_downtime_alert(self, manager_email: str, store_name: str, audit_data: dict):
        """Dispatches an alert email to the store manager."""
        template = self.jinja_env.get_template("downtime_report.html")
        rendered_html = template.render(store_name=store_name, audit=audit_data)

        msg = EmailMessage()
        msg["Subject"] = f"CRITICAL: {store_name} Uptime or Broken Link Alert"
        msg["From"] = settings.EMAILS_FROM_EMAIL
        msg["To"] = manager_email
        msg.set_content(f"Alert for {store_name}: Store status is down or contains broken links.")
        msg.add_alternative(rendered_html, subtype="html")

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT
            )
            print(f"Alert email dispatched to {manager_email}")
        except Exception as e:
            print(f"Alert dispatch failed: {e}")

alert_service = AlertService()
