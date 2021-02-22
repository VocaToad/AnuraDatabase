from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import argparse
import yaml
import logging
import pathlib
from tables import Species, Recording, Base


databasePath = pathlib.Path(__file__).parent.absolute()
configPath = databasePath.joinpath("config").absolute()
dbConfigPath = configPath.joinpath("DBConfig.yaml").absolute()

class AnuraDatabase:
    def __init__(self):
        logging.debug("Creating instance of AnuraDatabase")
        try:
            self.dbConfig = self.__loadDBConfig()

            engineParameters = "".join([self.dbConfig["dbms"],"://",self.dbConfig["user"],":",self.dbConfig["pswd"],"@",self.dbConfig["host"],":",str(self.dbConfig["port"]),"/"+self.dbConfig["db"]])
            self.engine = create_engine(engineParameters)
            logging.info("Engine created for: "+engineParameters)

            self.meta = MetaData(bind=self.engine, reflect=True)
            Base.metadata = self.meta
            logging.debug("Instance of AnuraDatabase created successfully")
        except:
            logging.critical("Failed create instance of AnuraDatabase")
            logging.exception('')

    def __loadDBConfig(self):
        logging.debug("loadDBConfig started")
        try:
            with open(dbConfigPath, "r") as dbConfigFile:
                dbConfig = yaml.load(dbConfigFile)
            logging.info("Loaded Database Configuration: "+dbConfigPath._str)
        except:
            logging.critical("Error loading Database Configuration:"+dbConfigPath._str)
            logging.exception('')

        logging.debug("loadDBConfig finished")
        return dbConfig

    def Connect(self):
        logging.debug("Connect started")
        try:
            self.engine.connect()
            logging.info("Connected to database: "+self.dbConfig["db"])
        except:
            logging.critical("Unable to connect to database: "+self.dbConfig["db"])
            logging.exception('')

        logging.debug("Connect finished")
    
    def Create(self):
        logging.debug("Create started")
        Species().create(self.engine, self.meta)
        Recording().create(self.engine, self.meta)

    def OpenSession(self):
        logging.debug("OpenSession started")
        try:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            logging.info("Session created")
            return self.session
        except:
            logging.critical("Unable to create session in database: "+self.dbConfig["db"])
            return None

class AnuraDatabaseSetup:
    def __init__(self,args=None):
        self.ParseArguments(args)
        self.anuraDatabase = AnuraDatabase()
        self.anuraDatabase.Connect()
    
    def ParseArguments(self, args):
        parser = argparse.ArgumentParser(description="Database Builder and Populator.")
        
        parser.add_argument("--Create","-c", dest="create", action='store_true', required=False,
                    help="Creates a database.")
        parser.add_argument("--Populate","-p", dest="populate", nargs="*", default=[], required=False,
                    help="List of files to populate the database.")
        parsedArguments = parser.parse_args(args)
        self.create = parsedArguments.create
        self.populate = parsedArguments.populate
    
    def Create(self):
        if not self.create:
            return
        try:
            self.anuraDatabase.Create()
        except:
            logging.critical("Failed create AnuraDatabase")
            logging.exception('')

if __name__ == "__main__":
    anuraDatabase = AnuraDatabaseSetup()
    anuraDatabase.Create()