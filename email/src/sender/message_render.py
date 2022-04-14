import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader  # type: ignore

logger = logging.getLogger('email_notification')
template_dir = Path(__file__).resolve().parent.parent.parent


def get_message(template_path: str, msg_data: dict) -> str:
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = env.get_template(template_path)

    return template.render(**msg_data)
