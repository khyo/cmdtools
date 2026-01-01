#!/usr/bin/env python3
import os
import argparse
import re
from pathlib import Path
from .lib import sh, sh_output, subprocess


def main():
    parser = argparse.ArgumentParser(description=".AppImage launcher")
    parser.add_argument("path", help="working directory where a .AppImage file must live to be launched")
    parser.add_argument("extra_args", nargs=argparse.REMAINDER, help="additional arguments to pass to the AppImage")

    # dispatch subcommand
    args = parser.parse_args()
    if args.path:
        launch(args)
    else:
        parser.parse_args("-h")


def launch(args):
    wd = Path(args.path)
    print("pathy", args.path, wd )

    exe = ""
    for f in os.listdir(wd):
        exe =  f
        if f.lower().endswith(".appimage"):
            execute(wd, f, args.extra_args)
            return
    if exe:
        execute(wd, exe, args.extra_args)


def execute(wd: Path, f: str, extra_args: list):
    af = wd.joinpath(f)
    af.chmod(af.stat().st_mode | 0o111)  # Add executable permission for user, group, and others
    sh(str(af), *extra_args)  # Launch the AppImage with additional arguments
