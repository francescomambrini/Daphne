# Guidelines
This document details the guidelines for morphosyntactic annotation that were followed
for this fork of the [Ancient Greek Dependency Treebank]().

In general, the same annotation rules and principles as the AGDT (v 1.7) will be followed.
We discuss here only the case where some additional details add to be specified,
or where some corrections had to be made to the original annotation.

## Morphological analysis and Lemmatization

### Pronouns

In contrast to other POS (like adjectives or nouns), pronouns belong to a close class, but it is not always easy to to assign the different lemmata to this or that category. Bear in mind that POS does not register syntactic annotation, thus proper pronouns (like ὅδε) used adjectively are *not* annotated as adjectives.

Thus, the list of pronouns varies considerably, depending on whether one considers syntactic, semantic or morphological (i.e. based on flexion) aspects to make the distinction.

Our list and classification is based on that of Kuhner and Blass (pp. 579-ss), with some modifications (marked with *):

1. personal pronouns: ἐγώ, σύ, ἡμεῖς, ὑμεῖς, σφεῖς with various peculiar forms for the other persons and cases (ἕ, νῶϊ, οὗ etc.)

2. possessive pronouns: ἐμός, σός, ἡμέτερος, ὑμέτερος, (ἑ)ὅς, νωΐτερος, σφέτερος

3. reflexive pron.: ἐμαυτοῦ, σαυτοῦ, ἑαυτοῦ

4. reciprocal pron.: ἀλλήλων

5. demonstrative pronouns:
   * ὁ, ὅδε
   * αὐτός
   * οὗτος, ἐκεῖνος
   * ἄλλος
   * τόσος, τοσόσδε, τοσοῦτος
   * τοῖος, τοιόσδε, τοιοῦτος
   * τήλικος, τηλικόσδε, τηλικοῦτος

6. interrogative pronouns:
   * τίς
   * πότερος*
   * πόσος
   * ποῖος
   * πηλίκος

7. relative-interrogative pron:
   * ὅς
   * οἷος
   * ὁποῖος
   * ὅσος, ὁπόσος
   * ὁπότερος (vedi K-B par 157.8)
   * ἡλίκος
   * ὁπηλίκος

8. indefinite and interrogative pronouns:
   * τις
   * ὅστις
   * δεῖνα
   * ἑκάτερος, ἕκαστος (vedi K-B par 157.8)
   * πᾶς*
   * ποσός
   * ποιός
   * οὐδείς, μηδείς

Note that K-B correctly identifies a class of pronominal adverbs (together with pronominal adjectives and nouns); however they also rightly state that these pronouns behave more as adverbs and we will annotate them as such.

