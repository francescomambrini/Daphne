# The Daphne Treebank repository of Ancient Greek Poetry.

**IMPORTANT!**

With v.0.5, Daphne now has switched to the [UD](https://universaldependencies.org/)
annotation schema. If you want the old AGLDT-compliant XML files you can either:
  - check out the version tagged `v0.4.1-agldt`
  - retrieve them from the file `other/old_agldt_source.zip`

## What is it?

A collection of treebanks of poetic Ancient Greek texts, starting with drama and
archaic epos. For Aeschylus, Sophocles, Homer and Hesiod, the source
of the annotation is Perseus' [Ancient Greek and Latin Dependency Treebank](https://perseusdl.github.io/treebank_data/).
Euripides' *Medea* comes from [Pedalion](https://github.com/perseids-publications/pedalion-trees).

The treebanks were converted from the original AGLDT-like formalism to
[Universal Dependencies](https://universaldependencies.org/) (UD) with the help
of my rule-based converted [tb2ud](https://github.com/francescomambrini/tb2ud).
The UD conversion is constantly revised and reviewed by hand.

## What kind of modification were introduced?

At first, I started Daphne because I wanted to bring the annotation in line with a
more specific set of guidelines, for both morphology and syntax. The original guidelines
for Daphne were based on version 1.7 of the AGDT guidelines for Greek,
with some qualification and special trait.

In a second phase of the work, I decided to move all the annotation to the Universal
Dependencies formalism. One of the reason why I decided to move to UD is because
I'd like to add other layers of annotation, like speaker tags for direct speech,
animacy for words, links to dictionary forms, etc. UD is a very active community
where support is constantly introduced for new tools and new expansions.

## Why did we need another treebank for Greek?

The AGLDT is simply awesome (and I know: I did a bit of it)!

But what we need is: a) a tighter set of annotation guidelines to make the annotations
more consistent; b) texts with those corrections implemented here and there where they need it;
c) more annotation (both as in "more annotated texts" and "more types of annotation on what we already have treebanked") d) better NLP and reliable automatic annotation e) more
integration with other projects, both for Greek and other languages.

AGDT 2.x goes in the direction of more defined guidelines. But I'd still like to have control on the type of annotation I perform. Secondly, UD provides the perfect answer to all
the latter requirements.

## Why just poetry?

Well, that's what I like to work with...

## Are there commentaries attached to the treebanks?

As I tried to argue [elsewhere](https://www.ubiquitypress.com/site/chapters/10.5334/bat.f/),
you can't do treebank annotation without doing a full, thorough textual analysis of
what you're annotating.

So, you might as well keep track on what you do, especially the alternative interpretations that
are possible and the nuance of meanings that different treebank configuration might introduce.
I did just that when I annotated some of the tragedies of Sophocles.

**Caution**: at the moment, those files are just notes. Some of them even mix Italian (my own
native tongue) and English. I'll polish them in due time.
