#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import peewee ORM.
from peewee import *
# Import Base utils.base (Peewee ORM connector)
from utils.bdd import MyModel
#
class Memory(MyModel): 
  
  """ 
    Concept of Haroun Memory. 
    Memories are permanent memory information.
    It's like Memory infos but without expiration date.
  """
  
  # Memory info key.
  key = CharField()
  # Memory info value.
  value = CharField()
  # Memory domain, define a specific domain memory info is reserved for.
  domain = CharField(null = True)
    
  class Meta:
    
    """ Model-specific configuration class Meta. """
    
    # Table indexes.
    indexes = (
      # Create unique index on key/domain
      (('key', 'domain'), True),
    )
    
  @staticmethod
  def add(key, value, domain = None):
    
    """ 
      Add some info (key, value) to memory table.
      Update value if key already exist.
      ---
      Parameters 
        key : String
          Memory key.
        value : String
          Memory value.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : Memory
        Created Memory Object.
    """
    
    # If exist.
    if Memory.check(key, domain) :
      # Retrieve.
      memory = Memory.get(key, domain)
      # Update value.
      memory.value = value
      # Save.
      memory.save()
    else:
      # Create memory entry.
      memory = Memory.create(
        key=key, 
        value=value,
        domain=domain,
      )
      
    # Return created memory.
    return memory
    
  @staticmethod
  def remove(key, domain = None):
    
    """ 
      Remove specific info (key, value) from memory table.
      ---
      Parameters 
        key : String
          Memory key.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : Boolean
        Memory found and deleted.
    """
    
    # Retrieve memory object.
    memory = Memory.get(key, domain)
    
    # If exist.
    if memory :
      memory.delete_instance()
      return True
    else:
      return False
  
  @staticmethod
  def get(key, domain = None):
    
    """ 
      Retrieve some info from memory using Memory.key 
      ---
      Parameters 
        key : String
          Memory key.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : Memory/None
        Corresponding Memory Object, None if no matching result.
    """
    
    # Create query
    query = Memory.select().where((Memory.key == key) & (Memory.domain == domain))
    
    # Check if no result.
    if query.exists() :
      for memory in query: 
        return memory
    else:
      return None
  
  @staticmethod
  def reverse_get(value, domain = None):
    
    """ 
      Retrieve some info from memory using Memory.value 
      ---
      Parameters 
        value : String
          Memory value.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : List
        Corresponding Memorys Object in list, None if no matching result.
    """
    
    # Create query
    query = Memory.select().where((Memory.value == value) & (Memory.domain == domain))
        
    # Check query have result.
    if query.exists():
      # Get query memory objects.
      memories = [memory for memory in query]
      return memories
    else:
      return None    
  
  @staticmethod
  def check(key, domain = None):
    
    """ 
      Check if some info exist in memory using Memory.key 
      ---
      Parameters 
        key : String
          Memory key.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : Boolean
        Corresponding Memory Object exist.
    """
    
    # Create query
    query = Memory.select().where((Memory.key == key) & (Memory.domain == domain))
    
    # Return exists value.
    return query.exists()
  
  @staticmethod
  def reverse_check(value, domain = None):
    
    """ 
      Check if some info exist in memory using Memory.value 
      ---
      Parameters 
        value : String
          Memory value.
        domain : String (optionnal)
          Domain name info is reserved for, by default memory info is for all domains. [Default = None]
      ---
      Return : Memory
        Corresponding Memory Object exist.
    """
    
    # Create query
    query = Memory.select().where((Memory.value == value) & (Memory.domain == domain))
    
    # Return exists value.
    return query.exists()
    
    
    
    
    
   
    
    