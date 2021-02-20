from sqlalchemy import Column, Integer, String, Sequence, Table, UniqueConstraint
from .Utils import *
from .Base import *
import logging

class Species(Base):
    __tablename__ = 'species'
    
    id = Column(Integer,  Sequence('species_id_seq'), primary_key=True)
    classe = Column(String(256), nullable=False)
    family = Column(String(256), nullable=False)
    gender = Column(String(256), nullable=False)
    species = Column(String(256), nullable=False)
    popularName = Column(String(256))

    def __init__(self, classe=None, family=None, gender=None, species=None, popularName=None):
        self.classe = classe
        self.family = family
        self.gender = gender
        self.species = species
        self.popularName = popularName

    def __repr__(self):
        return "<Species(classe='%s', family='%s', gender='%s', species='%s', popularName='%s')>" % (
                                  self.classe, self.family, self.gender,
                                  self.species, self.popularName)

    def create(self, engine, meta):
        logging.debug("Creating Table Species")
        user = Table(self.__tablename__, meta,
        Column('id',Integer,  Sequence('species_id_seq'), primary_key=True),
        Column('classe', String(256), nullable=False),
        Column('family', String(256), nullable=False),
        Column('gender', String(256), nullable=False),
        Column('species', String(256), nullable=False),
        Column('popularName', String(256)),
        UniqueConstraint('gender','species',name="scientific_name"),
        extend_existing=True
        )
        try:
            user.create(engine)
            logging.info("Table Species Created")
        except:
            logging.error("Failed Species Table Users")
    
    #Migration
    def addColumn(self,engine,column):
        add_column(engine, self.__tablename__, column)
