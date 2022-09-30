#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import plex API server.
from plexapi.server import PlexServer
# Import logging library
import logging
#
#
# 
class Plex(Domain):  
    
    def __init__(self):
    
        """ Class constructor. """
                
        # Init parent class Domain.
        super().__init__()
        
        # Plex server instance.
        self.server = None

         # Plex account instance.
        self.account = None

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
                Connection plex server connection status.
        """
        
        try:
            # Connect to plex server using PLEX_SERVER_TOKEN.
            self.server = PlexServer(self.plex_server_url, self.plex_server_token)
        except:
            # [LOG]
            logging.error("Plex server connection failed.")
            self.server = None

        # [LOG]
        if not self.check_client(self.plex_client_name) :
            logging.warning(f"Client {self.plex_client_name} not available.\n")

        # Return boolean plex server connection status.
        return self.server is not None
        
    
    def __get_available_client(self):
        
        """ 
            Retrieve plex available client.
            ---
            Return List
                Plex clients list.
        """
        
        # Retrieve plex clients list.
        plex_clients = self.server.clients()
        
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
        client = self.server.client(self.plex_client_name)
        
        # return client.
        return client
        
    def play_client(self, media):
            
        """ Launch media on client. """
        
        # Play retry counter.
        play_retry = 0

        # Play max retry.
        try:
            play_max_retry = int(self.config["plex"]["play_max_retry"])
        except:
            play_max_retry = 2

        # Retrieve client.
        client = self.get_client()

        try:
            # Reload client connection.
            client.connect()
            # Play media on client.
            played = client.playMedia(media)
            # Retry if media not played.
            while play_retry <= play_max_retry and not client.isPlayingMedia() :
                # Retry play media on client.
                played = client.playMedia(media)
                # Increment play retry counter.
                play_retry += 1
        except:
            return f"Le client {self.plex_client_name} n'est pas disponible je ne peux rien faire, désolé."
            
        # Return 
        return played
        
    def search(self, media_type, search_string):
        
        """ 
            Search for entry in plex database.
            ---
            Parameters
                media_type : String
                    Media type to search in plex database.
                search_string : String
                    String to search in plex database.
            ---
            Return List
                List of plex media matching search_string.
        """
        
        # List of matching media title.
        matching_media_titles = []
        
        # Make plex search
        for media in self.server.search(search_string, media_type):
            # Retrieve media title.
            matching_media_titles.append(media.title)
            
        # Return matching media title list
        return matching_media_titles

    def search_match(self, media_title, media_type):
        
        """ 
            Make search and check if search retrun match asked media.
            ---
            Parameters
                media_type : String
                    Media type to search.
                media_title : String
                    Media title to find.
            ---
            Return Boolean, String
                Plex media find.
        """
        
        # Make plex search
        matching_media_titles = self.server.search(media_type, media_title)

        # One media found.
        if len(matching_media_titles) == 1 :
            # Return media title.
            return True, matching_media_titles[0]
        
        # No media found.
        elif len(matching_media_titles) == 0 :
            # Return None.
            return False, None
        
        # Multiple media found.
        else :
            # Check if one match media title.
            for media in matching_media_titles:
                if media.title == media_title :
                    return True, media.title
            
            # No match video title return all.
            return False, Plex.create_media_list(matching_media_titles)
        

    @staticmethod
    def create_media_list(media_titles):
        
        """ 
            Create media string list for user to choose.
            ---
            Parameters
                media_titles : List
                    List of media title.
            ---
            Return String
                String list of plex media title.
        """

        # Media string list.
        string_list = ""
        
        # Create media list.
        for title in media_titles:
            string_list += f"{title}, "
            
        # Return matching media title list
        return string_list
    
    def get_all_medias(self, library_section):
        
        """ 
            Connect to Plex server via API. 
            ---
            Parameters
                library_section : String
                    Plex library section to retrieve.
            ---
            Return List
                List of plex medias title in library section.
        """
        
        # Check connection.
        if self.server :
            # Search for all section medias in Plex.
            medias = self.server.library.section(library_section).all()
            # Get medias titles.
            medias_titles = [Plex.clean_media_title(media.title, True) for media in medias]

        # Return medias titles.
        return medias_titles

    @staticmethod
    def clean_media_title(media_title, slot_value=True):

        """
            Clean media title.
            ---
            Parameters
                media_title : String
                    Media title to clean.
                slot_value : Boolean
                    If True, clean media title for slot value.
            ---
            Return str
                Return media title cleaned.
        """

        # Lower case media title.
        media_title = f" {media_title.lower()} "

        # String to replace by specified string.
        strings_to_replace = {
            "#": " ",
            "&": "et",
            "!" : " ",
            "/": " ",
            ":": " ",
            "·": " ",
            "-": " ",
            "…": " ",
            "...": " ",
            ".": "",
            "ë": "e",
            ",": " ",
            "\xa0" : " ",
            " i " : " 1 ",
            " ii " : " 2 ",
            " iii " : " 3 ",
            " iv " : " 4 ",
            " v " : " 5 ",
            " vi " : " 6 ",
            " vii " : " 7 ",
            " viii " : " 8 ",
            " ix " : " 9 ",
        }

        # Facultative strings.
        facultative_strings = {
            # Definite article
            " le " : " [le] ",
            " la " : " [la] ",
            " les " : " [les] ",
            " un " : " [un] ",
            " une " : " [une] ",
            " des " : " [des] ",
            " du " : " [du] ",
            " de " : " [de] ",
            " au " : " [au] ",
            " aux " : " [aux] ",
            " a " : " [a] ",
            " à " : " [à] ",
            " en " : " [en] ",
            " et " : " [et] ",
            " ou " : " [ou] ",
            " sur " : " [sur] ",
            " dans " : " [dans] ",
            " par " : " [par] ",
            " pour " : " [pour] ",
            " avec " : " [avec] ",
            " the " : " [the] ",
            # Definite article with apostrophe
            "'s" : "['s]",
            "d'" : "[d']",
            "n'" : "[n']",
            "l'" : "[l']",
            # Optional words
            " épisode " : " [épisode] ",
        }

        # Clean media title.
        [media_title := media_title.replace(string, replacement) for string, replacement in strings_to_replace.items() if string in media_title]
        # If slot_value is True, clean media title for slot value.
        if slot_value:
            # Add facultative strings.
            [media_title := media_title.replace(string, replacement) for string, replacement in facultative_strings.items() if string in media_title]

        # Remove double spaces.
        media_title = " ".join(media_title.split())

        # Return cleaned media title.
        return media_title

    @staticmethod
    def clean_medias_titles(medias_titles):

        """
            Clean medias titles.
            ---
            Return List
                Return medias titles cleaned.
        """

        # Return cleaned medias titles.
        return [Plex.clean_media_title(media_title) for media_title in medias_titles]

    
    # ! - Methods.
    
    @Domain.check_api_connection("server")
    @Domain.match_intent("plex.play_media")
    def play_media(self, media_type = None, media_title = None, season_number = None, episode_number = None, orphan = None):

        """
            Play media on Plex client.
            ---
            Parameters
                media_type : String
                    Media type to play.
                media_title : String
                    Media title to play.
                orphan : String
                    Orphan slot value.
            ---
            Return String
                Response.
        """

        # If we have no media type.
        if media_type is None:

            # Create context.
            self.set_context_intent("plex.play_media", {})
            # Return response.
            return self.say("plex.play_media.get_media_type")
            
        # If we have media but no media title.
        elif media_title is None:

            # Create context.
            self.set_context_intent("plex.play_media", {"media_type": media_type})

            # Ask for media title.
            return self.say(
                "plex.play_media.get_title",
                media_type = self.get_slot(media_type)
            )

        # If we have media type and media title.
        else:
            
            # Check for media title in Plex library.
            media_found, found_media_title = self.search_match(media_type, media_title)

            # If media is identify.
            if media_found:

                # If media type is movie.
                if media_type == "movie":
                    # Get movie to play.
                    media = self.server.library.section(self.plex_movies_section).get(found_media_title)
                elif media_type == "show":
                    # Get show to play.
                    media = self.server.library.section(self.plex_shows_section).get(found_media_title)
                
                # Play media.
                self.play_client(media)

                # Return dialog response.
                return self.say("plex.play_media.found", media_title = found_media_title)
            
            # If media is not identify.
            else:

                # No media found.
                if found_media_title is None:
                    # Return dialog response.
                    return self.say("plex.play_media.not_found", media_title = media_title)
                # Multiple medias found.
                else:
                    # Return dialog response.
                    return self.say(
                        "plex.play_media.found_multiple",
                        media_type = self.get_slot(media_type),
                        medias_titles = found_media_title
                    )




        

    @Domain.check_api_connection("server")
    @Domain.match_intent("plex.play_movie")
    def play_movie(self, movie_title = None, orphan = None):
        
        # Check if movie title is provided.
        if movie_title:
            # Search for movie in Plex.
            matching_videos_titles = self.search(movie_title, 'movie')
        # If no movie title provided.
        else:
            # Create context.
            self.set_context_intent("plex.play_movie", {})
            # Get dialog response.
            response = self.dialog.say("plex.play_movie.movie_title")
            # Return response.
            return response
        
        # If no movie found.
        if len(matching_videos_titles) == 0 :
            
            # Get dialog response.
            response = self.dialog.say("plex.play_movie.not_found")

            # Return response.
            return response.format(movie_title = movie_title)

        # If just one movie found.
        elif len(matching_videos_titles) == 1 :

            # Get correct movie title.
            correct_movie_title = matching_videos_titles[0]
            
            # Get movie to play.
            movie_to_play = self.server.library.section(self.plex_movies_section).get(correct_movie_title)
                        
            # Say client to play movie.
            error = self.play_client(movie_to_play)

            # [LOG]
            logging.info(f"Playing movie {correct_movie_title} on client {self.plex_client_name}.")
            logging.info(f"movie_to_play : {movie_to_play}")
            logging.info(f"Error : {error}")

            # Check if error.
            if error :
                # Set error message as response.
                response = error
            else:
                # Get dialog response.
                response = self.say("plex.play_movie.found", movie_title = correct_movie_title)
            
            # Return response.
            return response

        # If more than one movie found.
        else:

            # Create context.
            self.set_context_intent("plex.play_movie", {})

            # Return dialog response.
            return self.say(
                "plex.play_movie.found_multiple", 
                movies_titles = Plex.create_video_list(matching_videos_titles)
            )


    @Domain.check_api_connection("server")
    @Domain.match_intent("plex.play_show")
    def play_show(self, show_title = None, season_number = None, episode_number = 1, mode = None, orphan = None):        
        
        # Check if show title is provided.
        if show_title:
            # Search for show in Plex.
            matching_videos_titles = self.search(show_title, 'show')
        else:
            # Create context.
            self.set_context_intent("plex.play_show", {})
            # Return dialog response.
            return self.say("plex.play_show.show_title")

        # If no show found.
        if len(matching_videos_titles) == 0 :
            # Return dialog response.
            return self.say("plex.show.not_found", show_title = show_title)

        # If just one show found.
        elif len(matching_videos_titles) == 1 or show_title.capitalize() in matching_videos_titles :
            
            # Get correct show title.
            correct_show_title = matching_videos_titles[0]
            
            # Get show to play.
            show_to_play = self.server.library.section(self.plex_shows_section).get(correct_show_title)
            
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
                    # Return dialog response.
                    return self.say(
                        "plex.show.episode_not_found",
                        show_title = correct_show_title, 
                        episode_number = episode_number, 
                        season_number = season_number
                    )
                
                # Say client to play episode.        
                error = self.play_client(match_episode)
                if error :
                    return error
                
                # Return dialog response.
                return self.say(
                    "plex.show.found",
                    show_title = correct_show_title, 
                    episode_number = episode_number, 
                    season_number = season_number
                )
                
            else:
                        
                # Say client to play show.
                error = self.play_client(show_to_play)
                if error :
                    return error
                
                # Return dialog response.
                return self.say(
                    "plex.show.found",
                    show_title = correct_show_title, 
                    episode_number = episode_number, 
                    season_number = season_number
                )

        # If more than one show found.     
        else:
            
            # Create context.
            self.set_context_intent("plex.play_show", {})
        
            # List of available show with this title match.
            shows_titles = ""
            for show_title in matching_videos_titles:
                shows_titles = shows_titles + f"{show_title}, "
            
            # Return dialog response.
            return self.say("plex.show.found_multiple", shows_titles = shows_titles)


    @Domain.check_api_connection("server")
    @Domain.match_intent("plex.play")
    def play(self):
        
        """" Ask client to play video """
        
        # Retrieve client.
        client = self.get_client()
        
        # Play
        client.play()
        
        # Return response.
        response = self.dialog.get_dialog("plex.play")
        return response


    @Domain.check_api_connection("server")
    @Domain.match_intent("plex.pause")
    def pause(self):
        
        """" Ask client to pause video """
        
        # Retrieve client.
        client = self.get_client()
        
        # Pause
        client.pause()
        
        # Return response.
        response = self.dialog.get_dialog("plex.pause")
        return response


    @Domain.check_api_connection("server")
    @Domain.match_intent("plex.stop")
    def stop(self):
        
        """" Ask client to stop video """
        
        # Retrieve client.
        client = self.get_client()
        
        # Stop
        client.stop()
        
        # Return response.
        response = self.dialog.get_dialog("plex.stop")
        return response
