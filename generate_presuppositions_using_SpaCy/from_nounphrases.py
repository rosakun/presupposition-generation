import re
import spacy
from from_relativeclauses import generate_pp
from generate_constituents import starts_with_vowel, regular_plural


"""
This is the main function that detects and generates presuppositions that are triggered by noun phrases in questions.
We differentiate between four such presupposition triggers:
    1) Presuppositions that are triggered by possessive constructions, i.e. "Mary's dog" -> "Mary has a dog".
    2) Presuppositions that are triggered by determiners, i.e. "the pizza place nearby" -> "There is a pizza place nearby".
    3) Presuppositions that are triggered by named entities, i.e. "we are in Spain" -> "There is a country called Spain."
    4) Presuppositions generated by other, 'generic' noun phrases, i.e. "firemen take Easter off" -> "There are firemen".
"""


def generate_presuppositions_from_nounphrases(doc):
    presuppositions = []
    docchunklist = list(doc.noun_chunks)
    for chunk in docchunklist:
        pos_list = [word.pos_ for word in chunk]
        if len(chunk) == 1 and chunk[0].pos_ == "PRON":
            pass
        elif "'s" in str(chunk):
            psp = generate_possessive_psp(chunk)
            presuppositions.append(psp)
        elif chunk[0].pos_ == "DET":
            psp = generate_determiner_psp(chunk)
            presuppositions.append(psp)
        elif "PROPN" in pos_list:
            psp = generate_entity_psp(doc,chunk)
            presuppositions.append(psp)
        else:
            psp = generate_generic_existential_psp(chunk)
            presuppositions.append(psp)
    return list(dict.fromkeys(presuppositions))



"""
This function handles the generation of 1) presuppositions that are triggered by possessive constructions, i.e. "Mary's dog" -> "Mary has a dog".
"""

def generate_possessive_psp(chunk):
    index = 0
    for word in chunk:
        if str(word) == "'s":
            break
        else:
            index += 1
    haver = str(chunk[:index]).capitalize()
    thing_had = chunk[(index+1):]
    if starts_with_vowel(thing_had[0]):
        psp = haver + " has an " + str(thing_had) + "."
    else:
        psp = haver + " has a " + str(thing_had) + "."
    if regular_plural(thing_had[-1]):
        psp = haver + " has " + str(thing_had) + "."
    return psp



"""
This function handles the generation of 2) presuppositions that are triggered by determiners, i.e. "the pizza place nearby" -> "There is a pizza place nearby".
"""

def generate_determiner_psp(chunk):
    if starts_with_vowel(chunk[1]):
        psp = "There is an " + str(chunk[1:]) + "." 
    else:
        psp = "There is a " + str(chunk[1:]) + "." 
    if regular_plural(chunk[-1]):
        psp = "There are " + str(chunk[1:]) + "."
    return psp



"""
This function handles the generation of 3) presuppositions that are triggered by named entities, i.e. "we are in Spain" -> "There is a country called Spain."
"""

def generate_entity_psp(doc,chunk):
    psp = ""
    for word in chunk:
        for ent in doc.ents:
            if str(word.text) in str(ent):
                wordtype = ent.label_
                if starts_with_vowel(str(wordtype)):
                    psp = "There is an " +  label_converter(wordtype) + " called " + str(chunk) + "." 
                else:
                    psp = "There is a " +  label_converter(wordtype) + " called " + str(chunk) + "."
    return psp



"""
This function handles the generation of 4) presuppositions generated by other, 'generic' noun phrases, i.e. "firemen take Easter off" -> "There are firemen".
"""


def generate_generic_existential_psp(chunk):
    if starts_with_vowel(chunk[0]):
        psp = "There is an " + str(chunk) + "."
    else:
        psp = "There is a " + str(chunk) + "."
    if regular_plural(chunk[-1]):
        psp = "There are " + str(chunk) + "."
    return psp



"""
This function converts Spacy NER labels into words that can be used in sentences.
"""

def label_converter(label):
    if label == "PERSON":
        return "person"
    elif label == "TIME":
        return "time"
    elif label == "ORG":
        return "company or organization"
    elif label == "GPE":
        return "country"
    elif label == "DATE":
        return "date"
    elif label == "EVENT":
        return "event"
    elif label == "FAC":
        return "facility"
    elif label == "NORP":
        return "group"
    else:
        return label