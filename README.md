AMAer
=====

AMAer ("Adjacency Matrix-er") turns a list of nodes and their connections...

    id1   abc   def   ghi
    id2   abc   def
    id3   ghi   jkl

...into an [adjacency matrix](http://en.wikipedia.org/wiki/Adjacency_matrix):

          abc   def   ghi   jkl
    abc          2     1     0
    def    2           1     0
    ghi    1     1           1
    jkl    0     0     1     0

Inputs and outputs somewhat Excel-compliant CSV.

**Note:** To use the output with Gephi, note that the keywords ("abc", "def"... in previous example) should not contain spaces or commas.

Basic usage: `python amaer.py input.csv output.csv`

For more, see: `python amaer.py --help`

---

&copy; 2013 [Petteri Noponen](https://github.com/petterin) (Licensed under the [MIT License](LICENSE))
