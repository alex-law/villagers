from flask import Flask, render_template, request, redirect, url_for
from settup import getConfig
from mongoCommands import dbObj

app = Flask(__name__)

config = getConfig()
db = dbObj(config)


@app.get("/")
def home():
    todo_list = db.getToDo()
    return render_template("base.html", todo_list=todo_list)


# @app.route("/add", methods=["POST"])
@app.post("/add")
def add():
    title = request.form.get("title")
    new_todo = db(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    # todo = db.query.filter_by(id=todo_id).first()
    todo = db.session.query(db).filter(db.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    # todo = db.query.filter_by(id=todo_id).first()
    todo = db.session.query(db).filter(db.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
