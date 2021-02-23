import argparse
import yaml
import logging
import pathlib
import json
from AnuraDatabase import AnuraDatabase
from tables import Species, Recording

databasePath = pathlib.Path(__file__).parent.absolute()
configPath = databasePath.joinpath("config").absolute()
fnjvAnuraPath = configPath.joinpath("FNJV_Anura.yaml").absolute()

class PopulateDatabase():
    def __init__(self):
        self.anuraDatabase = AnuraDatabase()
        self.anuraDatabase.Connect()
    
    def Populate(self):
        fnjvPopulator = FNJVPopulator(self.anuraDatabase)
        fnjvPopulator.Populate()



class FNJVPopulator:
    def __init__(self,anuraDatabase):
        self.__loadConfigFile()
        self.anuraDatabase = anuraDatabase

    def __loadConfigFile(self):
        logging.debug("loadConfigFile started")
        try:
            with open(fnjvAnuraPath, "r") as fnjvAnuraFile:
                self.fnjvAnura = yaml.load(fnjvAnuraFile)
            logging.info("Loaded fnjvAnura Configuration: "+fnjvAnuraPath._str)
        except:
            logging.critical("Error loading Database Configuration:"+fnjvAnuraPath._str)
            logging.exception('')
        logging.debug("loadConfigFile finished")
    
    def Populate(self):
        self.__PopulateFromFnjvAnuraFile()

    def __LoadFromFnjvAnuraFile(self):
        self.fnjvAnuraFilePath = pathlib.Path(self.fnjvAnura["folder"]).absolute()
        referenceFile = self.fnjvAnuraFilePath.joinpath(self.fnjvAnura["mainFile"]).absolute()
        with open(str(referenceFile)) as f:
            mainData = json.load(f)
        return mainData
        
    def __PopulateFromFnjvAnuraFile(self):
        mainData = self.__LoadFromFnjvAnuraFile()
        successfulRecordings = 0
        failedRecordings = 0
        for recording in mainData["animals"]:
            if self.__PopulateRecording(recording):
                successfulRecordings += 1
            else:
                failedRecordings += 1
        logging.info("Recordings added to database: "+str(successfulRecordings))
        if failedRecordings > 0:
            logging.warning(" Failed Recordings: "+str(failedRecordings))


    def __PopulateRecording(self,recording):
        try:
            recordingData = self.__LoadRecordingFile(recording["filename"])
            animal = self.__SpeciesExist(recordingData)
            if not animal:
                if not self.__AddSpecies(recordingData):
                    return False
            
            if self.__RecordingExist(recordingData):
                return True
            
            if not self.__AddRecording(recordingData):
                return False
            return True
        except:
            logging.exception('')
            return False

    def __SpeciesExist(self, recordingData):
        try:
            session = self.anuraDatabase.OpenSession()
            animal = session.query(Species).filter_by(species=recordingData["species"]).\
                        filter_by(gender=recordingData["gender"]).first()
            session.close()
            return animal
        except:
            logging.exception('')
            return None

    def __AddSpecies(self,recordingData):
        try:
            session = self.anuraDatabase.OpenSession()
            newSpecies = Species(recordingData["class"],\
                recordingData["family"],\
                    recordingData["gender"],\
                        recordingData["species"],\
                            recordingData["popularName"])
            session.add(newSpecies)
            session.commit()
            session.close()
            return True
        except:
            logging.critical("Unable to Create Species: "+recordingData["gender"]+" "+recordingData["species"])
            logging.exception('')
            return False
        
    def __RecordingExist(self,recordingData):
        try:
            session = self.anuraDatabase.OpenSession()
            recording = session.query(Recording).filter_by(number=recordingData["number"]).first()
            session.close()
            return recording
        except:
            logging.exception('')
            return None

    def __AddRecording(self,recordingData):
        try:
            session = self.anuraDatabase.OpenSession()
            animal = session.query(Species).filter_by(species=recordingData["species"]).\
                        filter_by(gender=recordingData["gender"]).first()
            newRecording = Recording(recordingData["number"],\
                animal.id,\
                recordingData["individualData"]["register"],\
                recordingData["individualData"]["individual"],\
                recordingData["individualData"]["location"],\
                recordingData["individualData"]["audio"]["specter"]["url"],\
                recordingData["individualData"]["audio"]["specter"]["file"],\
                recordingData["individualData"]["audio"]["audio"]["url"],\
                recordingData["individualData"]["audio"]["audio"]["file"],\
                )
            session.add(newRecording)
            session.commit()
            session.close()
            return True
        except:
            logging.critical("Unable to Create Recording: "+recordingData["number"])
            logging.exception('')
            return False

    def __LoadRecordingFile(self,filename):
        recordingFile = self.fnjvAnuraFilePath.joinpath(filename).absolute()
        with open(str(recordingFile)) as f:
            recordingData = json.load(f)
        return recordingData


if __name__ == "__main__":
    dbPopulator = PopulateDatabase()
    dbPopulator.Populate()