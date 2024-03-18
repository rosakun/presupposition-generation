import spacy
import re
from ner_hilfsfunktionen import ner_psp_generator
import json
from np_hilfsfunktionen import np_psp_generator
from relcl_hilfsfunktionentest import relcl_psp_generator
from advclause_hilfsfunktionen import generate_adverbial_psp
from speaker_hilfsfunktionen import generate_speaker_psp

spacy_model = spacy.load("en_core_web_sm")


# NAMED ENTITY RECOGNITION for extracting
# TODO: Combine chunker and NER components for better definite article recognition

# Removes whitespaces, newlines, quotation marks and Q: from .csv questions file
# Outputs a .json file with sentences and presupposition
def clean_csv(csvfile,jsonfile):
    tojson = []
    with open(csvfile,encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip(): # Skips lines that are only whitespace
                line = line.strip("\"")
                line = re.sub("\"$","",line)
                line = line.strip()
                jdict = {"question": line}
                tojson.append(jdict)
    with open(jsonfile, "w", encoding="utf-8") as w:
        json.dump(tojson,w,indent=4)

# Takes a sentence as input and returns a list of all NER-based PSPs.




def pos_generator(doc):
    pos = []
    for word in doc:
        pos.append(str(word.text) + ": " + str(word.pos_))
    return pos

def tag_counter(incsv):
    count = {}
    with open(incsv) as f:
        for line in f.readlines():
            line = line.split(',')
            tag = line[-2]
            if tag not in count.keys():
                count[tag] = 1
            else:
                count[tag] += 1
    sorted_count = sorted(count.items(), key=lambda x:x[1])
    print(sorted_count)

def presupposition_counter(injson):
    psp_count = 0
    with open(injson) as f:
        questions = json.load(f)
        for question in questions:
            for item in question["presuppositions"]:
                psp_count += 1
    return psp_count


def psp_generator(injson,outjson,generate_pos=False):
    with open(injson,encoding="utf-8") as r:
        questions = json.load(r)
        for question in questions:
            doc = spacy_model(question["question"])
            question["presuppositions"] = np_psp_generator(doc)
            question["presuppositions"] += relcl_psp_generator(doc)
            question["presuppositions"] += generate_adverbial_psp(doc)
            if generate_pos:
                question["pos"] = pos_generator(doc)
    with open(outjson,"w",encoding="utf-8") as w:
        json.dump(questions,w,indent=4)


psp_generator("randykinnard.json","randykinnard_psp.json")
#print(presupposition_counter("randykinnard_psp.json"))
#clean_csv("np.csv","np.json")
#tag_counter("Tagged_psp.csv")