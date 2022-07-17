#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import sys.path as syspath
from sys import path as syspath
# Import os.path and os.walk
from os import path, walk
# Import configparser.
from configparser import ConfigParser
# Import logging library
import logging
# Import peewee ORM.
from peewee import *
# Import peewee playhouse sqlite extension.
from playhouse.sqlite_ext import *
# Import datetime.datetime
from datetime import datetime
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
ROOT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
# Database declaration.
MY_DATABASE = SqliteDatabase(
  # Database filename.
  f"{ROOT_PATH}bdd/haroun.db",
  # Database options
  pragmas={
    # allow readers and writers to co-exist.
    'journal_mode': 'wal',
    # set page-cache size in KiB, e.g. -32000 = 32MB
    'cache_size': -1 * 64000,  # 64MB
    # enforce foreign-key constraints
    'foreign_keys': 1,
    # enforce CHECK constraints
    'ignore_check_constraints': 0,
    # let OS handle fsync (use with caution)
    'synchronous': 0
  }
)
#
class MyModel(Model): 
  
  # MyModel config dict.
  config = {}
  
  # Haroun config file path.
  haroun_config_file_path = f"{ROOT_PATH}config/Haroun.ini"
  
  # Check if config exist.
  if path.exists(haroun_config_file_path):
  
    # See configparser 
    configParser = ConfigParser()
  
    # Parse haroun.ini config file.
    configParser.read(haroun_config_file_path)
     
    # Get config parser sections.
    sections = configParser.sections()
    
    # Get all sections.
    for section_name in sections:
      config[section_name] = configParser[section_name]
    
  else:
    # [LOG]
    logging.critical(f"Fatal error : config file {haroun_config_file_path} doesn't exist.")
    # Exit program.
    quit()
  
  # Database reference.
  db = MY_DATABASE
  
  # Generic fields :
  
  # Primary key.
  id = AutoField()  # id will be auto-incrementing Primary Key.
  # Created datetime  
  created = DateTimeField(default=datetime.now)
  # Modified datetime
  modified = DateTimeField
  
  # Set logging level.
  logging.getLogger().setLevel(config['haroun']['LOG_LEVEL'])
    
  class Meta:
    
    """ MyModel specific configuration class Meta. """
  
    # Database.
    database = MY_DATABASE # MyModel use MY_DATABASE as database.
    
    # Table name.
    # Peewee will automatically infer the database table name from the name of the class. 
    # You can override the default name by specifying a table_name attribute
    #table_name = ''
     
  def save(self, *args, **kwargs):
    
    """ Override peewee save method """
    
    # Update instance modified field.
    self.modified = datetime.now()
    
    # Call peewee Model save method.
    return super(MyModel, self).save(*args, **kwargs)
    
  def force_update_schema(self):
    
    """ Delete table then create a new one based on actual schema. """
    
    # Create table
    self.create_table(
      # Specify IF NOT EXISTS clause.
      safe = False,
    )
    
  def backup():
    
    """ Create a backup of the database """
    
    # Create filename for backup with current date.
    filename = 'backup-%s.db' % (datetime.now())
    
    # Create database backup to file.
    MyModel.db.backup_to_file(filename)
    
  
class MemoryModel(MyModel):
  
    
  """ 
    Concept of Haroun MemoryModel. 
    Abstract class permanent memories and temporary context.
  """
  
  # MemoryModel info key.
  key = CharField()
  # MemoryModel info value.
  value = CharField()
  # MemoryModel.domain, define a specific domain MemoryModel info is reserved for.
  domain = CharField(null = True)
    
  class Meta:
    
    """ MemoryModel specific configuration class Meta. """
    
    # Table indexes.
    indexes = (
      # Create unique index on key/domain
      (('key', 'domain'), True),
    )
    
  @staticmethod
  def add(key, value, domain = None):
    
    """ 
      Add some info (key, value) to MemoryModel table.
      Update value if key already exist.
      ---
      Parameters 
        key : String
          MemoryModel key.
        value : String
          MemoryModel value.
        domain : String (optionnal)
          Domain name info is reserved for, by default MemoryModel info is for all domains. [Default = None]
      ---
      Return : Memory
        Created Memory Object.
    """
    
    # If exist.
    if MemoryModel.check(key, domain) :
      # Retrieve instance.
      instance = MemoryModel.get(key, domain)
      # Update value.
      instance.value = value
      # Save.
      instance.save()
    else:
      # Create instance.
      instance = MemoryModel.create(
        key=key, 
        value=value,
        domain=domain,
      )
      
    # Return created instance.
    return instance
    
  @staticmethod
  def remove(key, domain = None):
    
    """ 
      Remove specific info (key, value) from class table.
      ---
      Parameters 
        key : String
          MemoryModel key.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : Boolean
        MemoryModel found and deleted.
    """
    
    # Retrieve instance.
    instance = MemoryModel.get(key, domain)
    
    # If exist.
    if instance :
      instance.delete_instance()
      return True
    else:
      return False
  
  @staticmethod
  def get(key, domain = None):
    
    """ 
      Retrieve some info from class table using MemoryModel.key 
      ---
      Parameters 
        key : String
          MemoryModel key.
        domain : String (optionnal)
          Domain name info is reserved for, by default info is for all domains. [Default = None]
      ---
      Return : MemoryModel Class/None
        Corresponding MemoryModel Object, None if no matching result.
    """
    
    # Create query
    query = MemoryModel.select().where((MemoryModel.key == key) & (MemoryModel.domain == domain))
    
    # Check if no result.
    if query.exists() :
      for instance in query: 
        return instance
    else:
      return None
  
  @staticmethod
  def reverse_get(value, domain = None):
    
    """ 
      Retrieve some info from memory using Memory.value 
      ---
      Parameters 
        value : String
          MemoryModel value.
        domain : String (optionnal)
          Domain name info is reserved for, by default info is for all domains. [Default = None]
      ---
      Return : List
        Corresponding MemoryModel Objects in list, None if no matching result.
    """
    
    # Create query
    query = MemoryModel.select().where((MemoryModel.value == value) & (MemoryModel.domain == domain))
        
    # Check query have result.
    if query.exists():
      # Get query MemoryModel instances objects.
      instances = [intance for instance in query]
      return instances
    else:
      return None    
  
  @staticmethod
  def check(key, domain = None):
    
    """ 
      Check if some info exist in MemoryModel table using MemoryModel.key 
      ---
      Parameters 
        key : String
          MemoryModel key.
        domain : String (optionnal)
          Domain name info is reserved for, by default info is for all domains. [Default = None]
      ---
      Return : Boolean
        Corresponding MemoryModel Object exist.
    """
    
    # Create query
    query = MemoryModel.select().where((MemoryModel.key == key) & (MemoryModel.domain == domain))
    
    # Return exists value.
    return query.exists()
  
  @staticmethod
  def reverse_check(value, domain = None):
    
    """ 
      Check if some info exist in memory using Memory.value 
      ---
      Parameters 
        value : String
          MemoryModel value.
        domain : String (optionnal)
          Domain name info is reserved for, by default info is for all domains. [Default = None]
      ---
      Return : Memory
        Corresponding MemoryModel Object exist.
    """
    
    # Create query
    query = MemoryModel.select().where((MemoryModel.value == value) & (MemoryModel.domain == domain))
    
    # Return exists value.
    return query.exists()
    
