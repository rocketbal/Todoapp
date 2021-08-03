from flask import Flask, render_template,request,jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todoapp_prod'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

@app.route('/todos/create',methods=["POST"])
def create_todos():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        print(description)
        todo = Todo(description=description)
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


@app.route('/todos/<tocloseid>/close', methods=['POST'])
def close_todo(tocloseid):
    try:
        Todo.query.filter_by(id=tocloseid).delete()
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True })




@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.order_by('id').all())
