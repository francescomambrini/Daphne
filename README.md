# The Daphne Treebank repository of Ancient Greek Poetry.

## What is it?

A collection of treebanks of poetic Ancient Greek texts, starting with drama and 
archaic epos. For Aeschylus, Sophocles and (coming soon) Homer and Hesiod, the treebanks 
are taken from Perseus' [Ancient Greek and Latin Dependency Treebank](https://perseusdl.github.io/treebank_data/), 
but with some modifications in the annotation introduced by me.

## What kind of modification were introduced?

I would like to bring the annotation in line with a more specific set of guidelines, 
for both morphology and syntax. The guidelines for Daphne are based on version 1.7 of the AGDT guidelines for Greek, 
with some qualification and special trait.

## That's it? Is there something more?

Yes, I'd like to add other layers of annotation, like speaker tags for direct speech, 
animacy for words, links to dictionary forms, etc. The way I'd like to do that, though, is 
by using Linked Open Data principles. But that will take a while, I am afraid...

## Why did we need another treebank for Greek?

The AGLDT is simply awesome (and I know: I did a bit of it)!

But what we need is: a) a tighter set of annotation guidelines to make the annotations 
more consistent; b) texts with those corrections implemented here and there where they need it; 
c) more annotation (both as in "more annotated texts" and "more types of annotation on what we already have treebanked")!

AGDT 2.x goes in the direction of more defined guidelines. But I'd still like to have control on the type of 
annotation I perform

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


## I notice treebank files are distributed in two formats, XML and CoNLL-U. Why?

I use Perseids [Arethusa](https://www.perseids.org/tools/arethusa/app/#/) to tinkle 
with the original AGDLT XML files. But we still don't have a nice, easy search interface 
to query the Greek treebanks.

Now, it's very trivial to switch back and forth between ConLL-like formalisms and AGLDT XML. 
And [CoNLL-U](https://universaldependencies.org/format.html), the format of Universal Dependencies, 
has a lot of support and tools. See [here](https://universaldependencies.org/tools.html).

So I will keep the two versions in sync.
