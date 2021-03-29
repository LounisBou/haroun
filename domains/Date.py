#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Domaine Date : Librairie Haroune pour la gestion de la date et de l'heure.
#
#
# Dépendances :
#
# Import librairie execution de commande
import subprocess
#
# Class : Date.
class Date:
		
	# Fonctions : Actions
	
	# Action date 
	def datetime(self, format):	
		# Commande
		command = "date '+{format}'".format(format=format)
		# Ecécution de la Competence 
		# et récuperaction de la sortie standard
		# Version DEBUG : Sortie erreur redirigé vers sortie standard
		# result = subprocess.check_output([batcmd], stderr=subprocess.STDOUT)
		return subprocess.check_output(command, shell=True)
	
	# Action date 
	def date(self):		
		# Format 
		format = '%A %d %B %Y'
		# Commande
		command = "date '+{format}'".format(format=format)
		# Ecécution de la Competence 
		# et récuperaction de la sortie standard
		# Version DEBUG : Sortie erreur redirigé vers sortie standard
		# result = subprocess.check_output([batcmd], stderr=subprocess.STDOUT)
		return subprocess.check_output(command, shell=True)
		
	# Action heure 
	def heure(self):
		# Format 
		format = '%H heures %M minutes'
		# Commande
		command = "date '+{format}'".format(format=format)
		# Ecécution de la Competence 
		# et récuperaction de la sortie standard
		# Version DEBUG : Sortie erreur redirigé vers sortie standard
		# result = subprocess.check_output([batcmd], stderr=subprocess.STDOUT)
		return subprocess.check_output(command, shell=True)