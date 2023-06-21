#!/usr/bin/python3
"""
Data storage engine that persists data in MySQL
database
"""
import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    Represents Database Storage instance
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the DBStorage Object
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                        os.getenv('HBNB_MYSQL_USER'),
                                        os.getenv('HBNB_MYSQL_PWD'),
                                        os.getenv('HBNB_MYSQL_HOST'),
                                        os.getenv('HBNB_MYSQL_DB')
                                        ))
        self.instance_map = {
            'Amenity': Amenity,
            'City': City,
            'Place': Place,
            'State': State,
            'Review': Review,
            'User': User
        }

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all objects depending of the class name
        the format is a dictionary with:
            key = <class-name>.<object-id>
            value = object
        Args:
            cls (String): name of the class instance
        """
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = self.instance_map.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in self.instance_map.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def new(self, obj):
        """
        Adds the object to the current database
        Args:
            obj (Object): The object to add to the database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes from the current database session obj if not None
        Args:
            obj (Object): The object to delete from the database session
        """
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database
        """
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False
                                       )
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def close(self):
        """
        Close the current session if active
        """
        self.__session.remove()