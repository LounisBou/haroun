#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import system library.
import sys
# Import OS library.
from os import path
# Import Python Object Inspector library.
import inspect
# Import functools wraps for decorators.
from functools import wraps
#
#
# Globals :
#
# Current, parent, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
PARENT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
ROOT_PATH = path.dirname(path.abspath(PARENT_PATH))+'/'
sys.path.append(ROOT_PATH)
import domains
#
#
#
class Domain:
  
  """ Concept of Haroun Domain. """
  
  # Static variables :
  
  # Store intents handlers for each instanciate domains
  intents_handlers = {}
  
  # Fonction : Constructeur
  def __init__(self):
    
    """ __init__ : Domain class constructor. """ 
    
    # Slots entries.
    self.slots_entries = {}  
    
  @staticmethod
  def __get_slot(slot_file_name):
    
    """ 
      Acquire a slot file and return all slot entries in dict. 
      ---
      Parameters 
        slot_file_name : String 
          Slot file name
      ---
      Return : Dict
        Dict of Slots in file.
    """
    
    # Slots directory path.
    slots_path=ROOT_PATH+"slots/"
    
    """ Create slot entries dict from slot file. """
    
    # Slot entries dict.
    slot_entries = {}

    # Construct file path.
    slot_file_path = slots_path+slot_file_name
      
    # Retrieve slot file content.
    with open(slot_file_path) as fileBuffer:
      
      # Read file lines. 
      fileLines = fileBuffer.readlines()
      
      # For each lines.
      for line in fileLines :
        
        # Split line on ':'
        entry_parts = line.split(':')
        
        # If split is ok.
        if len(entry_parts) == 2 :
        
          # Create slot_entry_key from second part.
          slot_entry_key = entry_parts[1].strip().replace("(", "").replace(")", "")
          slot_entry_key = slot_entry_key.strip()
          
          # Create slot_entry_value from second part.
          slot_entry_value = entry_parts[0].strip().replace("(", "").replace(")", "")
          slot_entry_value = slot_entry_value.split('|')
          slot_entry_value = slot_entry_value[0]
          slot_entry_value = slot_entry_value.replace("[", "").replace("]", "")
          slot_entry_value = slot_entry_value.strip()
          
          # Set second part as key, first part as value.
          slot_entries[slot_entry_key] = slot_entry_value
          
        else :
          # [DEBUG]
          print(f"Slot line can't be interpreted. File slot {slot_file_name} error on : {line}")
    
    # Return slot_entries
    return slot_entries
    
  def get_slots_entries(self, slots_files_names):
    
    """
      Retrieve slots entries from specified slots files names.
      Add entries to self.slots_entries.
      ---
      Parameters
        slots_files_names : List
          List of slots files names to import.
    """
    
    # Retrieve slots entries for each specified files.
    for slot_file_name in slots_files_names :
    
      # Use Domain static method getSlot to get slot file entries.
      slot_entries = Domain.__get_slot(slot_file_name)
      
      # [DEBUG]
      #print(f"Slot file {slot_file_name} entries : {slot_entries}")
      
      # Add slot_entries to self.slots_entries dict.
      self.slots_entries.update(slot_entries)
    
  def methodGetArgs(self, method_name):
    
    """
      methodGetArgs : Get methods arguments list as tuple.
      ---
      Parameters : 
        method_name : String
          Method name in domain instance.
      ---
      Return Tuple
        Method arguments.
    """ 
    
    # Get Skill method.
    method = getattr(self, method_name)
    
    # Retrieve method arguments.
    args = inspect.getargspec(method).args
    
    # [DEBUG]
    #print(f"{method_name} args : {args}")
    
    # Return methods args.
    return args
    
  
  def executeSkill(self, skill):
    
    """
      executeSkill : Execute the skill on a domain class method.
      ---
      Parameters : 
        skill : Skill
          Skill to execute.
      ---
      Return skill : modified skill.
    """ 
    
    # Get methods.
    method = getattr(self, skill.method_name)
    
    # [DEBUG]
    print(f"Skills parameters = {skill.parameters}")
    
    # Execute methods with skill parameters
    skill.return_values = method(**skill.parameters)
    
    # Return modified skill
    return skill
  
  @staticmethod
  def register_handled_intent(module_name, class_name, method_name, intent_name):
    
    """
      Register domain method that handle an intent with Skill.match_intent decorator.
      ---
      Parameters
        module_name : String
           Domain module name that match the intent.
        class_name : String
           Domain class name that match the intent.
        method_name : String
          Domain method name that match the intent.
        intent_name : String
          Name of the intent to match.
    """
    
    # [DEBUG]
    #print(f"Preparing intent handler for {Domain.loading_domain_name}")
        
    # If intent_name entry don't exist. 
    if intent_name not in Domain.intents_handlers.keys() :
      # Create intent handler entry in intents_handlers.
      Domain.intents_handlers[intent_name] = {
        "module" : module_name,
        "class" : class_name,
        "method" : method_name,
      }
      # [DEBUG]
      #print(f"Register {Domain.loading_domain_name}.{method_name} as handling {intent_name}")
    else:    
      # [DEBUG]
      #print(f"Intent handler for {intent_name} already exist !")  
      pass
    
    
    
  # ! Decorators :
  
  @staticmethod
  def match_intent(intent_name):
    
    """
      Decorator that allow a domain method to match a specific intent.
      ---
      Parameters
        intent_name : String
          Name of intent to match.
      ---
      Return Function
        Decorator inner function.
    """
    
    def inner_function(function):
      
      """
        inner_function that received the original function in parameters.
        --- 
        Parameters
          function : Function
            Domain method on which the decorator was applied.
        ---
        Return Function
          Decorator function wrapper
      """
    
      @wraps(function)
      def wrapper(self_instance, *args, **kwargs):
        
        """
          match_intent wrapper function. Execute decorator code.
          ---
          Parameters
            self_instance : Class instance
              Domain instance on which method have been called.
            *args : List
              List of arguments pass on function call.
            *kargs : Dict
              Dict of arguments_names : arguments pass on function call.
          ---
          Return : result of function call.
        """
        
        # [DEBUG]
        #print(f"Intent name : {intent_name}")
        #print(f"Instance : {self_instance}")
        #print(f"args :  {args}")
        #print(f"kwargs : {kwargs}")
        #print(f"Before Calling {function.__name__}")
        
        # Call the original function.
        result = function(self_instance, *args, **kwargs)
        
        # [DEBUG]
        #print(f"After Calling {function.__name__}")
        
        # Return result.
        return result
      
      # Try to maintain method signature.
      wrapper.__signature__ = inspect.signature(function)  # the magic is here!
      
      # Get all function infos for registering intent handler.
      module_name = function.__module__.split('.')[1]
      class_name = function.__qualname__.split('.')[0]
      method_name = function.__qualname__.split('.')[1]
      
      # [DEBUG]
      print(f"Intent {intent_name} : handling by {module_name}.{class_name}.{method_name}")
           
      # Registering function as intent handler.
      Domain.register_handled_intent(module_name, class_name, method_name, intent_name)
            
      # Return the wrapper function.
      return wrapper
          
    # Return inner_function
    return inner_function
  


