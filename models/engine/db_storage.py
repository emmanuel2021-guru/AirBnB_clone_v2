#!/usr/bin/python3

"""Database storage module for the AirBnB clone"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData, inspect
from ..base_model import BaseModel, Base
from ..city import City
from ..state import State
from ..place import Place
from ..review import Review
from ..user import User
from ..amenity import Amenity

import os

os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'


class DBStorage():
    """Class for the database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database storage"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
                                      os.environ.get('HBNB_MYSQL_USER'),
                                      os.environ.get('HBNB_MYSQL_PWD'),
                                      os.environ.get('HBNB_MYSQL_HOST'),
                                      os.environ.get('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        if os.environ.get('HBNB_ENV') == "test":
            metadata = MetaData()
            metadata.reflect(bind=self.__engine)
            metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns all objects under the class name 'cls'"""
        ret_dict = {}
        if cls is not None:
            all_objs = self.__session.query(cls).all()
            for obj in all_objs:
                ret_dict.update({"{}.{}".format(cls, obj.id): obj})
        else:
            """all_users = self.__session.query(User).all()
            for user in all_users:
                ret_dict.update({'User.{}'.format(user.id): user})"""
            all_states = self.__session.query(State).all()
            for state in all_states:
                ret_dict.update({'State.{}'.format(user.id): state})
            all_cities = self.__session.query(City).all()
            for city in all_cities:
                ret_dict.update({'City.{}'.format(city.id): city})
            """all_places = self.__session.query(Place).all()
            for place in all_places:
                ret_dict.update({'Place.{}'.format(place.id): place})
            all_amenities = self.__session.query(Amenity).all()
            for amenity in all_amenities:
                ret_dict.update({'Amenity.{}'.format(amenity.id): amenity})
            all_reviews = self.__session.query(Review).all()
            for review in all_reviews:
                ret_dict.update({'Review.{}'.format(review.id): review})"""
        return ret_dict

    def new(self, obj):
        """Adds a new object to the current database session"""
        self.__session.add(obj)
        self.__session.commit()

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        self.save()
