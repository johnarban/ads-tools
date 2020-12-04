#!/usr/bin/env python
# coding: utf-8
import os
import ads

# if you don't want bibtexabs, pip install abs,
# otherwise pip install git+git://github.com/andycasey/ads@master
# this script currently has bibtexabs hardcoded in two places
# a simple find/replace should be safe to change it to bibtex
import requests  # pip install requests
import math
import argparse


# code source:
# https://github.com/adsabs/ads-examples/blob/master/library_csv/lib_2_csv.py


def get_config(token=None):
    """
    Load ADS developer key from file
    :return: str
    @andycasey
    """
    # global token
    if token is None:
        try:
            with open(os.path.expanduser("~/.ads/dev_key")) as f:
                # ~/.ads/dev_key should contain your ADS API token
                token = f.read().strip()
        except IOError:
            print(
                "The script assumes you have your ADS developer token in the"
                "folder: {}".format()
            )

    return {
        "url": "https://api.adsabs.harvard.edu/v1/biblib",
        "headers": {
            "Authorization": "Bearer:{}".format(token),
            "Content-Type": "application/json",
        },
    }

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Add bibcode to Bibtex file"
    )

    parser.add_argument('bibcode_list',nargs='+',help='list of bibcodes separated by a space')
        
        
    parser.add_argument(
        "-t",
        "--token",
        default=None,
        help="ADS developer token otherwise defaults to ~/.ads/dev_key",
    )

    parser.add_argument(
        "-b",
        "--bibcodes",
        help="name of file to store bibcodes",
        default="bibcodes",
        dest="bibcodes",
    )

    parser.add_argument(
        "-f",
        "--bibfile",
        help="name of bibtex (.bib) file",
        default="library.bib",
        dest="bibfile",
    )

    parser.add_argument(
        "--bib-format",
        choices=["bibtex", "bibtexabs"],
        help="""[[DISABLED]] Format for bibtex file. 
                       bibtexabs only works if using the git version of the abs module""",
        default="bibtex",
    )

    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()
    bibcodefile = args.bibcodes
    bibfile = args.bibfile
    token = args.token
    
    bibcodes = args.bibcode_list
    print(bibcodes)
    
    if args.debug:
        print(bibcodefile)
        print(bibfile)
        print(token)

    

    print("Adding {} new items".format(len(bibcodes)))
    bibtex = ads.ExportQuery(bibcodes, format=args.bib_format).execute()

    with open(bibcodefile, "a+") as f:
        f.writelines("{}\n".format(bc) for bc in bibcodes)
    with open(bibfile, "a+") as f:
        f.write("\n\n\n\n\n")
        f.write(bibtex)
