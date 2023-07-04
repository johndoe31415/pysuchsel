# pysuchsel
pysuchsel is a program to create "Suchsel" word puzzles (i.e., a rectangular
array of letters which have words hidden within that you need to find, aka
"word search"). It can also create crossword puzzles. For both, from a given
word list, grid size and filling rules, it creates an SVG image that can easily
printed.

For Suchsels, it can fill all the void spaces with random letters that are
uniformly distributed or it can choose a random distribution that satisfies a
natural language (German and English are supported), making the Suchsel much
more difficult. It also supports hiding words left-to-right, right-to-left,
top-to-bottom, bottom-to-top, diagonally-to-top-right, diagonally-to-top-left,
diagonally-to-bottom-right, diagonally-to-bottom-left or any combination of
these placements.

For crossword puzzles, it takes care there is not adjacent cells filled, it
enumerates the words and creates number fields in the resulting SVG.

## Installation
pysuchsel requrires an SVG library written by myself,
[pysvgedit](https://github.com/johndoe31415/pysvgedit). It can, however, be
easily installed via PyPi:

```
$ pip install pysuchsel
```


## Suchsel mode
You'll first have to create a file that contains all the words (e.g., using
pluma or vim). We'll call it words.txt

```
$ cat words.txt
SUCHSEL
PADDELFISCH
```

Our file only contains two words. Then, you can already call pysuchsel to place
them into a Suchsel puzzle:

```
$ pysuchsel suchsel words.txt my_first_suchsel.svg
```

If you want to see where they were placed, specify "-v" as well:

```
$ pysuchsel suchsel -v words.txt my_first_suchsel.svg
+--------------------------------+
|                                |
|                                |
|                                |
|                                |
|       P A D D E L F I S C H    |
|                       U        |
|                       C        |
|                       H        |
|                       S        |
|                       E        |
|                       L        |
|                                |
|                                |
|                                |
|                                |
|                                |
|                                |
|                                |
|                                |
|                                |
+--------------------------------+
```

You can influence the size with the "-x" and "-y" options:

```
$ pysuchsel suchsel -x 11 -y 11 -v words.txt my_first_suchsel.svg
+------------------------+
| P                      |
| A                      |
| D                      |
| D                      |
| E                      |
| L                      |
| F                      |
| I       S U C H S E L  |
| S                      |
| C                      |
| H                      |
+------------------------+
```

You can also specify that you'd like words to share letters, which is then
going to be the preference:

```
$ pysuchsel suchsel -c -x 11 -y 11 -v words.txt my_first_suchsel.svg
+------------------------+
|                   P    |
|                   A    |
|                   D    |
|                   D    |
|         S U C H S E L  |
|                   L    |
|                   F    |
|                   I    |
|                   S    |
|                   C    |
|                   H    |
+------------------------+
```

When you specify "--verbose" twice, it'll also show how the padded Suchsel
looks like on the command line:

```
$ pysuchsel suchsel -c -x 11 -y 11 -vv words.txt my_first_suchsel.svg
+------------------------+
|                        |
|                        |
|                        |
|                        |
|         S              |
|         U              |
|         C              |
|         H              |
|         S              |
| P A D D E L F I S C H  |
|         L              |
+------------------------+
+------------------------+
| V C V P A B M O Z C K  |
| G I M S T X M U S P D  |
| T C P W H X W N E D L  |
| A S B L H T J U K V Q  |
| E L C M S U R T C W Z  |
| Z M J C U Y G K Y Q D  |
| J C Z E C B I X K J V  |
| U T Q E H K Y A F R P  |
| H R F A S K K N K V L  |
| P A D D E L F I S C H  |
| O N D N L E T A H T V  |
+------------------------+
```

To specify placement, use the "-p" command line option. For example, to only
create diagonal placement to the bottom right, do:

