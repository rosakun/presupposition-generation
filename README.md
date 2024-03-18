# presupposition-generation

## from_crossexamination

This folder includes code that uses SpaCy to extract elementary presuppositions from cross-examinations. 
The file 'main.py' includes the main code that executes this. You can specify an input json file that contains questions, and the name for an output file that contains questions and their presuppositions.
It also includes a code that converts .csv files to .json files that can then be used as input for 'main.py'.
We include three files as examples: 'randykinnard.csv' is an example of the acceptable format for csv files that can be converted to .json.
'randykinnard.json' is an example of the acceptable format for input json files to 'main.py'.
'presupposition_randykinnard' is what the output of 'main.py' should look like.

## presupposition_augmentation

This folder includes code that re-embeds the presuppositions of premise-presupposition pairs under negation, interrogation, modals and conditionals.
To run it, you need a dataset in the same format as you can see in 'example_input_file.json'.
Simply run the function 'main(presupposition_file,output_file)' in the main.py file with your dataset and the name you want your output file to have.
It should end up looking like 'example_output_file.json'.
