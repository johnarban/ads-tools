# ads-tools
tools<sup>*</sup> for working with ADS

<sup>*</sup> _tool**s**_ in the classic _singular_ sense of the plural




## ads_lib_pull.py
You **need** an ADS API token for this to work. You can get one with an ADS account [here](https://ui.adsabs.harvard.edu/user/settings/token)

Requirements:
 - ads from Andy Casey: https://github.com/andycasey/ads `pip install ads`
 - requests: fairly standard package.https://requests.readthedocs.io/en/master/user/install/  `pip install requests`
 
call with `python ads_lib_pull.py`
or `chmod +x` the file, to make it executable without `python` at the beginning. 

Use case:

```bash
> cd ~/Overleaf/MySharedBibTexFile
> ads_lib_pull.py -l [library_id] -t [TOKEN]
> ls
 bibcodes
 libraries.bib
```
After making changes to the library, run the command again to get update the .bib file. Or, you can
add merge a 2nd library. Duplicate entries won't be added.

______________________________
```

usage: ads_lib_pull.py [-h] [-l LIBRARY_ID] [-t TOKEN] [-r] [--list] [-b BIBCODES] [-f BIBFILE]
                       [--bib-format {bibtex,bibtexabs}] [--api-rows API_ROWS] [--debug]

Create/update a bibliography file for an ADS Library

optional arguments:
  -h, --help            show this help message and exit
  -l LIBRARY_ID, --library_id LIBRARY_ID
                        ID of ADS Library: https://ui.adsabs.harvard.edu/user/libraries/[library_id]. If not passed, it
                        should either be hardcoded or in the file library.id. library.id is created when the script is
                        first run
  -t TOKEN, --token TOKEN
                        ADS developer token otherwise defaults to ~/.ads/dev_key
  -r, --refresh         create a new bibtex file and bibcode list even if one exists. This will overwrite any changes
                        you've made
  --list, --list-libaries
                        List your library names and IDs
  -b BIBCODES, --bibcodes BIBCODES
                        name of file to store bibcodes
  -f BIBFILE, --bibfile BIBFILE
                        name of bibtex (.bib) file
  --bib-format {bibtex,bibtexabs}
                        [[DISABLED]] Format for bibtex file. bibtexabs only works if using the git version of the abs
                        module
  --api-rows API_ROWS   number of rows retreived with each api call to download the library
  --debug

```

Recommended alterations:
 - I increase the number of row retreived with each API call to 500. This is done by setting `--api-rows` in the call
   - ~This *should* be made an option that is settable from the command line. *Shoulda, woulda, coulda*.~
 - Future versions should save config options to the `library.id` file
   - like the bibcode file, bibtex file, number of rows, etc. that way you can customize the results w/o modifying the script


Credit: Thank you to [@adsabs](https://twitter.com/adsabs/status/1334569272778035207) for the tweet which led me down this road
 
