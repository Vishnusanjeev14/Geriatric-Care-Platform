import json
from pathlib import Path

from flask import session


LANG_DIR = Path(__file__).resolve().parents[1] / "translations"
SUPPORTED_LANGUAGES = {"en": "English", "ta": "Tamil"}


def get_locale(account=None):
    if session.get("language"):
        return session["language"]
    if account:
        return account.preferred_language
    return "en"


def translate(key, account=None):
    locale = get_locale(account)
    data = _load(locale)
    return data.get(key, _load("en").get(key, key))


def _load(locale):
    path = LANG_DIR / f"{locale}.json"
    if not path.exists():
        path = LANG_DIR / "en.json"
    return json.loads(path.read_text(encoding="utf-8"))
