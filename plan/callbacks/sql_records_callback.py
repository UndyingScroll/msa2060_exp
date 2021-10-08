from sqlalchemy import create_engine  
from sqlalchemy import String, DateTime, JSON, Text, Table, Column, Integer, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker, relationship
import json
from openhtf.output.callbacks import json_factory
import re, os, json, yaml, time, datetime






def sql_reports_callback(test_record):
    record_dict = json_factory.OutputToJSON(sort_keys = True).convert_to_dict(test_record)
   
    settings = 'records_db.yaml'
    if os.path.exists(settings):
        try:
            with open(settings) as file:
            
                db_settings = yaml.load(file, Loader=yaml.FullLoader)
                db_string = str(db_settings['uri'])
            
           
            print(db_string)
        except:
            print('failed to load yaml file. exiting')
            exit(2)
    else:
        print('Database settings file C:\\WorkFlow\\records_db.yaml does not exist. exiting')
        exit()

    
    db = create_engine(db_string)  
    Base = declarative_base()
    
    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        children = relationship("Child", back_populates="parent")

        dut_id = Column(String)
        test_name = Column(String)
        test_version = Column(String)
        test_description = Column(String)
        station_id = Column(String)
        test_date = Column(DateTime)
        test_duration = Column(BigInteger)
        user_id = Column(String)
        test_outcome = Column(String)
        record = Column(JSON)
    

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))
        parent = relationship("Parent", back_populates="children")

        name = Column(String)
        outcome = Column(String)
        measurement_name = Column(String)
        measurement_value = Column(String)
        validator = Column(String)
        start = Column(BigInteger)
        end = Column(BigInteger)
        
    Session = sessionmaker(db)  
    session = Session()

    Base.metadata.create_all(db)
    #print('here')
    # Create 
    #    record_to_insert = ('testDUT1', 'One Plus 6', '1.0.0', 'this is a description', '20200430-HPES16', '2020-09-16 15:37:12.251000', 'operator', 'PASS', json.dumps(record_json))
    test_record = Parent()
    test_record.dut_id = record_dict['dut_id']
    if 'station_id' in record_dict['metadata']['config']:
        test_record.station_id = record_dict['metadata']['config']['station_id']
    if 'test_name' in record_dict['metadata']:
        test_record.test_name = record_dict['metadata']['test_name']
    if 'test_version' in record_dict['metadata']:
        test_record.test_version = record_dict['metadata']['test_version']
    if 'test_description' in record_dict['metadata']:
        test_record.test_description = record_dict['metadata']['test_description']
    test_record.test_date = datetime.datetime.fromtimestamp(record_dict['start_time_millis']/1000.0)
    if 'user_id' in record_dict['metadata']:
        test_record.user_id = record_dict['metadata']['user_id']
    test_duration = record_dict['end_time_millis']-record_dict['start_time_millis']
    #print('original :', test_duration)
    test_record.test_outcome = record_dict['outcome']
    test_record.record = record_dict
    trim_duration = 0

    for phase in record_dict['phases']:
        phase_name = phase['name']
        start_time_millis = phase['start_time_millis']
        end_time_millis = phase['end_time_millis']
        test_phase = Child()
        test_phase.name = phase_name
        test_phase.start = start_time_millis
        test_phase.end = end_time_millis
        test_phase.outcome = phase['outcome']
        test_record.children.append(test_phase)
        duration = end_time_millis - start_time_millis
        
        if phase_name == 'Test Complete':
            trim_duration = duration
            #print('trim: ', trim_duration)

        session.add(test_phase)
        for each in phase['measurements'].keys():
            run = Child()
            run.name = phase_name
            if 'outcome' in phase['measurements'][each]:
                run.outcome = phase['measurements'][each]['outcome']
            if 'name' in phase['measurements'][each]:
                run.measurement_name = phase['measurements'][each]['name']
            if 'measured_value' in phase['measurements'][each]:
                run.measurement_value = phase['measurements'][each]['measured_value']
            if 'validators' in phase['measurements'][each]:
                run.validator = phase['measurements'][each]['validators']
            try:
                run.start = int(start_time_millis)
            except:
                run.start = 0
            try:
                run.end = int(end_time_millis)
            except: 
                run.end = 0
            
            test_record.children.append(run)
            session.add(run)
    final = int(test_duration) - int(trim_duration)
    #print(final)
    test_record.test_duration = int(test_duration) - int(trim_duration)

    
    
    session.add(test_record)
    
    session.commit()
    

