# presupposition-generation

## generate_presuppositions_using_SpaCy

This folder includes code that uses SpaCy to extract elementary presuppositions from cross-examinations. 
The file 'main.py' includes the main code that executes this. You can specify an input json file that contains questions, and the name for an output file that contains questions and their presuppositions.
It also includes a code that converts .csv files to .json files that can then be used as input for 'main.py'.
We include three files as examples: 'randykinnard.csv' is an example of the acceptable format for csv files that can be converted to .json.
'randykinnard.json' is an example of the acceptable format for input json files to 'main.py'.
'presupposition_randykinnard' is what the output of 'main.py' should look like.

## generate_presuppositions_using_GPT

This folder includes code that generates presuppositions from cross-examination questions using GPT (da-vinci-003).
First, it includes a code that pre-processes .tsv files containing cross-examinations in the format given by the website https://www.patrickmalonelaw.com/useful-information/legal-resources/attorneys/legal-resources-attorneys-injured-clients/cross-examination-transcripts/ . An example of such a file is given by 'cross_examinations.tsv'. An example preprocessed file is 'cross_examinations_preprocessed.tsv'.
It also includes a code that takes the preprocessed cross-examination file as input, and uses GPT to generate presuppositions triggered by each question. It outputs
premise-hypothesis pairs in a .json file, an example is 'output.json'.
As a default, the premise-hypothesis pairs are labeled as 'entailment', or 'E'. This is because GPT generally outputs entailments instead of presuppositions. The pairs that are actually presuppositions must be manually checked and changed. In addition, the fields 'type' and 'trigger_type' are given default values 'na', that must also be changed manually in case of real presupposition items.

## presupposition_augmentation

This folder includes code that re-embeds the presuppositions of premise-presupposition pairs under negation, interrogation, modals and conditionals.
To run it, you need a dataset in the same format as you can see in 'example_input_file.json'.
Simply run the function 'main(presupposition_file,output_file)' in the main.py file with your dataset and the name you want your output file to have.
It should end up looking like 'example_output_file.json'.