```
$ pysuchsel suchsel -x 11 -y 11 -p dbr -v words.txt my_first_suchsel.svg
+------------------------+
| P     S                |
|   A     U              |
|     D     C            |
|       D     H          |
|         E     S        |
|           L     E      |
|             F     L    |
|               I        |
|                 S      |
|                   C    |
|                     H  |
+------------------------+
```

To allow more than one placement method, specify them all. For example, only
allow top-to-bottom and bottom-to-top:

```
$ pysuchsel suchsel -x 11 -y 11 -p tb -p bt -v words.txt my_first_suchsel.svg
+------------------------+
|         S       H      |
|         U       C      |
|         C       S      |
|         H       I      |
|         S       F      |
|         E       L      |
|         L       E      |
|                 D      |
|                 D      |
|                 A      |
|                 P      |
+------------------------+
```

To influence the padding of letters, look at the "--fill-rule" option. By
default, padded letters are placed in natural language distribution of English
(i.e., each letter has the same probability of occurrence and only A-Z are
placed). That makes uncommon letters (e.g., Q and Y in the German language)
rather frequent not stand out. For example:

```
$ pysuchsel suchsel -x 5 -y 11 -vv words.txt my_first_suchsel.svg
+------------+
| P          |
| A          |
| D          |
| D S        |
| E U        |
| L C        |
| F H        |
| I S        |
| S E        |
| C L        |
| H          |
+------------+
+------------+
| P A L S I  |
| A L U T T  |
| D R W N H  |
| D S E N R  |
| E U T N T  |
| L C S I W  |
| F H D E D  |
| I S N S E  |
| S E E A R  |
| C L S A W  |
| H E T E A  |
+------------+
```

You can now first switch to German language, which will include more letters
and choose the German language distribution:

```
$ pysuchsel suchsel -f de -x 5 -y 11 -vv words.txt my_first_suchsel.svg
+------------+
|       P    |
|       A    |
|   S   D    |
|   U   D    |
|   C   E    |
|   H   L    |
|   S   F    |
|   E   I    |
|   L   S    |
|       C    |
|       H    |
+------------+
+------------+
| L D B P S  |
| S E N A F  |
| I S D D E  |
| E U B D P  |
| Ä C D E R  |
| I H N L I  |
| A S V F S  |
| T E N I B  |
| L L P S G  |
| L S N C R  |
| U N T H G  |
+------------+
```

You'll see that German letters are placed as fillers (e..g, note the "Ä"), but
it only occurs once (because its character frequency in German language is
comparatively low). Now compare that to:

```
$ pysuchsel suchsel -f de --uniform-distribution -x 5 -y 11 -vv words.txt my_first_suchsel.svg
+------------+
|     P      |
|     A   S  |
|     D   U  |
|     D   C  |
|     E   H  |
|     L   S  |
|     F   E  |
|     I   L  |
|     S      |
|     C      |
|     H      |
+------------+
+------------+
| V J P D B  |
| T G A R S  |
| X S D B U  |
| I M D H C  |
| N N E P H  |
| E H L A S  |
| Z A F Ö E  |
| W J I ß L  |
| W O S Z B  |
| T G C V Ä  |
| P Ö H C V  |
+------------+
```

Where you'll see many more "Ä", "Ö", "Ü"s.

The solution to all puzzles is always included in every SVG as a separate
layer; check out "Layer -> Layers and Objects" in Inkscape, for example, and
choose the visibility that suits your needs.

This is how a PNG rendering then looks like:

![Paddelfisch Suchsel](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/my_first_suchsel.png)

And this is how the solution PNG looks like:

![Paddelfisch Suchsel](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/solution.png)


## Crossword Mode
For crossword mode, you need to use "pysuchsel crossword" instead of "pysuchsel
suchsel". Let's say we add a few more words to our list:

```
$ cat words.txt
SUCHSEL
PADDELFISCH
KREUZWORT
FLUGZEUG
XYLOPHON
```

Then, try to create a crossword:

