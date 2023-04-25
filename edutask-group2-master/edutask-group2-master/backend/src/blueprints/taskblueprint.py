from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from pymongo.errors import WriteError
import json

#import src.controllers.taskcontroller as controller
from src.controllers.taskcontroller import TaskController
from src.util.daos import getDao
controller = TaskController(tasks_dao=getDao(collection_name='task'), videos_dao=getDao(collection_name='video'), todos_dao=getDao(collection_name='todo'), users_dao=getDao(collection_name='user'))

# instantiate the flask blueprint
task_blueprint = Blueprint('task_blueprint', __name__)

# create a new task
@task_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create():
    try:
        data = request.form.to_dict(flat=False)
        userid = data['userid'][0]
        # convert all non-array fields back to simple values
        for key in ['title', 'description', 'start', 'due', 'userid', 'url']:
            if key in data and isinstance(data[key], list):
                data[key] = data[key][0]

        taskid = controller.create(data)
        tasks = controller.get_tasks_of_user(userid)
        return jsonify(tasks), 200
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# get or update a specific task
@task_blueprint.route('/byid/<id>', methods=['GET', 'PUT'])
@cross_origin()
def get(id):
    try:
        if request.method == 'GET':
            task = controller.get(id)
            return jsonify(task), 200
        elif request.method == 'PUT':
            data = request.form.to_dict(flat=True)['data']
            data = json.loads(data.replace("'", "\""))

            task = controller.update(id, data)
            return jsonify(task), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain all tasks associated to a specific user
@task_blueprint.route('/ofuser/<id>', methods=['GET'])
@cross_origin()
def get_tasks_of_user(id):
    try:
        tasks = controller.get_tasks_of_user(id)
        return jsonify(tasks), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')