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
  
  """ Concept of Haroun Memory. """
  
  # Define Model schema.
  key = CharField(unique=True)
  value = CharField()
    
  def __init__(self):
    
    """ Memory class constructor. """
    
    # Init parent class Base.
    super().__init__()
    
    
    
   
    
    