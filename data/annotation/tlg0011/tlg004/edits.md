# List of Edits to the treebank

On Jul 14 2019, I have uploaded a new XML version on Arethusa, with improved
tokenization (krasis of καί and the 5 complex conjunctions).

Made some changes to the text:
- 190-191: text of the MSS (which was in any cases already the one annotated) restored:

```
Ἄρεά τε τὸν μαλερόν, ὃς / νῦν ἄχαλκος ἀσπίδων / φλέγει με περιβόητος ἀντιάζων, / παλίσσυτον δράμημα νωτίσαι πάτρας...
```
- 201: comma changed to period

Progress:

* prune useless Artificial Nodes

* check cases of:
   * ~~εἴτε, which seem undivided~~
   * μηδέ: conj
   * οὐδέ: conj
   * οὔτε: conj
   * μήτε: conj

* checking doubtful construction:
    * proleptic pronouns
    * advs with ἔχειν

* ~~checking doubtful POS tags:
    * σός > Pron (not adj)
    * τε : conj
    * μηδέ: conj
    * οὐδέ: conj
    * οὔτε: conj
    * μήτε: conj
    * εἴτε: conj
    * ἄν: AuxY > adv (lemma=ἄν1) ; AuxC > conj (lemma=ἐάν)~~

* checking the `UNDEFINED` relations

* checking the wrong `_ExD`
475 [('2', 'τάδ᾽'), ('8', 'γὼ'), ('13', 'ἀρὰς')]
520 [('1', 'ὡς'), ('9', 'κυβερνήτην')]
753 [('13', 'ἀφ᾽'), ('18', 'ξὺν'), ('25', 'οὕς'), ('27', 'μ᾽')]
790 [('39', 'οὓς'), ('45', 'οὓς')]
872 [('1', 'ὅμως'), ('2', 'δ᾽'), ('4', 'ἕσταμεν'), ('7', 'ἄμεινον'), ('8', 'ἐκμαθεῖν'), ('9', 'τι'), ('10', 'δραστέον')]
