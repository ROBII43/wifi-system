from flask import render_template
from . import admin_bp
import os

LOG_DIR = "logs"

FILES = {
    "system": "system.log",
    "users": "users.log",
    "payments": "payments.log"
}


@admin_bp.route("/logs")
def logs():

    all_logs = []

    for log_type, file_name in FILES.items():

        path = os.path.join(LOG_DIR, file_name)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

                for line in lines:
                    all_logs.append({
                        "type": log_type,
                        "text": line.strip()
                    })

    # newest first
    all_logs = all_logs[::-1]

    return render_template("admin/logs.html", logs=all_logs)