from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# to read or fetch data from database
@app.route('/')
def index():
    todos = Todo.query.all()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', todos=todos, current_datetime=current_datetime)

# to add objects | the id is generated automatically
@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

# to update objects | sends id to update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get(id)

    if request.method == 'POST':
        todo.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', todo=todo)

# uses id to delete object
@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get(id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

