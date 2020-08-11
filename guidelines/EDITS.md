# Edits to the original AGLDT XML files

Here is a list of all the changes that must be made to the original XML texts

## All texts

* πρέσβυς agg. instead of noun
* Check sentence tokenization
* fix tokenization
  * congiunzioni: οὔτε, μήτε, μηδέ, οὐδέ, εἴτε
* POS of pronouns
* Predicative participles
* Arguments of nouns (e.g. λόγος + Acc/Inf)
* οὕνεκα conj and prep
* check μή: adv vs conj

## Specific author/texts

### Tragedy

* check CTS URNs of the choral odes

### Sophocles

* check the "collapsed" artificial:
  * go to the files of v1 (e.g. [here](https://raw.githubusercontent.com/PerseusDL/treebank_data/master/v1/greek/data/tlg0011.tlg005.perseus-grc2.xml))
  * look for cases where `_ExD` have the same index but different head
  * e.g. `cid=45106176` and `cid=45106163` are both `_ExD0_` but the first has
  `head=47`, the latter `head=34`.  

### Homer

* get rid of the AP_ExD0_APOS

| Author    | Title  | Sentences | Tokens (tot)     | Artificial  	|
|---	|---	|---	|---	|--:	|