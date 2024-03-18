import spacy
from hilfsfunktionen import starts_with_vowel
from hilfsfunktionen import regular_plural
import re
from sentence_splitter import SentenceSplitter
spacy_model = spacy.load("en_core_web_sm")
splitter = SentenceSplitter(language='en')

def convert_first_second_person(word):
    if word == "I’m":
        return "they're"
    if word == 'I':
        return "they"
    if word == "I’ve":
        return "they've"
    if word == "you":
        return "their partner"
    if word == 'am':
        return 'are'
    if word == 'my':
        return 'their'
    if word == 'was':
        return 'were'
    else:
        return word

def find_dep(token):
    dep = [(token.text,token.dep_)]
    for child in token.children:
        dep.append((child.text,child.dep_))
    return dep

def is_tag_question(question):
    question = question.strip(" ")
    return question in ["True?","Is that fair?","Do you agree?","Right?","Correct?","Are you with me?","Okay?"]

def is_cc(word):
    return word in ["and","And","but","But","So,","Well,","Then,","Then","Now,","And,"]

# Find parts of each phrase to prune, and remove them from doc_list.
# !!! Only use the sentences you really want to extract, i.e. the ones followed by 'Right?', 'You see?'.
# Piece together a sentence from the words remaining in doc_list.
def generate_speaker_psp(question):
    presuppositions = []
    sentencelist = splitter.split(text=question)
    print(sentencelist)
    speakerpsp_sentencelist = []
    index = 0
    for sentence in sentencelist:
        if is_tag_question(sentence):
            speakerpsp_sentencelist.append(sentencelist[index-1])
        index += 1
    for sentence in speakerpsp_sentencelist:
        wordslist = [word for word in sentence.split(" ")]
        print(wordslist)
        if is_cc(wordslist[0]):
            wordslist = wordslist[1:]
        psp = "The speaker believes that "
        for word in wordslist:
                psp += convert_first_second_person(word) + " "
        presuppositions.append(psp)
    return presuppositions


