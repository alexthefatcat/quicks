# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:44:51 2026

@author: alexm
"""


def cleaned_splitlines(text: str, ignore_comment_lines: bool = True, ignore_comments: bool = True, isin: str | None = None, strip_speachmarks: bool = False) -> list[str]:
    lines = []
    for line in text.splitlines():
        if ignore_comments:
            line = line.split('#')[0]        
        cleaned = line.strip()
        if len(cleaned)==0:
            continue
        if ignore_comment_lines and cleaned.startswith("#"):
            continue
        if isin is not None and not isin in cleaned:
            continue
        if strip_speachmarks:
            line = line.strip('"' + "'")
        lines.append(cleaned)
    return lines


pokemon_text = '''

    ##Pokemon
        # Water
            Squirtle
            Vaporeon
            Psyduck
            Magikarp #  worst one
            Totodile
    
        # Grass
            Bulbasaur
            Chikorita
            Sceptile
            Leafeon
            Oddish
        
        # Normal
            Snorlax
            Eevee
            Meowth
            Ditto
            Jigglypuff
            Mew  # Best


'''   
pokemon = cleaned_splitlines(pokemon_text)

pokemon_out =         [  'Squirtle',
                         'Vaporeon',
                         'Psyduck',
                         'Magikarp',
                         'Totodile',
                         'Bulbasaur',
                         'Chikorita',
                         'Sceptile',
                         'Leafeon',
                         'Oddish',
                         'Snorlax',
                         'Eevee',
                         'Meowth',
                         'Ditto',
                         'Jigglypuff',
                         'Mew']