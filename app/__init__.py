import os
from flask import Flask
from app.config import Config
app=Flask(__name__)
app.config.from_object(Config)
if os.environ.get("RENDER") == "true":
    app.config.update(
        SESSION_COOKIE_SECURE=True,     # Cookies only sent over HTTPS
        SESSION_COOKIE_HTTPONLY=True,   # Prevent JavaScript access
        SESSION_COOKIE_SAMESITE="Lax"   # Avoid cross-site issues
    )
else:
    # Local development settings (cookies work on http://127.0.0.1)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax"
    )
from app import routes
