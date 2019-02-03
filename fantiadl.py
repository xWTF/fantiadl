#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download media and other data from Fantia"""

import argparse
import sys

from models import FantiaDownloader, FantiaClub

__author__ = "bitbybyte"
__copyright__ = "Copyright 2018 bitbybyte"

__license__ = "MIT"
__version__ = "1.0"

if __name__ == "__main__":
    cmdl_usage = "%(prog)s session_key url"
    cmdl_version = __version__
    cmdl_parser = argparse.ArgumentParser(usage=cmdl_usage, conflict_handler="resolve")

    cmdl_parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="suppress output")
    cmdl_parser.add_argument("-v", "--version", action="version", version=cmdl_version)
    cmdl_parser.add_argument("session_key", help="session key")
    cmdl_parser.add_argument("url", help="fanclub or post URL")

    dl_group = cmdl_parser.add_argument_group("download options")
    dl_group.add_argument("-o", "--output-directory", dest="output_path", help="directory to download to")
    dl_group.add_argument("-m", "--dump-metadata", action="store_true", dest="dump_metadata", help="store metadata to file")

    cmdl_opts = cmdl_parser.parse_args()

    downloader = FantiaDownloader(cmdl_opts.session_key, dump_metadata=cmdl_opts.dump_metadata, directory=cmdl_opts.output_path, quiet=cmdl_opts.quiet)

    url_groups = downloader.FANTIA_URL_RE.match(cmdl_opts.url)
    if url_groups:
        if url_groups[1] == "fanclubs":
            fanclub = FantiaClub(url_groups[2])
            downloader.download_fanclub_posts(fanclub)
        elif url_groups[1] == "posts":
            downloader.download_post(url_groups[2])
    else:
        sys.exit("Please provide a valid Fantia URL (/posts/[id], /fanclubs/[id])")
