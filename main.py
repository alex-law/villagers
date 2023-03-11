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
    if len(title.strip()) > 0:
        new_todo_dict = {'title': title,
                        'complete': False}
        db.addToDo(new_todo_dict)
    return redirect(url_for("home"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.collection.find_one({'id': str(todo_id)})
    todo['complete'] = not todo['complete']
    db.collection.update_one({'id':str(todo_id)}, {"$set": todo}, upsert=False)
    return redirect(url_for("home"))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    db.collection.delete_one({'id': str(todo_id)})
    return redirect(url_for("home"))
