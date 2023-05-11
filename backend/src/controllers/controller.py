from src.util.dao import DAO

class Controller:
    def __init__(self, dao: DAO):
        self.dao = dao

    def create(self, data: dict):
        try:
            return self.dao.create(data)
        except Exception as e:
            raise

    def get(self, id: str):
        try:
            return self.dao.findOne(id)
        except Exception as e:
            raise

    def get_all(self):
        try:
            return self.dao.find()
        except Exception as e:
            raise

    def update(self, id: str, data: dict):
        try:
            update_result = self.dao.update(id=id, update_data=data)
            return update_result
        except Exception as e:
            raise

    def delete(self, id: str):
        try:
            result = self.dao.delete(id=id)
            return result
        except Exception as e:
            raise
