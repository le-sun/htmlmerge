Html Merge
==========

Merges html files that are created by pdfminer.six using -Y exact.

To use:

from htmlmerge import html_merge
f = open('foo.html', 'rb').read()
foobar = html_merge(f)
result = foobar.run()
