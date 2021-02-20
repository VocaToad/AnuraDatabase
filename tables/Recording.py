from sqlalchemy import Column, String, Integer, Sequence, Table, UniqueConstraint
from .Utils import *
from .Base import *
import logging

class Recording(Base):
    __tablename__ = 'recordings'
    
    id = Column(Integer,  Sequence('recording_id_seq'), primary_key=True)
    number = Column(String(50), nullable=False)
    species = Column(Integer, nullable=False)
    individual = Column(String(2000))
    register = Column(String(2000))
    location = Column(String(2000))
    specterUrl = Column(String(500))
    specterPath = Column(String(500))
    audioUrl = Column(String(500))
    audioPath = Column(String(500))

    def __init__(self, number=None, species=None, individual=None, register=None, location=None, specterUrl=None, specterPath=None, audioUrl=None, audioPath=None):
        self.number = number
        self.species = species
        self.individual = individual
        self.register = register
        self.location = location
        self.specterUrl = specterUrl
        self.specterPath = specterPath
        self.audioUrl = audioUrl
        self.audioPath = audioPath

    def __repr__(self):
        return "<Recordings(number='%s', species='%s', individual='%s', register='%s', location='%s', specterUrl='%s', specterPath='%s', audioUrl='%s', audioPath='%s')>" % (
                                  self.number, self.species, self.individual,
                                  self.register, self.location, self.specterUrl,
                                  self.specterPath, self.audioUrl, self.audioPath
                                  )

    def create(self, engine, meta):
        logging.debug("Creating Table Recordings")
        user = Table(self.__tablename__, meta,
        Column('id',Integer,  Sequence('species_id_seq'), primary_key=True),
        Column('number', String(50), nullable=False),
        Column('species', Integer, ForeignKey("species.id"), nullable=False),
        Column('register', String(2000)),
        Column('individual', String(2000)),
        Column('location', String(2000)),
        Column('specterUrl', String(500)),
        Column('specterPath', String(500)),
        Column('audioUrl', String(500)),
        Column('audioPath', String(500)),
        extend_existing=True
        )
        try:
            user.create(engine)
            logging.info("Table Recordings Created")
        except:
            logging.error("Failed Recordings Table Users")
    
    #Migration
    def addColumn(self,engine,column):
        add_column(engine, self.__tablename__, column)