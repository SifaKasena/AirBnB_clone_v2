#!/usr/bin/python3
"""Module to define method for database storage engine"""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Class to manage database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a DBStorage instance"""
        user = environ['HBNB_MYSQL_USER']
        pwd = environ['HBNB_MYSQL_PWD']
        host = environ['HBNB_MYSQL_HOST']
        db = environ['HBNB_MYSQL_DB']
        url = f"mysql+mysqldb://{user}:{pwd}@{host}/{db}"
        self.__engine = create_engine(url, pool_pre_ping=True)

        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query objects from the database session based on the class name.
        If cls=None, query all types of objects.
        Returns a dictionary: {<class-name>.<object-id>: object}
        """
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        objs_dict = {}
        if cls:
            classes = [cls]
        else:
            classes = [User, State, Review, City, Amenity, Place]

        for cls in classes:
            cls_objs = self.__session.query(cls)
            for obj in cls_objs:
                key = f'{obj.__class__.__name__}.{obj.id}'
                objs_dict[key] = obj
        
        return (objs_dict)

    def new(self, obj):
        """Add a new object to the session"""
        self.__session.add(obj)
        
    def save(self):
        """Commits changes on the current session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """Deletes an object from the session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables and recreates a session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
