#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref='state')
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns the list of City instances
            with state_id equals to the current State.id.
            """
            city_instances = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_instances.append(city)
            return city_instances
