# Rulings on constructions

I try to keep alphabetical order

## Addressees and clauses

### Description

>τοὔνεκά *οἱ *προθέουσιν ὀνείδεα *μυθήσασθαι (Il. 1.291)

Addressee can be in dat or acc.

### Ruling

As the dat addressee would be an `iobj` under normal circumstances, I rule it as
`obj` here; the addressee almost always controls the subject of the clause, thus
the head of the clause is an `xcomp`.

In the rare cases when it is not controlled, then `ccomp`.

If a dative is not an addressee (e.g. with verbs meaning "to appear", "look like"),
then `obl:arg`.

## Free Relatives

In en, free relatives are relative phrases modifying a wh- pronoun, like 'how,
where, what, when'. Often (but not always), but by no means always, these pronouns
are in the *-ever* form.

In the [English guidelines](https://universaldependencies.org/en/dep/acl-relcl.html#free-relatives)
the annotation of free relatives is done withe the wh-pronoun as argument of the
main clause, while the head of the clause is a either `acl:relcl` (for pronominal heads),
or `adv:relcl` for 'where, when, how(ever)'.

~~~ sdparse
I 'll have whatever she 's having .
obj(have, whatever)
acl:relcl(having, whatever)

You can go where you want and eat what you want .
advmod(go, where)
advcl:relcl(where, want-6)
obj(eat, what)
acl:relcl(what, want-11)
~~~

### Description

In Greek (and Latin), the antecedent of a relative can be omitted, a special double
pronoun like ὅστις exists, and relativizers like ἵνα, ὅπου or adverbial ὡς work
like their English counterparts.

Here's a particularly nasty example with ὅστις
>ἄλγεα [...] ὅσσα διδοῦσιν ὅτίς σφ' ἀλίτηται ὀμόσσας (Il 19.265)
>griefs [...] which they give to anybody that...

If we take the "PDT" approach (which I prefer), that is, we take the head of the
relative clause as argument of the main verb, what are we to do of this indirect
object?

### Ruling

Since this relative clause is both a core argument and a clause, only `ccomp` is
right. However, this is a very peculiar type of `ccomp`: I'm calling it `ccomp:relcl`.

## Proleptic demonstratives

### Description

>τόδε ἴσθι, ὅτι...

There are a few different constructions that could be distinguished. In some cases,
the clause does not look like a subordinate (no conjunction, no infinitive), and
it could be taken as a normal case of `parataxis`. Compare En.:

>This I will say to you, none of you shall return

It will be normal to have:
```
parataxis(have, return)
```

But in most cases, the clause is a clear subordinate, either with acc/inf or by
some complementizer (particles for indirect questions, conjunctions). Int. ind.
clauses might be dubious, as they can also be taken as direct questions.

### Ruling

At present, I have nothing better to offer than `parataxis` with the pronoun
governing the clause. That's just a stub, but it should be easy to retrieve.

### How to retrieve

Look for `parataxis` of verbs governed by what is in most cases a `PRON`, but
`DET` or even `ADJ` could be possible.
