from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from weather import weather_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
app.register_blueprint(weather_bp)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']
    new_task = Task(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get(id)
    task.completed = True
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
