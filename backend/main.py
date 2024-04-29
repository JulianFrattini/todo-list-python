# coding=utf-8
import os, json
import pymongo
from dotenv import dotenv_values, load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from src.blueprints.userblueprint import user_blueprint
from src.blueprints.taskblueprint import task_blueprint
from src.blueprints.todoblueprint import todo_blueprint

from src.controllers.usercontroller import UserController
from src.controllers.taskcontroller import TaskController
from src.util.daos import getDao

app = Flask('todoapp')

# configure CORS for cross-origin resource sharing (between the frontend and backend)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# register blueprints
app.register_blueprint(blueprint=user_blueprint, url_prefix='/users')
app.register_blueprint(blueprint=task_blueprint, url_prefix='/tasks')
app.register_blueprint(blueprint=todo_blueprint, url_prefix='/todos')


# simple heartbeat method to check if the server is running
@app.route('/')
@cross_origin()
def ping():
    VERSION = dotenv_values('.env').get('VERSION')
    return jsonify({'version': VERSION}), 200

# simple population method that adds initial data to the database
@app.route('/populate', methods=['POST'])
@cross_origin()
def populate():
    usercontroller = UserController(getDao(collection_name='user'))
    taskcontroller = TaskController(tasks_dao=getDao(collection_name='task'), videos_dao=getDao(collection_name='video'), todos_dao=getDao(collection_name='todo'), users_dao=getDao(collection_name='user'))

    response = {'users': []}
    with open(f'./src/static/data/dummy.json', 'r') as f:
        dummydata = json.load(f)

        for userdata in dummydata:
            user = usercontroller.create({
                'firstName': userdata['firstName'],
                'lastName': userdata['lastName'],
                'email': userdata['email']
            })

            for taskdata in userdata['tasks']:
                taskcontroller.create({
                    'userid': user['_id']['$oid'],
                    'title': taskdata['title'],
                    'description': taskdata['description'],
                    'url': taskdata['url'],
                    'todos': taskdata['todos']
                })

            response['users'].append(user['_id']['$oid'])

    return jsonify(response), 200

# drop all collections and repopulate them
@app.route('/seed', methods=['POST'])
@cross_origin()
def seed():
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

    print(f'Connecting to MongoDB at url {MONGO_URL}')
    client = pymongo.MongoClient(MONGO_URL)
    db = client.edutask

    collections = db.list_collection_names()
    for collection in collections:
        db.drop_collection(collection)

    res = populate()
    data = res.get_json()
    uid = data.get('users')[0]

    return jsonify(uid), 200

# main loop
if __name__ == '__main__':
    # print the URL map, which lists all API endpoints of this flask server
    print(app.url_map)

    host = '0.0.0.0'
    if (os.environ.get('FLASK_BIND_IP')):
        # in case the environment variables contain a different IP address, overwrite the host value
        host = os.environ.get('FLASK_BIND_IP')

    port = os.environ.get('PORT')
    app.run(host, port)
