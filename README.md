# pysuchsel
pysuchsel is a program to create "Suchsel" word puzzles (i.e., a rectangular
array of letters which have words hidden within that you need to find). From a
given word list and grid size and filling rules, it creates an SVG image that
can easily printed. 

It can fill all the void spaces with random letters that are uniformly
distributed or it can choose a random distribution that satisfies a natural
language (German and English are supported), making the Suchsel much more
difficult. It also supports hiding words left-to-right, right-to-left,
top-to-bottom, bottom-to-top, diagonally-to-top-right, diagonally-to-top-left,
diagonally-to-bottom-right, diagonally-to-bottom-left or any combination of
these placements.

## Usage
You'll first have to create a file that contains all the words (e.g., using
pluma or vim). We'll call it words.txt

```
$ cat words.txt
SUCHSEL
PADDELFISCH
```

Our file only contains two words. Then, you can already call pysuchsel to place them:

```
$ ./pysuchsel words.txt my_first_suchsel.svg
```

If you want to see where they were placed, specify "-v" as well:

```
$ ./pysuchsel -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel -x 11 -y 11 -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel -c -x 11 -y 11 -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel -c -x 11 -y 11 -vv words.txt my_first_suchsel.svg
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
$ ./pysuchsel -x 11 -y 11 -p dbr -v words.txt my_first_suchsel.svg
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
$ ./pysuchsel -x 11 -y 11 -p tb -p bt -v words.txt my_first_suchsel.svg
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

To influence the padding of letters, look at the "-d" option. By default,
padded letters are uniformly distributed (i.e., each letter has the same
probability of occurrence). That makes uncommon letters (e.g., Q and Y in the
German language) rather frequent and stand out. For example:

```
$ ./pysuchsel -x 5 -y 11 -vv words.txt my_first_suchsel.svg
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
| P L I B Q  |
| A H J E D  |
| D O H F Q  |
| D S L B G  |
| E U C K L  |
| L C J I I  |
| F H O K I  |
| I S S G A  |
| S E D X X  |
| C L K E K  |
| H S I L Q  |
+------------+
```

Compare that to:

```
$ ./pysuchsel -x 5 -y 11 -d natlang-de -vv words.txt my_first_suchsel.svg
+------------+
|   P        |
|   A        |
|   D        |
|   D        |
|   E   S    |
|   L   U    |
|   F   C    |
|   I   H    |
|   S   S    |
|   C   E    |
|   H   L    |
+------------+
+------------+
| D P C W D  |
| R A S L F  |
| S D T U E  |
| Z D V N C  |
| S E H S K  |
| I L N U N  |
| W F K C S  |
| G I N H H  |
| A S N S T  |
| G C T E N  |
| N H U L E  |
+------------+
```

This is how a PNG rendering then looks like:

![Paddelfisch Suchsel](https://raw.githubusercontent.com/johndoe31415/pysuchsel/master/docs/my_first_suchsel.png)


## License
GNU-GPL 3.
