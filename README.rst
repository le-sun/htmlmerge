Html Merge
==========

Merges html files that are created by pdfminer.six using -Y exact.

To use:

f = open('foo.html', 'rb').read()
foobar = htmlmerge(f)
result = foobar.run()
