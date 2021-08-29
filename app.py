from flask import Flask, render_template,request,jsonify,abort,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todoapp_prod'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# ---------------------------- Todo table declaration ------------------------------- #
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean,nullable=False,default=False)
    list_id = db.Column(db.Integer,db.ForeignKey('todolists.id',ondelete="cascade"),nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    todos=db.relationship('Todo',backref='list',cascade="all,delete-orphan",lazy=True)

# ---------------------------- Create a new item in the todo table ------------------------------- #
@app.route('/todos/create',methods=["POST"])
def create_todos():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description,list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        print('error')
        abort(400)
    else:
        return jsonify(body)


# ------------------------ Create a new list in the todolist table --------------------------- #
@app.route('/todos/createlist',methods=["POST"])
def create_todoslist():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['name'] = todolist.name
        body['list_id'] = todolist.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        print('error')
        abort(400)
    else:
        return jsonify(body)



# ----------------------------Update completed items with true ------------------------------- #
@app.route('/todos/<todoId>/check-completed', methods=['POST'])
def check_completed(todoId):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todoId)
        todo.completed = completed
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))


# ----------------------------Update completed items with true ------------------------------- #
@app.route('/todos/<todoId>/list-completed', methods=['POST'])
def list_completed(todoId):
    try:
        print("List_completed")
        completed = request.get_json()['completed']
        Todo.query.filter_by(list_id=todoId).delete()
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))



# ----------------------------Close completed items ------------------------------- #
@app.route('/todos/<tocloseId>/close', methods=['DELETE'])
def close_todo(tocloseId):
    print(tocloseId)
    try:
        Todo.query.filter_by(id=tocloseId).delete()
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True })


# ----------------------------Close todolist ------------------------------- #
@app.route('/todos/<closelistId>/closelist', methods=['DELETE'])
def close_list(closelistId):
    print("close_list")
    try:
        TodoList.query.filter_by(id=closelistId).delete()
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True })



@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
    lists=TodoList.query.all(),
    todos=Todo.query.filter_by(list_id = list_id).order_by('id').all())


@app.route('/')
def index():
    return redirect(url_for('get_list_todos',list_id=1))
