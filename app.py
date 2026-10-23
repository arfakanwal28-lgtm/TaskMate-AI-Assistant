from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DB_PATH = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                due_date TEXT DEFAULT '',
                category TEXT DEFAULT 'Personal',
                priority TEXT DEFAULT 'Medium',
                completed INTEGER DEFAULT 0
            )
        """)

def all_tasks(search=""):
    with get_db() as db:
        if search:
            like = f"%{search}%"
            return db.execute(
                "SELECT * FROM tasks WHERE title LIKE ? OR category LIKE ? OR description LIKE ? ORDER BY completed, due_date, id DESC",
                (like, like, like)
            ).fetchall()
        return db.execute("SELECT * FROM tasks ORDER BY completed, due_date, id DESC").fetchall()

@app.route("/")
def dashboard():
    tasks = all_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed
    today = date.today().isoformat()
    today_tasks = [t for t in tasks if t["due_date"] == today and not t["completed"]]
    return render_template(
        "dashboard.html", tasks=tasks[:5], total=total, pending=pending,
        completed=completed, today_tasks=today_tasks
    )

@app.route("/tasks")
def tasks_page():
    search = request.args.get("search", "").strip()
    tasks = all_tasks(search)
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    return render_template("tasks.html", tasks=tasks, search=search,
                           total=total, pending=total-completed, completed=completed)

@app.route("/tasks/new", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            with get_db() as db:
                db.execute(
                    "INSERT INTO tasks (title, description, due_date, category, priority) VALUES (?, ?, ?, ?, ?)",
                    (title, request.form.get("description", "").strip(),
                     request.form.get("due_date", ""), request.form.get("category", "Personal"),
                     request.form.get("priority", "Medium"))
                )
        return redirect(url_for("tasks_page"))
    return render_template("task_form.html", task=None, page_title="Add New Task")

@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    with get_db() as db:
        task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not task:
            return redirect(url_for("tasks_page"))
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            if title:
                db.execute("""UPDATE tasks SET title=?, description=?, due_date=?, category=?, priority=?
                              WHERE id=?""",
                           (title, request.form.get("description", "").strip(),
                            request.form.get("due_date", ""), request.form.get("category", "Personal"),
                            request.form.get("priority", "Medium"), task_id))
            return redirect(url_for("tasks_page"))
    return render_template("task_form.html", task=task, page_title="Edit Task")

@app.post("/tasks/<int:task_id>/complete")
def complete_task(task_id):
    with get_db() as db:
        db.execute("UPDATE tasks SET completed = CASE WHEN completed=1 THEN 0 ELSE 1 END WHERE id=?", (task_id,))
    return redirect(request.referrer or url_for("tasks_page"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    return redirect(request.referrer or url_for("tasks_page"))

@app.route("/assistant")
def assistant():
    tasks = all_tasks()
    pending = [t for t in tasks if not t["completed"]]
    suggestions = []
    if not pending:
        suggestions.append("Add one small task to start organising your day.")
    else:
        high = [t for t in pending if t["priority"] == "High"]
        if high:
            suggestions.append(f"Start with your high-priority task: “{high[0]['title']}”.")
        else:
            suggestions.append(f"Choose one manageable task first: “{pending[0]['title']}”.")
        if len(pending) > 3:
            suggestions.append("You have several tasks pending. Break the largest task into smaller steps.")
        if any(t["due_date"] == date.today().isoformat() for t in pending):
            suggestions.append("You have a task due today. Give it attention before lower-priority work.")
    return render_template("assistant.html", tasks=tasks, pending=pending, suggestions=suggestions)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
