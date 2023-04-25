from bson.objectid import ObjectId
from datetime import datetime

from src.controllers.controller import Controller
from src.util.dao import DAO

class TaskController(Controller):
    def __init__(self, tasks_dao: DAO, videos_dao: DAO, todos_dao: DAO, users_dao: DAO):
        super().__init__(dao=tasks_dao)
        self.videos_dao = videos_dao
        self.todos_dao = todos_dao
        self.users_dao = users_dao

    def create(self, data: dict):
        """Create a new task object based on the data contained in the dict. The data must contain at least a userid, a video url and a title. If todos are contained in the data, create todo objects and associate them to the task

        attributes:
            data -- dict containing the data of the new task (at least a title, url, and userid)

        returns:
            task -- newly created task object
        
        raises:
            KeyError -- in case an important key is missing in the data dict
            Exception -- in case any database operation fails
        """

        # store the userid
        if 'userid' not in data:
            raise KeyError('When creating a task object, the userid of the associated user must be given')
        uid = data['userid']
        del data['userid']

        
        # fill default values for missing values
        if 'startdate' not in data:
            data['startdate'] = datetime.today()
        if 'categories' not in data:
            data['categories'] = []

        try:
            # add the video url
            video = self.videos_dao.create({'url': data['url']})
            del data['url']
            data['video'] = ObjectId(video['_id']['$oid'])

            # create and add todos
            todos = []
            for todo in data['todos']:
                todoobj = self.todos_dao.create({'description': todo, 'done': False})
                todos.append(ObjectId(todoobj['_id']['$oid']))
            data['todos'] = todos

            # create the task object and assign it to the user
            task = self.dao.create(data)
            self.users_dao.update(
                uid, {'$push': {'tasks': ObjectId(task['_id']['$oid'])}})
            return task['_id']['$oid']
        except Exception as e:
            raise

    def get(self, id: str):
        try:
            task = super().get(id)
            return self.populate_task(task)
        except Exception as e:
            raise


    def get_tasks_of_user(self, id: str):
        """Return all task objects that are associated to a specific user.

        attributes:
            id -- the unique identifier of a user object

        returns:
            tasks -- list of tasks associated to that user

        raises:
            Exception -- in case any database operation fails
        """
        try:
            user = self.users_dao.findOne(id)
            tasks = self.dao.find(filter={'_id': user['tasks']}, toid=['_id'])

            for task in tasks:
                self.populate_task(task)

            return tasks
        except Exception as e:
            raise

    def populate_task(self, task):
        """Populate a given task object by resolving dependencies: replace the id contained in the video attribute by the actual video object and replace each todo id contained in the todos attribute by all actual todo objects

        parameters:
            task -- task object with reference ids (external keys)

        returns:
            task -- task object with resolved references        
        """
        # populate the video of the task
        video = self.videos_dao.findOne(task['video']['$oid'])
        task['video'] = video

        # populate the todos of the task
        todos = self.todos_dao.find(filter={'_id': task['todos']}, toid=['_id'])
        task['todos'] = todos

        return task

    def delete_of_user(self, id: str):
        """Delete all tasks that are associated to a user with the given ID. This includes each video and all todo items associated to each of the tasks.
        
        parameters:
            id -- the unique identifier of a user object
            
        returns:
            n -- number of deleted tasks
        
        raises:
            Exception -- in case any database operation fails
        """
        try:
            user = self.users_dao.findOne(id)
            if 'tasks' in user:
                tasks = self.dao.find(filter={'_id': user['tasks']}, toid=['_id'])

                for task in tasks:
                    self.videos_dao.delete(id=task['video']['$oid'])
                    for todo in task['todos']:
                        self.todos_dao.delete(id=todo['$oid'])
                    self.dao.delete(id=task['_id']['$oid'])

                return len(tasks)
            else:
                return 0
        except Exception as e:
            raise