It is worth noticing that (with the exception of the definite article, which has a POS for itself, and the personal pronoun which is distinguished in UD) our list largerly covers most of the same word types that are annotated with the tag [`DET`](https://universaldependencies.org/u/pos/DET.html) in Universal Dependency.

~~Note also that other ambiguous words (like πᾶς) are not tagged as pronouns, but as adjectives.~~

### Compound conjunctions

By "compound conjunction" I mean those conjunctions that are formed by two particles (of which, one is usually the coordinating conjunction τε or δέ, the other often a negative particle) that perform two syntactically different functions. The most frequent are five: εἴτε, μηδέ, οὐδέ, οὔτε, μήτε.

These words pose a few problems for treebanking, in several areas of the annotation process:

* tokenization: tokenize the five words separating the two components: εἴ and τε, μη and δέ, οὐ and δέ, οὔ and τε, μή and τε. Separate the components as they are written, without adding diacritics like hyphens or accents/spirits;
* morphology: annotate the two components as if you were annotating the full word, e.g.:

```xml
<word id="1" form="μη" lemma="μηδέ" postag="c--------" .../>
<word id="2" form="δέ" lemma="μηδέ" postag="c--------" .../>
```

All the 5 words listed above are to be tagged as **conjunctions**, regardless of the annotation of the single components (e.g. δέ and οὐ are usually tagged as adverb).

For syntax, the two components must be annotated according to their function. See below for the special case of εἴτε.

### Numerals

Numerals are tagged as adjectives.

### Irregular comparatives and superlatives
Lemmatize irregular (i.e. polytematic) comparatives and superlatives under themselves; the proper
degree (comp. or sup.) must be marked in the appropriate position of the pos-tag.

Note that this goes only for *polytematic* comp/sup. Superlatives φίλτατος and ἔχθιστος are lemmatized under
φίλος and ἐχθρός.

### Special words

#### καί

#### μᾶλλον and μάλιστα
μᾶλλον and μάλιστα must be lemmatized under μᾶλλον and μάλιστα, and tagged as comparative
and superlative respectively.

#### μή
Like Latin *ne*, μή can be either a negative adverb or a subordinating conjunction (typically, when it is joined with a *verbum timendi*). It must be tagged either as a conjunction or adverb.

However, note that μηδέ and μήτε are always conjunctions.

#### ὡς

We adopt a classification based on syntactic behaviour:

* when it introduces a clause, ὡς is tagged as conjunction (note that LSJ classes some of the uses under A., ὡς as Adverb):
    - comparative clauses, even with elided verbs (κινήθη δ᾽ ἀγορὴ ὡς κύματα μακρὰ θαλάσσης) and when it is correlated with other adverbs, such as οὕτως and even with other conjunctions (ὡς ὅτε)
    - with substantive clauses (=ὅτι)
    - with consecutive clauses (=ὥστε)
    - with adverbial clauses (e.g. ὡς ἔοικε)
    - with clausal clauses
    - with final clauses
    - with temporal clauses
    - with elliptical sentences (LSJ F.)
  To these protytpical examples, we also add:
    - with participles, present and future, nominative and oblique cases (LSJ C.I)
* when it is used adverbially in a clause, it is tagged as adverb:
    - with numerals (to mark that they are taken as approximation)
    - with other adverbs (ὡς ἀληθῶς)
    - with superlatives (ὡς ῥᾷστα)
    - with prepositions
    - with adjectives ("such persons as"... Headlam, CR 17 (1903:243)); also
    with pronouns: ὡς ἐμοί = "for such a person as I am", or with nouns: ὡς τειρομένου του, 
    "as of suffering man" (S. Phil. 203).
    - in indipendent clauses, as an exclamation, with adj., nouns and verbs
    - in indipendent clauses, in wishes ("ὡς ἔρις . . ἀπόλοιτο", Il.18.107)
* when it is used as a preposition (LSJ C.III), it is tagged as `r` accordingly.

On the syntactic annotation, see the section on ὡς (syntax).

## Syntax

### PNOM (and OCOMP)

The label `PNOM` (and, to some extent, the corresponding `OCOMP` label)  has been somewhat
extended from the original design, which limited its application only to the predicate nominals
of standard grammar.

The following is a list of constructions that are tagged as `PNOM`:

* predicate nominals (with copular verbs or in nominal constructions);
* raised complements with the nominative participles, in constructions where,
if attested with the infinitive, the subject of the infinitive is controlled by the
subject of the main verb) see below on ''raised'' complements;
* datives in dative of possessions (**est mihi puella**...);
* other predicative constructions with εἰμί (or nominal): e.g. with genitive (Τροίαν Ἀχαιῶν [`PNOM`] οὖσαν)
* genitive of pertinence ('it is proper of, appropriate to'...); Aesch. Ag. 1665:
οὐκ ἂν Ἀργείων τόδ' εἴη ('this would not befit the Argives'; 'it would not be the Argive way', Sommerstein)

### Special cases

#### "Raised" objects

"Predicative" construction, where one of the arguments of the subordinate clause is "raised"
and become argument of the main verb, are rather frequent in Greek.

One type of "raised" predicatives is represented by so called "predicative participles"
in accusative (or genitive/dative, depending on the case governed by the head verb). See
Soph. *Aj* 3-6:

```
 καὶ νῦν ἐπὶ σκηναῖς σε ναυτικαῖς ὁρῶ Αἴαντος [...] πάλαι κυνηγετοῦντα καὶ μετρούμενον ἴχνη

```

(Note that English has a similar "raised" construction with the verb "to see": "I see you chasing and measuring the tracks")

