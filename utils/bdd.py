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
    
    """ Model-specific configuration class Meta. """
  
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
    
  