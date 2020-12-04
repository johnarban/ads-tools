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


def get_libraries():
    """
    Get a list of all my libraries and their meta-data
    :return: list
    @andycasey
    """

    config = get_config()

    r = requests.get("{}/libraries".format(config["url"]), headers=config["headers"])

    # Collect a list of all of our libraries, this will include the number
    # of documents, the name, description, id, and other meta data
    try:
        data = r.json()["libraries"]
        return data
    except ValueError:
        raise ValueError(r.text)


def get_library(library_id, num_documents, start=0, rows=25):
    """
    Get the content of a library when you know its id. As we paginate the
    requests from the private library end point for document retrieval,
    we have to repeat requests until we have all documents.
    :param library_id: identifier of the library
    :type library_id:
    :param num_documents: number of documents in the library
    :type num_documents: int
    :param start: start with a given row
    :type start: int
    :param rows: number of rows to request
    :type rows: int
    :return: list
    @andycasey
    CHANGES: @astrojthe3 - Dec 4 2020
              added start keyword, 
              to start at arbitrary row
    """

    config = get_config()

    # start = 0
    num_documents -= start
    # rows = 25
    num_paginates = int(math.ceil(num_documents / (1.0 * rows)))

    documents = []
    for i in range(num_paginates):
        print("Pagination {} out of {}: rows:".format(i + 1, num_paginates))

        r = requests.get(
            "{}/libraries/{id}?start={start}&rows={rows}".format(
                config["url"], id=library_id, start=start, rows=rows
            ),
            headers=config["headers"],
        )

        # Get all the documents that are inside the library
        try:
            data = r.json()["documents"]
        except ValueError:
            raise ValueError(r.text)

        documents.extend(data)

        start += rows

    return documents


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create/update a bibliography file\n for an ADS Library"
    )

    parser.add_argument(
        "-l",
        "--library_id",
        help="""ID of ADS Library: https://ui.adsabs.harvard.edu/user/libraries/[library_id]. 
                If not passed, it should either be hardcoded or in the file library.id. 
                library.id is created when the script is first run""",
    )

    parser.add_argument(
        "-t",
        "--token",
        default=None,
        help="ADS developer token otherwise defaults to ~/.ads/dev_key",
    )

    parser.add_argument(
        "-r",
        "--refresh",
        action="store_true",
        help="create a new bibtex file and bibcode list even if one exists. This will overwrite any changes you've made",
    )

    parser.add_argument(
        "--list",
        "--list-libaries",
        action="store_true",
        help="List your library names and IDs",
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

    parser.add_argument(
        "--api-rows",
        type=int,
        help="number of rows retreived with each api call to download the library",
        default=25,
    )

    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    library_id = args.library_id
    bibcodefile = args.bibcodes
    bibfile = args.bibfile

    # get the saved library ID
    # if one isn't passed
    if os.path.isfile("library.id"):
        with open("library.id", "r") as f:
            lib_config = f.read()
        if library_id is None:
            library_id = lib_config
    #             if bibcodefile is None:
    #                 bibcodefile = lib_config[1]
    #             if bibfile is None:
    #                 bibfile = lib_config[2]

    token = args.token
    refresh = args.refresh
    rows = args.api_rows

    if args.debug:
        print(bibcodefile)
        print(bibfile)
        print(token)
        print(refresh)
        print(rows)

    if args.list:
        libraries = get_libraries()
        n = max([len(n["name"]) for n in libraries])
        print(("{:>%s}   {}" % n).format("NAME", "ADS ID"))
        print("-" * 72)
        for item in libraries:
            print(("{:>%s}   {}" % n).format(item["name"], item["id"]))

    # id I have no library_id
    # exit with a message
    elif library_id is None:
        print("Please provide library ID, or hardcode one")
        print("run with the --list flag to list available libraries")
    else:

        config = get_config(token)  # if there is no token it will fail thnx
        # to @andycasey's much better coding which
        # actually catches exceptions

        # we need to get the number of entries in the library
        # that is stored in metadata
        r = requests.get(
            "{}/libraries/{id}".format(config["url"], id=library_id),
            headers=config["headers"],
        )
        metadata = r.json()["metadata"]

        # if we are running for the first time
        # then there is no file of bibcodes to compare to
        # so we will just download the whole library
        if (not os.path.isfile(bibcodefile)) or refresh:
            print(
                'Creating new bib file for ADS Library "{}", id: {}'.format(
                    metadata["name"], metadata["id"]
                )
            )

            library = get_library(
                library_id=metadata["id"],
                num_documents=metadata["num_documents"],
                rows=rows,
            )
            print("New bib file has {} items".format(len(library)))

            bibtex = ads.ExportQuery(library, format=args.bib_format).execute()

            with open("library.id", "w") as f:
                f.write(library_id)
            #                 f.write(bibcodefile)
            #                 f.write(bibfile)

            with open(bibcodefile, "w") as f:
                f.writelines("{}\n".format(bc) for bc in library)

            with open(bibfile, "w") as f:
                f.write(bibtex)

        # if there is a file of bibcodes we
        # need to compare with it. Unfortunately,
        # we have to download the entire library
        # for this too. A savvy person could do some
        # table manipulation server side via the API
        # to offload some of the work, but that might
        # be even slower, than downloading
        elif os.path.isfile(bibcodefile):
            print("bibcode file {} already exists".format(bibcodefile))
            with open(bibcodefile, "r") as f:
                current = [i.strip() for i in f.readlines()]
            print("Contains {} items".format(len(current)))

            library = get_library(
                library_id=metadata["id"],
                num_documents=metadata["num_documents"],
                rows=rows,
            )

            # get the exclusive join of the sets
            new = list(set(current) ^ set(library))
            if len(new) > 0:
                print("Adding {} new items".format(len(new)))
                bibtex = ads.ExportQuery(new, format=args.bib_format).execute()

                with open(bibcodefile, "a") as f:
                    f.writelines("{}\n".format(bc) for bc in new)
                with open(bibfile, "a") as f:
                    f.write("\n\n\n\n\n")
                    f.write(bibtex)
