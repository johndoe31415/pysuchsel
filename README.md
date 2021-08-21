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
$ ./pysuchsel suchsel words.txt my_first_suchsel.svg
```

If you want to see where they were placed, specify "-v" as well:

```
$ ./pysuchsel suchsel -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -x 11 -y 11 -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -c -x 11 -y 11 -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -c -x 11 -y 11 -vv words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -x 11 -y 11 -p dbr -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -x 11 -y 11 -p tb -p bt -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -x 5 -y 11 -vv words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -f de -x 5 -y 11 -vv words.txt my_first_suchsel.svg
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
$ ./pysuchsel suchsel -f de --uniform-distribution -x 5 -y 11 -vv words.txt my_first_suchsel.svg
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

You can also generate not only the puzzle itself, but also the solution for the puzzle by specifying the "-s" option:

```
$ ./pysuchsel suchsel -f de -x 15 -y 15 -s solution.svg -vv words.txt my_first_suchsel.svg
+--------------------------------+
|                                |
|                       P        |
|                       A        |
|                       D        |
|                       D        |
|                       E        |
|                       L        |
|                       F        |
|                       I        |
|   S U C H S E L       S        |
|                       C        |
|                       H        |
|                                |
|                                |
|                                |
+--------------------------------+
+--------------------------------+
| Ü E N N D H C I R E T L H D M  |
| Ö S N E N A E N I M R P S S N  |
| I N Ä W A A I N T E M A E N R  |
| E O K R I V B E Z B R D Z A N  |
| G Ü I H E M E E L E L D B E L  |
| R T N T W N C R L H E E F Q F  |
| A G T A H F G G R Z A L S L U  |
| P E Ü I C G T R E F T F E E E  |
| E O N A S T D A R R E I F E E  |
| H S U C H S E L I A G S O F S  |
| S E I A R N R T N N T C N I B  |
| E S E U A G D E N D U H E R G  |
| S F E W E R U B R L E A O E E  |
| D E I N B E R H Ü B B E C O E  |
| I R H D T A R I F E S M N E S  |
+--------------------------------+
```

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
$ ./pysuchsel crossword -v words.txt my_first_crossword.svg
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
$ ./pysuchsel crossword -v -a 50 words.txt my_first_crossword.svg
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

## License
GNU-GPL 3.
