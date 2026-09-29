import hmac
import json
import re
import time
import urllib.request
from collections import defaultdict, deque
from datetime import datetime, timedelta

from flask import Flask, abort, jsonify, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

import agent
import calendar_client
import config
import slots

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///requests.db"
db = SQLAlchemy(app)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_hits = defaultdict(deque)


class MeetingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    topic = db.Column(db.String(500), nullable=False)
    start = db.Column(db.DateTime(timezone=True), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending|approved|declined
    created = db.Column(db.DateTime, default=datetime.utcnow)


def _rate_limited(ip):
    q, now = _hits[ip], time.time()
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= config.RATE_LIMIT_PER_HOUR:
        return True
    q.append(now)
    return False


def _notify(text):
    if not config.NOTIFY_WEBHOOK_URL:
        return
    req = urllib.request.Request(
        config.NOTIFY_WEBHOOK_URL, json.dumps({"text": text}).encode(),
        {"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except OSError:
        pass


def _submit(args, start, duration):
    email = str(args["email"]).strip()[:200]
    if not EMAIL_RE.match(email):
        return {"error": "invalid email address"}
    pending = MeetingRequest.query.filter_by(email=email, status="pending").count()
    if pending >= config.MAX_PENDING_PER_EMAIL:
        return {"error": "You already have pending requests. Please wait for a reply."}
    r = MeetingRequest(
        name=str(args["name"])[:100], email=email, topic=str(args["topic"])[:500],
        start=start, duration=duration,
    )
    db.session.add(r)
    db.session.commit()
    _notify(f"Meeting request from {r.name} <{r.email}>: {r.topic} ({duration} min, {start:%a %b %d %H:%M %Z}). "
            f"Review at /admin?token=…")
    return {"status": "submitted", "note": "Pending approval; visitor will get an invite if approved."}


@app.get("/")
def index():
    return render_template("index.html", owner=config.OWNER_NAME)


@app.post("/chat")
def chat():
    if _rate_limited(request.remote_addr):
        return jsonify(error="Too many requests, please try later."), 429
    data = request.get_json(silent=True) or {}
    msgs = data.get("messages")
    if not isinstance(msgs, list) or not msgs or len(msgs) > config.MAX_TURNS:
        return jsonify(error="Bad request."), 400
    clean = []
    for m in msgs:
        if m.get("role") not in ("user", "assistant") or not isinstance(m.get("content"), str):
            return jsonify(error="Bad request."), 400
        clean.append({"role": m["role"], "content": m["content"][:config.MAX_MESSAGE_CHARS]})
    if clean[-1]["role"] != "user":
        return jsonify(error="Bad request."), 400
    try:
        reply = agent.chat(clean, {"submit": _submit})
    except Exception:
        app.logger.exception("agent failure")
        return jsonify(error="Something went wrong. Please try again."), 500
    return jsonify(reply=reply)


def _require_admin():
    token = request.args.get("token") or request.form.get("token", "")
    if not config.ADMIN_TOKEN or not hmac.compare_digest(token, config.ADMIN_TOKEN):
        abort(404)
    return token


@app.get("/admin")
def admin():
    token = _require_admin()
    rows = MeetingRequest.query.filter_by(status="pending").order_by(MeetingRequest.start).all()
    return render_template("admin.html", rows=rows, token=token)


@app.post("/admin/<int:rid>/<action>")
def decide(rid, action):
    token = _require_admin()
    r = db.get_or_404(MeetingRequest, rid)
    if r.status != "pending" or action not in ("approve", "decline"):
        abort(400)
    if action == "approve":
        start = r.start if r.start.tzinfo else r.start.replace(tzinfo=slots.ZoneInfo(config.TIMEZONE))
        now = datetime.now(start.tzinfo)
        busy = calendar_client.get_busy(now, now + timedelta(days=config.MAX_DAYS_AHEAD + 1))
        if not slots.is_slot_valid(start, r.duration, busy, now, min_notice_hours=0):
            return "Slot is no longer free. Decline it or ask the visitor to rebook.", 409
        calendar_client.create_event(
            f"{r.name} / {config.OWNER_NAME}", start, start + timedelta(minutes=r.duration),
            r.email, r.name, f"Topic: {r.topic}",
        )
        r.status = "approved"
    else:
        r.status = "declined"
    db.session.commit()
    return redirect(f"/admin?token={token}")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=False)
