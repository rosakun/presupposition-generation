import spacy
from np_hilfsfunktionen import starts_with_vowel
from np_hilfsfunktionen import regular_plural
from relcl_hilfsfunktionentest import generate_np
from relcl_hilfsfunktionentest import generate_subject
from relcl_hilfsfunktionentest import generate_prt
from relcl_hilfsfunktionentest import generate_advmod
from relcl_hilfsfunktionentest import generate_xcomp
from relcl_hilfsfunktionentest import generate_pp
import re
spacy_model = spacy.load("en_core_web_sm")

"""
Adverbs:
when, before, after
"""

def generate_vp_advcl(token):
    deps = [child.dep_ for child in token.children]
    index = 0
    vp = ""
    aux = ""
    neg = ""
    auxpass = ""
    xcomp = ""
    acomp = ""
    mainverb = ""
    onceflag = True
    negflag = 'neg' in deps
    passive = 'auxpass' in deps
    if token.morph.get("Tense") == 'Pres' or token.morph.get("VerbForm") == 'Inf':
        onceflag = False
    for child in token.children:
        print(child.text,child.dep_)
        if str(child.dep_) == 'neg':
            neg += child.text
        if str(child.dep_) == 'aux':
            if negflag: 
                aux += child.text
            else:
                aux += child.text + ' once '
            onceflag = False
        if str(child.dep_) == 'auxpass':
            if negflag:
                if child.text == 'is':
                    auxpass += 'was' + " "
                    onceflag = False
                else:
                    auxpass += child.text + ' '
                    onceflag = False
            else:
                if child.text == 'is':
                    auxpass += 'was once '
                    onceflag = False
                else:
                    auxpass += child.text + ' once '
                    onceflag = False
        if str(child.dep_) == 'xcomp':
            xcomp += generate_xcomp(child)
            if onceflag:
                xcomp += ' once '
                onceflag = False
        if str(child.dep_) == 'acomp':
            acomp += child.text
        index += 1
    if onceflag:
        mainverb += " once "
    mainverb += token.text
    if passive:
        vp += aux + auxpass + neg +  " " + mainverb + " " + xcomp + " " + acomp
    else:
        vp += aux + neg + " " + auxpass + " " + mainverb + " " + xcomp + " " + acomp
    return vp

def generate_adverbial_psp(doc):
    presuppositions = []
    for token in doc:
        vp = ""
        subj = ""
        dobj = ""
        prt = ""
        advmod = ""
        pp = ""
        if str(token.dep_) in ['advmod','mark'] and token.text in ['when','When','before','Before']:
            vp += generate_vp_advcl(token.head) + " "
            #print(token.head)
            for child in token.head.children:
                #print(child.text, child.dep_)
                if str(child.dep_) == 'nsubj' or str(child.dep_) == 'nsubjpass':
                    subj += generate_np(child) + " "
                if str(child.dep_) == 'dobj':
                    dobj += generate_np(child)
                if str(child.dep_) == 'prt':
                    prt += generate_prt(child) + " "
                if str(child.dep_) == 'advmod' and child.text not in ['when','When','before','Before']:
                    advmod += generate_advmod(child) + " "
                if str(child.dep_) == 'prep':
                    pp += generate_pp(child) + " "
            psp = subj + vp + prt + dobj + advmod + pp
            psp = re.sub(' +', ' ',psp)
            psp = psp.strip()
            psp = psp[0].capitalize() + psp[1:]
            presuppositions.append(psp)
    return presuppositions

