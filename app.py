from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# Load tasks from JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    tasks = load_tasks()
    task_content = request.form['task']
    if task_content:
        new_task = {
            'id': len(tasks) + 1,
            'content': task_content,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)