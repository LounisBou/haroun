#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ! Imports :
# Import math library.
import math
# ! Globals :

# Start.
START_INT = 0
STOP_INT = 100

# Numbers words language traduction.
lang = {
    'numerals' : {
        0 : "zero",
        1 : "un",
        2 : "deux",
        3 : "trois",
        4 : "quatre",
        5 : "cinq",
        6 : "six",
        7 : "sept",
        8 : "huit",
        9 : "neuf",
        10 : "dix",
        11 : "onze",
        12 : "douze",
        13 : "treize",
        14 : "quatorze",
        15 : "quinze",
        16 : "seize",
        17 : "dix-sept",
        18 : "dix-huit",
        19 : "dix-neuf",
        20 : "vingt",
        30 : "trente",
        40 : "quarante",
        50 : "cinquante",
        60 : "soixante",
        70 : "soixante-dix",
        71 : "soixante-et-onze",
        72 : "soixante-douze",
        73 : "soixante-treize",
        74 : "soixante-quatorze",
        75 : "soixante-quinze",
        76 : "soixante-seize",
        77 : "soixante-dix-sept",
        78 : "soixante-dix-huit",
        79 : "soixante-dix-neuf",
        80 : "quatre-vingts",
        81 : "quatre-vingt-un",
        82 : "quatre-vingt-deux",
        83 : "quatre-vingt-trois",
        84 : "quatre-vingt-quatre",
        85 : "quatre-vingt-cinq",
        86 : "quatre-vingt-six",
        87 : "quatre-vingt-sept",
        88 : "quatre-vingt-huit",
        89 : "quatre-vingt-neuf",
        90 : "quatre-vingt-dix",
        91 : "quatre-vingt-onze",
        92 : "quatre-vingt-douze",
        93 : "quatre-vingt-treize",
        94 : "quatre-vingt-quatorze",
        95 : "quatre-vingt-quinze",
        96 : "quatre-vingt-seize",
        97 : "quatre-vingt-dix-sept",
        98 : "quatre-vingt-dix-huit",
        99 : "quatre-vingt-dix-neuf",
        100 : "cent",
        1000 : "mille",
        1000000 : "million",
        1000000000 : "millard",
        1000000000000 : "billion",
        1000000000000000 : "billiard",
        1000000000000000000 : "trillion",
        1000000000000000000000 : "trilliard",
        1000000000000000000000000 : "quadrillion",
        1000000000000000000000000000 : "quadrilliard",
    },
}


# ! Fonctions :

def numberToLetter(number):
    
    """
        numberToLetter : Convert int number format to string number format.
    """
    
    # Define a string that will contains number in letters.
    numberString = ""
    
    # Get language int list.
    langNumeralInt = list(lang["numerals"].keys())
    
    # Variable to store the previous numeral int for control.
    previousNumeralInt = None
    
    # Check if number is zero.
    if number == 0 :
        # Return zero string.
        return lang["numerals"][number]
    
    # For each language int numeral entry.
    for numeralInt in reversed(langNumeralInt) :
        
        # Check if number is over this numeral.
        if number >= numeralInt : 
            
            
            
            # Reset spacer.
            spacer = ""
            
            # If numberString not empty add spacer.
            if numberString :
                # if numeralInt is one.
                if numeralInt == 1  and previousNumeralInt < 70 :
                    # Spacer is dash and 'et'.
                    spacer = "-et-"
                else:
                    # if number between 2 and 9 (included) and previous numeral int under 100.
                    if number > 1 and number < 10 and previousNumeralInt < 100 :
                        # Spacer is dash.
                        spacer = "-"
                    else:
                        # Spacer is space.
                        spacer = " "
            
            # More than 20.
            if numeralInt > 20 :
            
                # Get the remainder part of the number
                remainder = number % numeralInt
                
                # Count number of times this number contains this numeral.
                numeralIntTimes = number // numeralInt
                
                # If numeralIntTimes more than 20.
                if numeralIntTimes > 20 :
                    # Then call numberToLetter recursively.
                    numeralIntTimesString = numberToLetter(numeralIntTimes)
                else:
                    # Get numeralIntTimes in string.
                    numeralIntTimesString = lang["numerals"][numeralIntTimes]
                
                # Get numeral string.
                numeralString = lang["numerals"][numeralInt]
                                
                # Add numeralIntTimesString if numeralIntTimes is more than 1.
                if numeralIntTimes > 1 :
                    # If numeralInt is 100 and number over or equal thousand.
                    if ( numeralInt == 100 or numeralInt > 1000 ) and number >= 1000 :
                        # add 's' (plurial) to numralString
                        numeralString += 's'
                    # If numeralInt is 100 and there is no remainder.
                    elif numeralInt == 100 and remainder == 0 :
                        # add 's' (plurial) to numralString
                        numeralString += 's'
                    # Add string part to number string.
                    numberString += f"{spacer}{numeralIntTimesString} {numeralString}"
                else:
                    # If numeralInt over or equal million.
                    if numeralInt >= 1000000 :
                        # Add string part to number string.
                        numberString += f"{spacer}{numeralIntTimesString} {numeralString}"
                    else:
                        # Add string part to number string.
                        numberString += f"{spacer}{numeralString}"
                    
                # Override number with remainder.
                number = remainder
                
            # Between 0 and 20.
            elif numeralInt > 0 :
                
                # Get numeral string.
                numeralString = lang["numerals"][numeralInt]
                # Add string part to number string.
                numberString += f"{spacer}{numeralString}"
                # Get the remainder part of the number
                number = number - numeralInt
                                
            else:
                
                # End.
                numberString.strip()
            
            # Save numeral int.
            previousNumeralInt = numeralInt
            
        # End for reversed(langNumeralInt)
            
    # Retun number string.
    return numberString

def getSlot(number):
    
    """
        getSlot : Convert range of numbers to string number format.
        ---
        Parameters
            number : Int
                Number to return slot.
        ---
        Return : String
            Number slot entry.
    """
    
     # Slot entry var.
    slot_entry = ""

    # Convert number to string.
    number_string = numberToLetter(number)
    # Number int with thousand separator.
    number_int_formated = format(number, ',d').replace(',',' ')
    number_string_formated = number_string.replace('-', ' ')
    
    # Create slot entry.
    slot_entry += "("
    
    # Add number to slot.
    slot_entry += f"{number}"
    
    # if number_formated not like number.
    if str(number) != number_int_formated :
        # Add number_int_formated to slot.
        slot_entry += f" | {number_int_formated}"
        
    # Add number string.
    slot_entry += f" | {number_string}"
    
    # if number_string_formated is no like number_string
    if number_string != number_string_formated :
        # Add number_string_formated to slot.
        slot_entry += f" | {number_string_formated}"
    
    # End of slot entry and number and slot key.
    slot_entry += f"):({number})"
    
    # Return slot entry string.
    return slot_entry

def createSlotFile(start, end, step = 1):
    
    """
        createSlotFile : Convert range of numbers to string number format.
        ---
        Parameters
            start : Int
                Start of range.
            end : Int
                End of range include.
            step : Int
                Value which determines the increment between each integer in the sequence.
        ---
        Return : None
    """
        
    # For number in range.
    for number in range(start, end+1, step):
        # Get slot.
        slot_entry = getSlot(number)
        # Print slot.
        print(f"{slot_entry}")
            
# ! Execution :

# Convert range.
createSlotFile(START_INT, STOP_INT)
createSlotFile(110, 1000, 10)
createSlotFile(1100, 10000, 100)
