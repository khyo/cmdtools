#!/usr/bin/env python3
import os
import pwd

import argparse
import re
from pathlib import Path
from .lib import sh, sh_output, subprocess


def main():
    parser = argparse.ArgumentParser(description=".AppImage launcher")
    parser.add_argument("path", help="working directory where a .AppImage file must live to be launched (also fixpwas)")
    parser.add_argument("extra_args", nargs=argparse.REMAINDER, help="additional arguments to pass to the AppImage")

    # dispatch subcommand
    args = parser.parse_args()

    if args.path:
        if args.path == "fixpwas":
            fixpwas()
            return
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


def get_username():
    return pwd.getpwuid(os.getuid())[0]

def fixpwas():
    rootdir = f"/home/{get_username()}/.local/share/applications"
    any_changed = False
    for fname in os.listdir(rootdir):
        if fname.startswith("msedge-"):
            fullpath = os.path.join(rootdir, fname)
            with open(fullpath, mode="r") as f:
                lines = f.readlines()
            changed = False
            for i in range(0, len(lines)):
                line = lines[i]
                if line.startswith("StartupWMClass=crx__"):
                    changed = True
                    newline = line.replace("StartupWMClass=crx__", "StartupWMClass=msedge-_") + "-Default"
                    print(f"fixpwas: changing '{fullpath}' from '{line}' -> '{newline}'")
                    lines[i] = newline
            if changed:
                any_changed = True
                with open(fullpath, mode="w") as f:
                    f.writelines(lines)
    if any_changed:
        print("running", f"update-desktop-database /home/{get_username()}/.local/share/applications")
        sh(f"update-desktop-database /home/{get_username()}/.local/share/applications")
                