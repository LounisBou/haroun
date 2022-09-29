#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ! Imports :
#
# Import os path.
from os import path
# Import system library.
from sys import path as syspath
# Import logging library
import logging
#
# Globals :
#
# Current, parent, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
PARENT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
ROOT_PATH = path.dirname(path.abspath(PARENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
# Import plex Domain.
from domains.Plex import Plex
# 
#
def getPlexMovies():
        
    """ 
        Connect to Plex server via Plex Domain and get all movies titles then print them.
    """
    
    # Get Plex domain instance.
    plex = Plex()

    # Get all medias titles.
    medias_titles = plex.get_all_medias("Films")

    # Print movies titles.
    for media_title in medias_titles:
        print(media_title)


# Main.
getPlexMovies()
