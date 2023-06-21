#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


place_amenity = Table('place_amenity', Base.metadata,
                      Column(
                             'place_id',
                             String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False
                             ),
                      Column(
                             'amenity_id',
                             String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False
                             )
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", cascade="all, delete",
                               backref="places")
        amenities = relationship("Amenity",
                                 secondary='place_amenity',
                                 back_populates="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def amenities(self):
        """
        Getter attribute amenities that returns the list of Amenity
        instances based on the attribute amenity_ids that
        contains all Amenity.id linked to the Place
        """
        obj_list = []
        amenities_objects = models.storage.all('Amenity')
        for amenity in amenities_objects.values():
            if amenity.id in amenity_ids:
                obj_list.append(amenity)
            return obj_list

    @amenities.setter
    def amenitites(self, obj):
        """
        Setter attribute amenities that handles append method
        for adding an Amenity.id to the attribute amenity_ids
        """
        if isinstance(obj, Amenity):
            if self.id == obj.place_id:
                self.amenity_ids.append(obj.id)
