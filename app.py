from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Initialize the database (create the "todo" table) if not exists
def init_db():
    with app.app_context():
        db.create_all()

# Call init_db to create the table before running the app
init_db()

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['POST', 'GET'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def about():
    return 'Hi Binoy!'

if __name__ == "__main__":
    app.run(debug=True)
