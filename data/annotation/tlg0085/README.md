# Daphne: Annotation in progress

Treebank files of Aeschylus that are currently being checked. Below you'll find a list
of all the features that I am currently checking.

The file `aeschylos_pedalion_changes.tsv` list all the changes that were made by the
people working on the Pedalion project, with a comparison to the AGLDT files. The list
was graciously provided by Toon van Hal and Alek Keersmaekers!

## lemmatization and pos to change

* πρέσβυς = adj instead of noun
* POS tagging of pronouns
* pos tagging of ὁ (always l)
* φρήν: check gender
* ἄλλος pronoun
* οὐδείς pronoun?

## Costructions to check

* tokenization
    * crasis
    * 5 compound conjunctions
* delete unused artificials
* Predicative participles: parts tagged as ATV/AtvV
* Raised objects: OBJ_AP with nouns/pronouns and verbs
* Objects dependent on nouns/adjs
* Constructions with εἶναι
* Dative of possession
* lemmatization of ἄντιος
* adverbs annotated as OBJ --> ADV
* pos of δέ
* pos of ὡς
* lemma of κἄν


## Versions:
The following files have been uploaded to Arethusa. This means that the ** version
in Arethusa is always the most updated** until the files are moved out of the `in_progress`
folder.

* tlg0085.005
