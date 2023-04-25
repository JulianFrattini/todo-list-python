from src.controllers.controller import Controller
from  src.util.dao import DAO

from bson.objectid import ObjectId

class TodoController(Controller):
    def __init__(self, todo_dao: DAO, tasks_dao: DAO):
        super().__init__(dao=todo_dao)
        self.tasks_dao = tasks_dao

    def create(self, data: dict):
        """Given a valid dict containing the data of the new todo item create a new todo item and return the newly created item. If in addition a taskid attribute is given, then the new todo object will be automatically associated to the task object.

        parameters: 
            data -- dict containing a description under the key description

        returns:
            todo -- created todo object upon success
        
        raises:
            Exception -- in case any database operation fails
        """

        try:
            if 'taskid' in data:
                task = self.tasks_dao.findOne(id=data['taskid'])
                del data['taskid']

                if 'done' in data:
                    if isinstance(data['done'], str):
                        data['done'] = (data['done'].lower() == 'true')

                todo = self.dao.create(data)
                self.tasks_dao.update(id=task['_id']['$oid'], update_data={'$push' : {'todos': ObjectId(todo['_id']['$oid'])}})

                return todo
            else:
                return self.dao.create(data)
        except Exception as e:
            raise