In this construction, the bivalent verb ὁράω receives a supplementary argument in the form of a participle, specifying
the actions that the verb's objects is seen doing. Note that, with many verbs that are contructed with predicative participles
of the object, the accusative/infintive construction is often also attested (for ὁράω, see [LSJ](http://www.perseus.tufts.edu/hopper/morph?l=oraw&la=greek#lexicon), II.d ).

A similar case, though less frequently attested and more irregular, is met when the subject of
a subordinate clause is "raised" and becomes the objects of the verb that governs the subordinate.
Sophocles in particular is rather fond of this construction. See for instance Soph. *Aj* 334-5:

 ```
 ἢ οὐκ ἠκούσατε Αἴαντος οἵαν τήνδε θωΰσσει βοήν;

 ```

Note here that Αἴαντος is not only raised from the position of subject of the interrogative clause, so as to fill
an additional role of the verb ἀκούω. It also acquires the genitive case, which is the proper case required by the verb.

Another example is Soph. *El.* 332-3:

```
καίτοι τοσοῦτόν γ᾽ οἶδα κἀμαυτήν, ὅτι ἀλγῶ 'πὶ τοῖς παροῦσιν
```

Where Jebb rightly notes: "κἀμαυτήν, ὅτι, instead of “ὅτι κἀγὼ”."

Again, Soph. *Tr. 320-1* is similar:

```
ἐπεὶ / καὶ ξυμφορά τοι μὴ εἰδέναι σέ γ᾽ ἥτις εἶ.
```
(σέ is the subject of the interrogative clause ἥτις εἶ raised to become the object of εἰδέναι)

Or Aesch. Ag. 1199-1200:

```
θαυμάζω δέ σου, πόντου πέραν τραφεῖσαν ἀλλόθρουν πόλιν κυρεῖν λέγουσαν
```

Commentaries and grammars often refers to these arguments objects in "apposition" or "justapposed". However,
the construction is a case of argument "raising" (while the annotation as apposition - with `OBJ_AP` would be wrong
as the two arguemnts do not have the same semantic reference).

Tim Osborne and Matthew Reeve (see [here](http://www.aclweb.org/anthology/W17-6521)) have reviewed the different options to formalize these constructions in a Dependency Grammar.
Here, we follow their suggestion: we attach both the "raised" and the proper argument to the governing verb. Osborne and Reeve do not discuss the
question of how to lable the arguments. A construction with two `OBJ`s would not work, as the two complements cannot be considered two independent and external arguments of the verb.

We decided to extend the use of the label `OCOMP` to tag also this peculiar type of verb complement.

**To sum up**: consturctions with verbs and raised arguments - where a supplementary argument of a governing verb is raised from an embedded predication -
are annotated as follows: both the raised and "proper" argument (generally represented by the verb of a subordinate clause or participle) are attached to the verb;
The "raised" argument is annotated as `OBJ`, while the other (which ends up occupying the position of a predicative object complement) is annotated as `OCOMP`.

#### Predicative participles in nominative (as in "λάθε βιώσας")

This is a famous peculiar construction of Greek. First-year students learn that, with some verbs (as φαίνω, λανθάνω, τυγχάνω etc.),
the main semantic weight of the action, event or state of affair is put on the joining participle, while the main verb
only adds a sort of a modality trait (pubblicity or hiddenness of the action, accidentality etc.). In a traslation,
the participle typically becomes the main verb, while the Greek main verb is rendered with an adverb (e.g. φαίνω: 'visibly', 'manifestly').

Although the semantic weight is peculiarly distributed between main verb and participle, from the standpoint of syntax there is no reason not to annotate similar sentences with
the usual syntactic structure reserved to verb + nominative participles. In other word, the verbs φαίνω, λανθάνω, τυγχάνω etc. is annotated according to its syntactic function (e.g. `PRED`, `OBJ`, `ATR` etc), while the participle is regularly tagged as `ADV`.

Note that with the verb κυρέω, the participle can be tagged as either:
* `ADV`, when the verb means 'it the mark in doing' (LSJ II.2)
* or `PNOM` when the verb means 'turn out', 'be' and is equivalent to an auxiliary (σεσωσμένος κυρεῖ, Aesch. Pe. 503).

#### Predicative participles in accusative (or indirect cases)
The participle is tagged as `OCOMP`: see above under `"Raised" objects`.


#### Arguments with nouns

Some nouns (especially those meaning "report", "story", but also words for sentiments, such as θάρσος, αἰδώς ecc)
govern infinitives or clauses that describe their content. See e.g. Soph. Tr. 1-2:

```
λόγος μέν ἐστ᾽ [...] / ὡς οὐκ ἂν αἰῶν᾽ ἐκμάθοις βροτῶν
```
("there is a saying [...] that...")

Those clauses must be annotated as `ATR`, as their function is to restrict the reference
of the governing noun (not just a saying whatsoever, but that saying that tells...) or
specify its features.

This also goes for the very rare case where the "content" of a noun is provided by another noun in accusative:

```
θεοὶ [...] ἀνδροθνῆτας Ἰλίου φθορὰς
ἐς αἱματηρὸν τεῦχος οὐ διχορρόπως
ψήφους ἔθεντο

(Aesch. Ag. 813-6)
```

According to Hermann (1852: 434) Ἰλίου φθορὰς ψήφους ἔθεντο = ἐψηφίσαντο Ἰλίου φθοράς.
Note, however, that some editors (Sommerstein, West and, dubitatively, Denniston-Page) follow Dobree
in reading φθορᾶς (gen. sg.) instead of φθορὰς (acc. pl.). See West (1990: 204).

Whatever reading, the syntactic function of the epexegetical/objective genitive and the accusative is the same.

#### Proleptic pronouns, followed by clause

Sentences like: "this I tell you, that [...]". Although some annotation here and there might still use `APOS` formalism, the construction should rather be annotated as:
* `OBJ` (or whatever tag is requested by the valency of the verb) for the proleptic pronoun;
* `ATR` for the clause, that must be attached to the proleptic pronoun.

E.g. Soph, *El.* 988-9:

```
τοῦτο γιγνώσκουσ᾽ ὅτι ζῆν αἰσχρὸν αἰσχρῶς τοῖς καλῶς πεφυκόσιν

```
(knowing *this*, that living a shameful life is shameful for those nobly born)

Note that we adopt annotation style even in the rare cases when the clause is not an acc+inf, but an independent clause, as in Aesch. Ag. 1332-4:

```
 δακτυλοδείκτων δ' οὔτις ἀπειπὼν εἴργει μελάθρων, μηκέτ' ἐσέλθῃς, τάδε φωνῶν .
```
("and no one bans it and keeps it away from houses at which fingers are pointed, saying this: “Don’t come in here any more!”"; trans. adapted from Sommerstein)

```
φωνῶν-[OBJ]->τάδε-[ATR]->ἐσέλθῃς
```

#### Noun or AuxP?

Certain nouns (typically in acc.) are used adverbially with a genitive; they appear to be on their way to lose they're full meaning and evolve to preposition. See for instance δίκην = "in the way of, after the manner of" (LSJ A.2).

Anyway, since they have *not* undergone a full desemanticization, they still must be annotated as `ADV`, while the governed genitive is `ATR`.
E.g. Aesch. Ag. 3 κυνὸς δίκην.

### Multi-word conjunctions

Expressions that means "except when", "as when" are tagged as multi-word conjunction groups.
This means that:
* the first conjuction is the head of the group
* the "when" part is `AuxY`

#### ἔχω + adverb

When adverbs are joined with the verb ἔχειν (with the meaning: "being in a certain condition", cf. Italian "stare (bene o male)"), they must be annotated as `ADV`, not `OBJ`.

#### Genitives with exclamation

It's a genitive of cause ("alas for..."), thus `ADV` attached to the exclamation. See e.g. *Aj* 366: ὤμοι γέλωτος (`ExD --> ADV`).

#### γάρ

γάρ is not a conjuction, and therefore it must **not** be annotated as `AuxC`. The particle is the typical sentence adverbial, and therefore is always annotated as `AuxY`. The fact thatin English it is often translated with the conjunction "for" is utterly irrelevant.

Occasionally, γάρ occurs in the middle of a sentence within a parenthetical expression. In that case, use the appropriate rules for annotation of parenthetical expressions (see below).

#### ὡς (syntax)

Syntactically, ὡς is annotated as:
- `AuxY` when it used to "color" some other (especially function) words, such as prepositions or conjunctions
- the same "coloring" function is also found with participles and numerals
- `AuxY` is also used when it is joined with adjectives or nouns used as `ATV/AtvV` (meaning 'as (something)')
- `AuxC` when it is tagged conjunction and it introduces one of the clauses listed above
- `ADV` when it is used in independent clauses in exclamations or wishes or with adjectives and nouns .

Note that the word governed by ὡς is generally tagged as `ADV`. This also goes for adjective/nouns,
even if in nominative. See for instance Ag. 1464-6:

```
μηδ᾿ εἰς Ἑλένην κότον ἐκτρέψῃς / ὡς ἀνδρολέτειρ᾿, ὡς μία πολλῶν ἀνδρῶν ψυχὰς Δαναῶν ὀλέσασ᾿ ἀξύστατον ἄλγος ἔπραξεν
```

Which Sommerstein aptly translates: "nor turn your anger against Helen, **calling her**
a destroyer of men, **saying that she** alone brought death to so many souls of Danaan men and caused pain too strong to stand"

Here, according to our guidelines the two ὡς have two different PoS: the first is adverb, the second conjuncion.
Likewise, the syntactic annotation is different: it's `AuxY` with the adj. ἀνδρολέτειρα,
and an ordinary `AuxC` governing ἔπραξεν.

However, the two clauses appear to be coordinated in asyndeton, with the repetition of ὡς.
The adj. ἀνδρολέτειρα is in nominative, so the word does not agree with Ἑλένην and
therefore cannot be made an `ATV` of it. However it would be clumsy to annotate
it as a nominal clause governed by an ὡς-AuxC and ἀνδρολέτειρα as `PNOM`.
The most natural solution, I believe, is to take this construction as an `ADV`,
pretty much as we annotate participles in nominative.


#### οἷος + noun or participle

When οἷος is used like ὡς, to introduce a comparison, in the sense of "as", "such as" and is coupled with noun or participle, it should be tagged `AuxY` and depend on noun/participle.


The governing nouns are then tagged as `ATV`/`AtvV`, while the participles are generally `ADV`.

#### εἴτε

εἴτε must be tokenized in its two components: εἴ + τε (see above Compound conjunctions for morphology). Sometimes εἰ performs the actual function of a conjunction, introducing two coordinated hypothetical subordinates. Other times, however, εἴτε is just equivalent to English "either", introducing a coordinated phrase that doesn't require a verb and has no hypothetical meaning.

In the former case, treat εἴ as a an `AuxC` governing the verb of the subordinate (either a word or an artificial node); in the latter, attach it to the head of the coordinate phrase as an `AuxY`. Treat the τε according to its function in the coordination as usual (`COORD` for terminal coordinating node; `AuxY` for every non-terminal coordinator).

#### Parenthetical expressions

We distinguish between one-word parenthetical expressions like οἶδα ("- I know -") and more complex parenthical sentences, where there is a verb govering a whole group of words or expressions.

The formers, can be adjectives used in "apposition to the whole sentence" (this is how they are typically referred to in commentaries, and they are not uncommon in tragedy); they are annotated as `ATR` and depend from the root of the sentence (or the clause they qualify). Most frequently, one-word parenthetical expressions are first-person verbs like οἶδα that are used to characterize the enunciative stand of the speaker. As such, they are a typical instances of `AuxY`.

More complex parenthetical are generally printed within parentheses and govern more complex syntactical constructions. In this case, the head of the sentence (typically, the verb) depends on the word the parenthesis is attached to. This can be the whole root of the sentence, if the parenthetical sentence adds information or comments on the whole sentence; or to the specific word of the sentence the parenthesis makes reference to. The head of the parenthetical sentence is tagged as `PRED` with the special `_PA` appendix derived from the [PDT guidelines](https://ufal.mff.cuni.cz/pdt2.0/doc/manuals/en/a-layer/html/ch03s05.html).

Note that nominal clauses used parenthetically such as νόμος γάρ or θέμις γάρ ("as it is the law / customary"), which are frequent in Homer, are in fact cases of more syntactically complex parenthesis, to be annotated with the `PRED_PA`. As the clauses are nominal, they should be annotated accordingly: the `PRED_PA` element is a reconstructed node.

#### "Resumed" objects

Sometimes, especially in colloquial style or impassioned speech, accusatives at the beginning of a sentence are "taken over", "picked up" or resumed by a new object towards the end of the utterance, or closer to the verb. Although this construction is very similar to an anacoluthon, the first direct object is not really left suspended or dangling without a construction, but is rather taken over by a different, yet conceptually related word.

E.g.:

* Soph. *Aj* 1062-3: ὧν εἵνεκ᾽ **αὐτὸν** οὔτις ἔστ᾽ ἀνὴρ σθένων / τοσοῦτον ὥστε **σῶμα** τυμβεῦσαι τάφῳ (lit.: "for these resons, *him*, there is no man strong enough to bury his corpse").
* Soph. *Aj* 1147-9: οὕτω δὲ **καὶ σὲ καὶ τὸ σὸν λάβρον στόμα** / σμικροῦ νέφους τάχ᾽ ἄν τις ἐκπνεύσας μέγας / χειμὼν κατασβέσειε **τὴν πολλὴν βοήν**. (lit: "and so you and your boisterous mouth a big storm rising from a small cloud shall perhaps quench your loud claim", with "loud claim" picking up "you and your boisterous mouth").
* Soph. *OT* 819-820: καὶ **τάδ᾽** οὔτις ἄλλος ἦν / ἢ 'γὼ 'π᾽ ἐμαυτῷ **τάσδ᾽ ἀρὰς** ὁ προστιθείς

(note that the first 2 sentences are both uttered by Menelaos in a very intense exchange over Teucer's right to bury Ajax)

**Temporary solution**: the first object is tagged as `AuxY`; note that in the second sentence, as the slot of the first (dangling) object is filled by a coordinating clause, we use the very rare tag `AuxY_CO`.
