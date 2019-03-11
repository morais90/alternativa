
import os
import sys
import configparser
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()

class Institution(Base):
	__tablename__ = "institution"
    id = Column(Integer, primary_key=True)
    name = Column(String) 
    cnpj = Column(String)
    number = Column(String)	#cases like '22A' or 'sem numero'
    additional_address_info = Column(String) #apartamento, etc
    cep_id = Column(Integer, ForeignKey('cep.id',ondelete='cascade'), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id',ondelete='cascade'), nullable=False)
    field_id = Column(Integer, ForeignKey('institutionfield.id'))


class InstitutionField(Base):
	__tablename__ = "institutionfield"
	id = Column(Integer, primary_key=True)
    name = Column(String) 


class SocialWorker(Base):
	__tablename__ = "socialworker"
	id = Column(Integer, primary_key=True)
    name = Column(String) 
    cpf = Column(String)
    number = Column(String)	#cases like '22A' or 'sem numero'
    additional_address_info = Column(String) #apartamento, etc
    cep_id = Column(Integer, ForeignKey('cep.id', ondelete='cascade'), nullable=True)
    city_id = Column(Integer, ForeignKey('city.id',ondelete='cascade'), nullable=False)

class Convict(Base):
	__tablename__ = "convict"
	id = Column(Integer, primary_key=True)
    name = Column(String) 
    cpf = Column(String)
    number = Column(String)	#cases like '22A' or 'sem numero'
    additional_address_info = Column(String) #apartamento, etc
    cep_id = Column(Integer, ForeignKey('cep.id',ondelete='cascade'), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id',ondelete='cascade'), nullable=False)

class Conviction(Base):
	__tablename__ = "convict"
	id = Column(Integer, primary_key=True)
	convict_id = Column(Integer, ForeignKey('convict.id',ondelete='cascade'), nullable=False)
    description = Column(String)
    issued = Column(DateTime)


class Activity(Base):
	__tablename__ = "activity"
	conviction_id = Column(Integer, ForeignKey('conviction.id'))
	socialworker_id =Column(Integer, ForeignKey('socialworker.id'))
	institution_id = Column(Integer, ForeignKey('institution.id'))
	date = Column(DateTime)
	status = convict_id = Column(Integer, ForeignKey('activitystatus.id'), nullable=False)

class ActivityStatus(Base):
	__tablename__ = "activitystatus"
	id = Column(Integer, primary_key=True)	
	description = Column(String)

class City(Base):
	__tablename__ = "city"
	id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)

class Cep(Base):
	__tablename__ = "cep" 
	id = Column(Integer, primary_key=True)
	street = Column(String) 
	zone = Column(String) 


class Skill(Base):
	__tablename__ = "skill"
	id = Column(Integer, primary_key=True)
	group = Column(String) 
    name = Column(String) 



#Will return a connector to a DB
def get_db_engine(create_schema=False):
	#Reads DB info from config file
	config = configparser.ConfigParser()
	config.read('db.properties')
	username = config['DEFAULT']['user']
	password = config['DEFAULT']['password']
	url = config['DEFAULT']['url']
	dbname = config['DEFAULT']['dbname']

	engine = create_engine('postgresql://'+username+':'+password+'@'+url+'/'+dbname)
	engine.connect()
	if create_schema:
		Base.metadata.drop_all(engine)
		Base.metadata.create_all(engine)
		populate_basic_tables(engine)
	return engine

#Returns the Session element with the database. Must not
#be used along with get_db_engine, you must choose between them
def get_db_session(create_schema=False):
	Session = sessionmaker(bind=get_db_engine(create_schema=create_schema))
	return Session()