#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ! Imports :
#
# Import system library.
import sys
# Add parent directory to path.
sys.path.append('..')
# Import plex API.
from domains.Plex import Plex
# Import logging library
import logging
# 
#
def getPlexMovies():
        
    """ 
        Connect to Plex server via API. 
        ---
        Return PlexServer, None
            Return PlexServer object if connection successful, None otherwise.
    """
    
    # Get Plex domain instance.
    plex = Plex()
    # Check connection.
    if plex.server :
        # Search for all movies in Plex.
        movies = plex.server.library.section("Films").all()
        # Get movies titles.
        movies_titles = [Plex.clean_media_title(movie.title, True) for movie in movies]
        # Print movies titles.
        for movie_title in movies_titles:
            print(movie_title)


# Main.
getPlexMovies()
