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

Recommended alterations:
 - I increase the number of row retreived with each API call to 500. This is done by setting `rows` in the `get_library` function definition
  - This *should* be made an option that is settable from the command line. *Shoulda, woulda, coulda*. 
 - Future versions should save config options to the `library.id` file
  - like the bibcode file, bibtex file, number of rows, etc. that way you can customize the results w/o modifying the script


Credit: Thank you to [@adsabs](https://twitter.com/adsabs/status/1334569272778035207) for the tweet which led me down this road
 
