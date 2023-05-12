from src.util.dao import DAO

daos = {}
def getDao(collection_name: str):
    """Obtain a data access object of a collection. The purpose of the realization using the singleton pattern is
    to avoid multiple data access objects for the same collection

    parameters:
        collection_name -- the name of the collection

    returns:
        validator -- DAO to the given collection
    """
    if collection_name not in daos:
        daos[collection_name] = DAO(collection_name=collection_name)
    return daos[collection_name]