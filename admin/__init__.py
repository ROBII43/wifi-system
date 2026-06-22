from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

from . import dashboard, users, mikrotik, billing, logs, settings, api