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
# Import logging library
import logging
#
#
class Context(MyModel): 
    
    """ 
        Concept of Haroun Context. 
        Allow to store value that can be shared between Intents.
        Context info (key, value) must be defined by Domains skills.
    """
    
    # Context info key.
    key = CharField()
    # Context info value.
    value = CharField()
    # Context domain, define a specific domain context info is reserved for.
    domain = CharField(null = True)
    # Context expiration date (store timestamp).
    expire = FloatField()
        
    class Meta:
    
        """ Model-specific configuration class Meta. """
    
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
        
        # Get expire date from duration.
        expire_date = datetime.now() + timedelta(minutes=duration)
        expire_timestamp = datetime.timestamp(expire_date)
        
        # If exist.
        if Context.check(key, domain) :
            # Retrieve.
            context = Context.get(key, domain)
            # Update value and expire.
            context.value = value
            context.expire = expire_timestamp
            # Save.
            context.save()
        else:
            # Create context entry.
            context = Context.create(
                key=key, 
                value=value,
                domain=domain,
                expire=expire_timestamp,
            )
        
        # [LOG]
        logging.debug(f"Context.add : key = {key}, value = {value}, domain = {domain}, duration = {duration}")

        # Return created context.
        return context
        
    @staticmethod
    def remove(key, domain = None):
        
        """ 
            Remove specific info (key, value) from context table.
            ---
            Parameters 
                key : String
                    Context key.
                domain : String (optionnal)
                    Domain name info is reserved for, by default context info is for all domains. [Default = None]
            ---
            Return : Boolean
                Context found and deleted.
        """
        
        # Retrieve context object.
        context = Context.get(key, domain)
        
        # [LOG]
        logging.debug(f"Context.remove : key = {key}, domain = {domain}")

        # If exist.
        if context :
            context.delete_instance()
            return True
        else:
            return False
    
    @staticmethod
    def get(key, domain = None):
        
        """ 
            Retrieve some info from context using Context.key 
            ---
            Parameters 
                key : String
                    Context key.
                domain : String (optionnal)
                    Domain name info is reserved for, by default context info is for all domains. [Default = None]
            ---
            Return : Context/None
                Context Object, None if no matching result.
        """
        
        # Get current timestamp.
        now_timestamp = datetime.timestamp(datetime.now())
        
        # Create select query
        query = Context.select().where((Context.key == key) & (Context.domain == domain) & (Context.expire > now_timestamp))
        
        # Check if no result.
        if query.exists() :
            for context in query: 
                return context
        else:
            return None
    
    @staticmethod
    def reverse_get(value, domain = None):
        
        """ 
            Retrieve some info from context using Context.value 
            ---
            Parameters 
                value : String
                    Context value.
                domain : String (optionnal)
                    Domain name info is reserved for, by default context info is for all domains. [Default = None]
            ---
            Return : List
                Contexts Object in list, None if no matching result.
        """
        
        # Get current timestamp.
        now_timestamp = datetime.timestamp(datetime.now())
        
        # Create query
        query = Context.select().where((Context.value == value) & (Context.domain == domain) & (Context.expire >now_timestamp))
        
        # Check query have result.
        if query.exists() :
            # Return query context objects.
            return [context for context in query]
        else :
            return None    
    
    @staticmethod
    def check(key, domain = None):
        
        """ 
            Check if some info exist in context using Context.key 
            ---
            Parameters 
                key : String
                    Context key.
                domain : String (optionnal)
                    Domain name info is reserved for, by default context info is for all domains. [Default = None]
            ---
            Return : Boolean
                Context Object exists.
        """

        # First clean expired context.
        Context.clean()
        
        # Get current timestamp.
        now_timestamp = datetime.timestamp(datetime.now())
        
        # Create query
        query = Context.select().where((Context.key == key) & (Context.domain == domain) & (Context.expire > now_timestamp))
        
        # Return query exists value.
        return query.exists()
    
    @staticmethod
    def reverse_check(value, domain = None):
        
        """ 
            Check if some info exist in context using Context.value 
            ---
            Parameters 
                value : String
                    Context value.
                domain : String (optionnal)
                    Domain name info is reserved for, by default context info is for all domains. [Default = None]
            ---
            Return : Boolean
                Context Object exists.
        """
        
        # Get current timestamp.
        now_timestamp = datetime.timestamp(datetime.now())
        
        # Create query
        query = Context.select().where((Context.value == value) & (Context.domain == domain) & (Context.expire > now_timestamp))
        
        # Return query exists value.
        return query.exists()
        
        
    @staticmethod
    def clean():
        
        """ 
            Search for expired context info and remove them from table. 
            ---
            return Int
                Number of rows removed.
        """
        
        # Get current timestamp.
        now_timestamp = datetime.timestamp(datetime.now())
        
        # Create delete query.
        query = Context.delete().where(Context.expire < now_timestamp)
        
        # Execute query
        nb_rows_deleted = query.execute()
        
        # Return 
        return nb_rows_deleted
        
        