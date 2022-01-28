#!/usr/bin/env python3
import argparse
import json
import os
import subprocess as sub
import sys

from bln.client import Client


def parse_args(argv):
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description="Big Local News Python Client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub = parser.add_subparsers(help="commands", dest="command")
    upload = sub.add_parser(
        "upload",
        help="upload files to a project",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    if is_git(sys.argv[0]):
        upload.add_argument(
            "-p",
            "--project_id",
            help="project ID on Big Local News platform"
            "; if not specified, will use projectId in ~/.git/bln.json",
        )
    else:  # regular `bln` command
        upload.add_argument(
            "project_id",
            help="project ID on Big Local News platform",
        )
    upload.add_argument(
        "files",
        nargs="+",
        help="list of files to upload",
    )
    upload.add_argument(
        "-k",
        "--api_key",
        help="if not specified, looks for one at ~/.bln/api_key",
    )
    upload.add_argument(
        "-t",
        "--tier",
        help='which tier; external parties will only be able to use "prod"',
        default="prod",
    )
    return parser.parse_args(argv[1:])


def is_git(cmd):
    """Test if a git command."""
    return cmd.endswith("git-bln")


def git_root():
    """Return the git root."""
    return (
        sub.Popen(["git", "rev-parse", "--show-toplevel"], stdout=sub.PIPE)
        .communicate()[0]
        .rstrip()
        .decode("utf-8")
    )


if __name__ == "__main__":
    args = parse_args(sys.argv)
    # create api_key directory
    bln_dir = os.path.expanduser("~/.bln")
    if not os.path.exists(bln_dir):
        os.mkdir(bln_dir)
    # use and save API key or load from {api_key_path}
    api_key_path = os.path.expanduser("~/.bln/api_key")
    if args.api_key:
        api_key = args.api_key
        with open(api_key_path, "w") as f:
            f.write(api_key)
        print(
            f"API key saved to {api_key_path}; future calls will use this "
            "API key as a default."
        )
    else:
        if not os.path.exists(api_key_path):
            print(
                "Must provide an API key, i.e. `-k <key>`; keys "
                "can be obtained from https://biglocalnews.org/#/manage_keys"
            )
            sys.exit(1)
        with open(api_key_path) as f:
            api_key = f.read().strip()
    # if git, use projectId from .git/bln.json, otherwise use args.project_id
    project_id = args.project_id
    if is_git(sys.argv[0]):
        git_bln_path = os.path.join(git_root(), "bln.json")
        if args.project_id:
            with open(git_bln_path, "w") as f:
                json.dump({"projectId": args.project_id}, f)
        else:
            if not os.path.exists(git_bln_path):
                print("Must provide a project ID!")
                sys.exit(1)
            with open(git_bln_path) as f:
                d = json.load(f)
            project_id = d.get("projectId", None)
            if not project_id:
                print("Must provide a project ID!")
                sys.exit(1)
    client = Client(api_key, args.tier)
    {
        "upload": lambda: client.upload_files(project_id, args.files),
    }[args.command]()
