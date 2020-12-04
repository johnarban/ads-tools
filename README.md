# ads-tools
tools<sup>*</sup> for working with ADS

<sup>*</sup> tools in the singular sense

call with `python update_bibliography.py`

or `chmod +x` the file, to make it executable without `python` at the beginning. 
```

usage: update_bibliography.py [-h] [-l LIBRARY_ID] [-t TOKEN] [-b BIBCODES] [-f BIBFILE]
                              [--bib-format {bibtex,bibtexabs}] [--list]

Create/update a bibliography file for an ADS Library

optional arguments:
  -h, --help            show this help message and exit
  -l LIBRARY_ID, --library_id LIBRARY_ID
                        ID of ADS Library: https://ui.adsabs.harvard.edu/user/libraries/[library_id]. If not passed, it
                        should either be hardcoded or in the file library.id. library.id is created when the script is
                        first run
  -t TOKEN, --token TOKEN
                        ADS developer token otherwise defaults to ~/.ads/dev_key
  -b BIBCODES, --bibcodes BIBCODES
                        name of file to store bibcodes
  -f BIBFILE, --bibfile BIBFILE
                        name of bibtex (.bib) file
  --bib-format {bibtex,bibtexabs}
                        [[DISABLED]] Format for bibtex file. bibtexabs only works if using the git version of the abs
                        module
  --list, --list-libaries
                        List your library names and IDs
```

