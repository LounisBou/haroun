#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import plex API.
from plexapi.server import PlexServer
# Import logging library
import logging
#
#
# Domain globals : 
#
# Needed slots list.
SLOTS_FILES = []
#
# 
class Plex(Domain):  
    
    def __init__(self):
    
        """ Class constructor. """
                
        # Init parent class Domain.
        super().__init__()
        
        # Plex server instance.
        self.plex = None

        # Initialisation.
        
        # Load config file.
        self.load_config()

        # Set variables.
        self.__set_variables()
        
        # Plex server connection.
        self.__connect()
    
    def __set_variables(self):

        """ Define Plex API infos from config file. """

        self.plex_server_url = self.config["plex"]["server_url"]
        self.plex_server_token = self.config["plex"]["server_token"]
        self.plex_movies_section = self.config["plex"]["movies_section"]
        self.plex_shows_section = self.config["plex"]["shows_section"]
        self.plex_client_name = self.config["plex"]["client_name"]
            
    def __connect(self):
        
        """ 
            Connect to Plex server via API. 
            ---
            Return Boolean
                Connection status.
        """
        
        try:
            # Connect to plex server using PLEX_SERVER_TOKEN.
            self.plex = PlexServer(self.plex_server_url, self.plex_server_token)
        except:
            self.plex = None
            return False

        # [LOG]
        if self.check_client(self.plex_client_name) :
            logging.info(f"Client {self.plex_client_name} available.")
        else:
            logging.warning(f"Client {self.plex_client_name} NOT available.")

        return True
        
    
    def __get_available_client(self):
        
        """ 
            Retrieve plex available client.
            ---
            Return List
                Plex clients list.
        """
        
        # Retrieve plex clients list.
        plex_clients = self.plex.clients()
        
        # [LOG]
        logging.debug(f"Plex available clients : {plex_clients}")
        
        # Return plex clients.
        return plex_clients
            
    def check_client(self, client_name):
        
        """ 
            Check if client with specified client_name is available. 
            ---
            Parameters
                client_name : String
                    Client name to check availability.
            ---
            Return Boolean
                Client is available.
        """
        
        # Retrieve plex available clients.
        plex_clients = self.__get_available_client()
        
        # Check all clients.
        for client in plex_clients:    
            # Check if client_name is in available clients list.
            if client_name == client.title :
                return True
        
        # Client not found.
        return False
        
    def get_client(self):
        
        """ 
            Retrieve plex client. 
            ---
            Return PlexClient
                Return the plex client.
        """    
        
        # Check for client availability.
        if not self.check_client(self.plex_client_name) :
            return f"Le client {self.plex_client_name} n'est pas disponible je ne peux rien faire, désolé."
        
        # Retrieve client.
        client = self.plex.client(self.plex_client_name)
        
        # return client.
        return client
        
    def play_client(self, media):
            
            """ Launch media on client. """
            
            # Retrieve client.
            client = self.get_client()
            
            try:
                # Play media on client.
                client.playMedia(media)
            except:
                return f"Le client {self.plex_client_name} n'est pas disponible je ne peux rien faire, désolé."
                
            # Return 
            return None
        
    def search(self, search_string, media_type = None):
        
        """ 
            Search for entry in plex database.
            ---
            Parameters
                search_string : String
            ---
            Return List
                List of plex Video matching search_string.
        """
        
        # List of matching videos title.
        matching_videos_titles = []
        
        # Make plex search
        for video in self.plex.search(search_string, media_type):
            # Retrieve movie title.
            matching_videos_titles.append(video.title)
            
        # Return matching movie title list
        return matching_videos_titles
            
    
    # ! - Methods.
    
    @Domain.check_api_connection("plex")
    @Domain.match_intent("plex.play_movie")
    def play_movie(self, orphan):
        
        # Get orphan as movie title.
        movie_title = orphan
        
        # Search for movie in Plex.
        matching_videos_titles = self.search(movie_title, 'movie')
        
        # If no movie found.
        if len(matching_videos_titles) == 0 :
            return f"Je n'ai pas trouvé de film correspondant à {movie_title} désolé."
        elif len(matching_videos_titles) == 1 :
            # Get correct movie title.
            correct_movie_title = matching_videos_titles[0]
            
            # Get movie to play.
            movie_to_play = self.plex.library.section(self.plex_movies_section).get(correct_movie_title)
                        
            # Say client to play movie.
            error = self.play_client(movie_to_play)
            if error :
                return error
        
            # Return response.
            return f"Je lance le film {correct_movie_title}"
        else:
            # Return list of available movie with this title match.
            response = f" J'ai trouvé plusieurs films qui peuvent correspondre à votre demande : "
            for movie_title in matching_videos_titles:
                response = response + f"{movie_title}, "
            response = response + f"pouvez-vous préciser lequel je dois lancer ?"
            # Return response.
            return response
    
    @Domain.check_api_connection("plex")
    @Domain.match_intent("plex.play_show")
    def play_show(self, orphan, season_number = None, episode_number = 1, mode = None):
        
        # Get orphan as show title.
        show_title = orphan
        
        # Search for show in Plex.
        matching_videos_titles = self.search(show_title, 'show')
        
        # If no movie found.
        if len(matching_videos_titles) == 0 :
            return f"Je n'ai pas trouvé de série correspondante à {show_title} désolé."
        elif len(matching_videos_titles) == 1 or show_title.capitalize() in matching_videos_titles :
        
            # Get correct show title.
            correct_show_title = matching_videos_titles[0]
            
            # Get show to play.
            show_to_play = self.plex.library.section(self.plex_shows_section).get(correct_show_title)
            
            # If ask for specific season
            if season_number :  
                
                # Var for matching episode.
                match_episode = None
            
                # Get show episodes.
                show_episodes = show_to_play.episodes()
                
                # Try to find the correct ask episode.
                for episode in show_episodes:
                    if int(episode.seasonNumber) == int(season_number) and int(episode.index) == int(episode_number) :
                        match_episode = episode
                
                # If episode not found.
                if not match_episode :
                    return f"Je n'ai pas trouvé l'épisode demandé."  
                
                # Say client to play episode.        
                error = self.play_client(match_episode)
                if error :
                    return error
                
                # Return response.
                return f"Je lance l'épisode {episode_number} de la saison {season_number} de {correct_show_title}"
                
            else:
                        
                # Say client to play show.
                error = self.play_client(show_to_play)
                if error :
                    return error
                
                # Return response.
                return f"Je lance la série {correct_show_title}"
                
        else:
        
            # Return list of available movie with this title match.
            response = f" J'ai trouvé plusieurs séries qui peuvent correspondre à votre demande : "
            for show_title in matching_videos_titles:
                response = response + f"{show_title}, "
            response = response + f"pouvez-vous préciser laquel je dois lancer ?"
            # Return response.
            return response
            
    @Domain.check_api_connection("plex")
    @Domain.match_intent("plex.play")
    def play(self):
        
        """" Ask client to play video """
        
        # Retrieve client.
        client = self.get_client()
        
        # Play
        client.play()
        
        # Return response.
        return f"Je relance la video."
        
    @Domain.check_api_connection("plex")
    @Domain.match_intent("plex.pause")
    def pause(self):
        
        """" Ask client to pause video """
        
        # Retrieve client.
        client = self.get_client()
        
        # Pause
        client.pause()
        
        # Return response.
        return f"Ok, je met sur pause."
        
    @Domain.check_api_connection("plex")
    @Domain.match_intent("plex.stop")
    def stop(self):
        
        """" Ask client to stop video """
        
        # Retrieve client.
        client = self.get_client()
        
        # Stop
        client.stop()
        
        # Return response.
        return f"Je coupe Plex."
