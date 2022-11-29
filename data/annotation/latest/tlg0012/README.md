# The Homeric poems (TLG 0012)

## Source

The original data were taken from Perseus [Ancient Greek and Latin Dependency Treebank](https://perseusdl.github.io/treebank_data/), v.2.1.

The Homeric poems were originally annotated by:

* Jennifer Adams
* Jennifer Curtin
* James C. D'Amico
* W. B. Dolan
* Calliopi Dourou
* Scott J. Dube
* C. Dan Earley
* Mary Ebbott
* J. F. Gentile
* Francis Hartel
* Connor Hayden
* Tovah Keynton
* Michael Kinney
* Florin Leonte
* Alex Lessie
* Daniel Lim Libatique
* Brian Livingston
* Meg Luthin
* George Matthews
* Molly Miller
* Jack Mitchell
* Jessica Nord
* Anthony D. Yates
* Sam Zukoff

See the original XML files for more information on the annotators. If you spot any
error or missing information, please report everything in the [issue](https://github.com/francescomambrini/Daphne/issues) section.

## Conversion and revision

The AGLDT files were converted to UD using the [tb2ud](https://github.com/francescomambrini/tb2ud) set of scripts.

The UD files were reviewed by Francesco Mambrini with the help of Erica Biagetti
and Chiara Zanchi (Univesità di Pavia).

## Things to review

* double accusatives
* adnominal datives
* blank nodes and ellipses
* verbs governing two or more `obj` (with cases other than acc)
* ἅδην + gen (e.g. *Od* 5.290: ἀλλ' ἔτι μέν μίν φημι ἅδην ἐλάαν κακότητος.):
morphology and syntax
* postpositive (-)δε: tokenization, morphology, syntax
* ὡς: morphology and syntax
* similes
