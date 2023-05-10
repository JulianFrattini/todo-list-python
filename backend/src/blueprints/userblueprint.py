from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from pymongo.errors import WriteError

from src.util.daos import getDao
from src.controllers.usercontroller import UserController
from src.controllers.taskcontroller import TaskController
controller = UserController(getDao(collection_name='user'))
taskcontroller = TaskController(tasks_dao=getDao(collection_name='task'), videos_dao=getDao(collection_name='video'), todos_dao=getDao(collection_name='todo'), users_dao=getDao(collection_name='user'))

# instantiate the flask blueprint
user_blueprint = Blueprint('user_blueprint', __name__)

# create a new user
@user_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create_user():
    data = request.form.to_dict()
    user = None
    try:
        user = controller.create(data)
        return jsonify(user)
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain one user by id (and optionally update him)
@user_blueprint.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def get_user(id):
    try:
        # get a specific user
        if request.method == 'GET':
            user = controller.get(id)
            return jsonify(user), 200
        # update the user
        elif request.method == 'PUT':
            data = request.form
            update_result = controller.update(id, data)
            user = controller.get(id)
            return jsonify(user), 200
        # delete a user
        elif request.method == 'DELETE':
            taskcontroller.delete_of_user(id=id)
            result = controller.delete(id=id)
            return jsonify({"success": result}), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain one user by id (and optionally update him)
@user_blueprint.route('/bymail/<email>', methods=['GET'])
@cross_origin()
def get_user_by_mail(email):
    try:
        user = controller.get_user_by_email(email)
        return jsonify(user), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain all users and return them
@user_blueprint.route('/all', methods=['GET'])
@cross_origin()
def get_users():
    try:
        users = controller.get_all()
        return jsonify(users), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')