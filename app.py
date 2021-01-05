from flask import Flask, request
from flask import render_template
from flask import redirect
import os

#  引入form類別
#from view_form import UserForm
basedir = os.path.abspath(os.path.dirname(__file__))

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_moment import Moment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your key values'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test.db')
#這裡要注意拼寫，不要把 URI 寫成 URL。前一個是通用資源表示號（Universal Resource Identifier），後者是統一資源定位符（Uniform Resource Locator）。

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
moment = Moment(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content

@app.before_first_request
def create_db():
    # Recreate database each time for demo
    #db.drop_all()
    db.create_all()

#查看全部
@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)
    #該函式需要傳入模板檔名和模板引數的變數列表，並返回模板中所有佔位符都用實際變數值替換後的字串結果。

@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')
@app.route('/edit/<int:task_id>/', methods=['GET','POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not task:
        return redirect('/')
    if request.method == "POST":
        task.content = request.form['content']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', task=task)

   
""""
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if request.method == "POST":
        task.content = request.form['content']
        if not task.content:
            return 'Error'

        task = Task(content)
        db.session.commit()
        return redirect('/')
    else:
		return render_template('list.html', tasks=tasks)
"""
"""
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    print(task)
    if not task:
        return redirect('/')
    if request.method == "POST":
        task.content = request.form[task_id]
        print(task.content)
        if not task.content:
            return 'Error'

        db.session.commit()
        return redirect('/')
"""

#查看readme
@app.route('/readme')
def readme():
    return render_template('readme.html')

if __name__ == '__main__':
    #app.debug= True
    #app.config['SECRET_KEY']='your key'
    app.run()