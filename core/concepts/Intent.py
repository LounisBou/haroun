#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import system library.
import sys
# Import OS library.
import os
#
#
# Globals :
#
# Current, parent, and root paths.
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
DOSSIER_RACINE = os.path.dirname(DOSSIER_PARENT)
sys.path.append(DOSSIER_RACINE)
#
#
#
class Intent: 
  
  """ Concept of Haroun Intent. """
  
  def __init__(self):
    
    """ Intent class constructor. """
    
    # Error flag.
    self.error = 0
    