```
$ pysuchsel crossword -v words.txt my_first_crossword.svg
Warning: could not place word "FLUGZEUG".
Warning: could not place word "KREUZWORT".
 1: PADDELFISCH
 2: SUCHSEL
 3: XYLOPHON
+--------------------------------+
|                                |
|                                |
|                                |
|                                |
|                                |
|                                |
|             v                  |
|             P                  |
|             A                  |
|             D     v            |
|             D     X            |
|             E     Y            |
|             L     L            |
|             F     O            |
|             I     P            |
|           > S U C H S E L .    |
|             C     O            |
|             H     N            |
|             .     .            |
|                                |
+--------------------------------+
```

You'll notice that it was not possible to place all words. You can ask
pysuchsel to re-attempt until it finds a solution that places all words by
specifying the "-a" (or --creation-attempts) parameter:

```
$ pysuchsel crossword -v -a 50 words.txt my_first_crossword.svg
 1: KREUZWORT
 2: XYLOPHON
 3: PADDELFISCH
 4: SUCHSEL
 5: FLUGZEUG
+--------------------------------+
|                                |
|                                |
|                                |
|                                |
|                         v      |
|               v         S      |
|               X         U      |
|               Y         C      |
|   > P A D D E L F I S C H .    |
|         v     O         S      |
|         F     P         E      |
|         L     H         L      |
| > K R E U Z W O R T .   .      |
|         G     N                |
|         Z     .                |
|         E                      |
|         U                      |
|         G                      |
|         .                      |
|                                |
+--------------------------------+
```

The rendering of this now looks like this:

![Paddelfisch Crossword](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/my_first_crossword.png)


## Solution Word Puzzle
Out of the word list, there can also be a puzzle be created that leads to a
specific solution word. This is called the "solution word" mode. For it to
work, you'll need a word list and specify the output word that you want to
create. pysuchsel will tell you if you have enough words to create that puzzle.
For example, you can do this:

```
$ pysuchsel solword -v words.txt solword.svg ITZI
           #
 1  PADDELFISCH
 2 KREUZWORT
 3     FLUGZEUG
 4        MIRABELLE
```

This will also create a puzzle SVG ("solword.svg") which includes the solution
as own separate layers.  This is how it looks:

![Paddelfisch Solution Word](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/solword.png)

![Paddelfisch Solution Word](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/solword_solution.png)


## Crypto Puzzle Mode
pysuchsel can also generate crypto puzzles where each letter corresponds to a
ciphertext character. Only a few letters are revealed and the reader needs to
replace and infer the rest of the letter, possibly using a codeword in the end.

For this, a text file can be generated first:

```
$ cat secret.txt
HELLO THERE
THIS IS A
SECRET MESSAGE
```

Then, simply do:

```
$ pysuchsel crypto -a math secret.txt crypto_puzzle.svg
```

By default, the letters ERNSTL are revealed (on their first occurrence,
respectively). This is how the output looks like:

![Paddelfisch Solution Word](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/crypto_puzzle.png)

The alphabet that is used for ciphertext characters can also be chosen. To learn what is available, consult the help page:

```
$ pysuchsel crypto --help
[...]
  -a {alpha,math,graph,zodiac,chess,runes}, --alphabet {alpha,math,graph,zodiac,chess,runes}
                        Name of the ciphertext alphabet(s) to use. Can be
                        specified multiple times, can be any of alpha, math,
                        graph, zodiac, chess, runes. Must be given at least
                        once.
```

To customize which letters are revealed, use the -r option. For example, to
reveal all vovels:

```
$ pysuchsel crypto -a math -r AEIOU secret.txt crypto_puzzle.svg
```

By specifying the -v option, you can see what the reader can definitely start
with (all the revealed letters are shown, although in the output SVG only the
first occurrence is ever shown):

```
$ pysuchsel crypto -v -a math -r AEIOU secret.txt crypto_puzzle.svg
_E__O __E_E
__I_ I_ A
_E__E_ _E__A_E
```


## License
GNU-GPL 3.
