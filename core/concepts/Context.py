#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import peewee ORM.
from peewee import *
# Import Base utils.base (Peewee ORM connector)
from utils.bdd import MyModel
# Importe datetime.datatime and datetime.timedelta
from datetime import datetime, timedelta
#
class Context(MyModel): 
  
  """ 
    Concept of Haroun Context. 
    Allow to store value that can be shared between Intents.
    Context info (key, value) must be defined by Domains skills.
  """
  
  # Context info key.
  key = CharField(unique=True)
  # Context info value.
  value = CharField()
  # Context domain, define a specific domain context info is reserved for.
  domain = CharField()
  # Context expiration date.
  expire = DateTimeField
    
  def __init__(self):
    
    """ Memory class constructor. """
    
    # Init parent class Base.
    super().__init__()
    
  class Meta:
  
    # Table indexes.
    indexes = (
      # Create unique index on key/domain
      (('key', 'domain'), True),
    )
    
  @staticmethod
  def add(key, value, domain = None, duration = 60):
    
    """ 
      Add some info (key, value) to context table.
      Update value if key already exist.
      ---
      Parameters 
        key : String
          Context key.
        value : String
          Context value.
        domain : String (optionnal)
          Domain name info is reserved for, by default context info is for all domains. [Default = None]
        duration : Int (optionnal)
          Context duration in minutes [Default = 60].
      ---
      Return : Context
        Created Context Object.
    """
    
    # Create timedelta from duration.
    duration_delta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=duration, hours=0, weeks=0)
    
    # Get expire date from duration.
    expire = datetime.now() + duration_delta
    
    # Create context entry.
    context = Context.create(key=key, value=value, domain=domain, expire=expire)
    
    # Return created context.
    return context 
  
  @staticmethod
  def get(key, domain = None, max_age = 60):
    
    """ 
      Retrieve some info from context using Context.key 
      ---
      Parameters 
        key : String
          Context key.
        domain : String (optionnal)
          Domain name info is reserved for, by default context info is for all domains. [Default = None]
        max_age : Int (optionnal)
          Max age since creation in minutes. [Default = 60]
      ---
      Return : Context
        Corresponding Context Object.
    """
    
    pass
  
  @staticmethod
  def reverse_get(value, domain = None, max_age = 60):
    
    """ 
      Retrieve some info from context using Context.value 
      ---
      Parameters 
        value : String
          Context value.
        domain : String (optionnal)
          Domain name info is reserved for, by default context info is for all domains. [Default = None]
        max_age : Int (optionnal)
          Max age since creation in minutes. [Default = 60]
      ---
      Return : Context
        Corresponding Context Object.
    """
    
    pass
  
  @staticmethod
  def check(key, domain = None, max_age = 60):
    
    """ 
      Check if some info exist in context using Context.key 
      ---
      Parameters 
        key : String
          Context key.
        domain : String (optionnal)
          Domain name info is reserved for, by default context info is for all domains. [Default = None]
        max_age : Int (optionnal)
          Max age since creation in minutes. [Default = 60]
      ---
      Return : Boolean
        Corresponding Context Object exist.
    """
    
    pass
  
  @staticmethod
  def reverse_check(value, domain = None, max_age = 60):
    
    """ 
      Check if some info exist in context using Context.value 
      ---
      Parameters 
        key : String
          Context value.
        domain : String (optionnal)
          Domain name info is reserved for, by default context info is for all domains. [Default = None]
        max_age : Int (optionnal)
          Max age since creation in minutes. [Default = 60]
      ---
      Return : Context
        Corresponding Context Object exist.
    """
    
    pass
    
    
  @staticmethod
  def clean_context():
    
    """ Search for expired context info and remove them from table. """
    
   
    
    