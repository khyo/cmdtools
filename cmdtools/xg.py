#!/usr/bin/env python3
import os
import argparse
import re
from .lib import sh, sh_output, subprocess


def main():
    parser = argparse.ArgumentParser(description="git commandline helper")
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(title="subcommands")

    sparser = subparsers.add_parser("p", help="git add . && git commit -m{ARGS} && git push")
    sparser.add_argument("msg", help="commit message, or use pull [reset] to pull all git repos", nargs="*")
    sparser.add_argument(
        "-a", "--all", help="perform gitp on all valid git repo directories including '.'", action="store_true"
    )
    sparser.add_argument(
        "-f", "--force", help="perform git add -> commit --ammend -> push --force", action="store_true"
    )
    sparser.add_argument("-p", "--patch", help="increment the repo's patch version", action="store_true")
    sparser.add_argument("-m", "--minor", help="increment the repo's minor version", action="store_true")
    sparser.add_argument("-M", "--major", help="increment the repo's major version", action="store_true")
    sparser.set_defaults(func=push)

    sparser = subparsers.add_parser("forcepull", help="force pull the repo on this branch (defaults to current branch)")
    parser.add_argument("branch", default="*", nargs="?")
    sparser.set_defaults(func=force_pull)

    args = parser.parse_args()
    if args.func:
        args.func(args)
    else:
        parser.parse_args("-h")


def push(args):
    if branch := args.forcepull:
        force_pull(branch)
        return

    if not len(args.msg) and not args.force:
        print("invalid args: a commit message must be supplied!")
        return

    msg = " ".join(args.msg)
    pull = msg == "pull"
    reset_then_pull = msg == "pull reset"
    force = args.force

    repos = []
    if args.all or pull or reset_then_pull:
        dirs = next(os.walk("."))[1] + ["."]
        for d in dirs:
            if os.path.exists(os.path.join(d, ".git")):
                repos.append(d)
    else:
        repos.append(".")

    cwd = os.path.abspath(os.getcwd())

    for repo in repos:
        try:
            repo_path = os.path.join(cwd, repo)
            print(">>>>", repo_path)
            os.chdir(repo_path)

            pushTags = None

            if pull:
                sh("git pull")
            elif reset_then_pull:
                sh("git reset HEAD --hard")
                sh("git pull")
            elif force:
                existing_tag = sh_output("git tag --contains HEAD")
                if not msg:
                    msg = sh_output("git log -1 --pretty=%B")
                sh("git add .")
                sh('git commit --amend -m"{}"'.format(msg))
                pushTags = rev_tag(args.major, args.minor, args.patch)
                if existing_tag:
                    sh('git tag {} -m" " --force'.format(existing_tag))
                    pushTags = True
                sh("git push --force")
            else:
                sh("git add .")
                sh('git commit -m"{}"'.format(msg))
                pushTags = rev_tag(args.major, args.minor, args.patch)
                sh("git push")

            if pushTags:
                sh("git push --tags --force")
        except Exception as ex:
            print(ex)


def force_pull(args):
    branch: str = args.branch
    if branch == "*":
        branch = get_current_branch()

    remotes = get_remotes()
    remote = "origin"
    if remote not in remotes:
        remote = remotes[0]

    print(f"force pulling from {remote}/{branch}")
    sh(f"git fetch {remote} {branch}")
    sh(f"git reset --hard {remote}/{branch}")
    sh("git pull --tags --force")


def rev_tag(revmaj: bool, revmin: bool, revpatch: bool):
    if revmaj:
        version = get_version()
        version[0] += 1
        version[1] = 0
        version[2] = 0
        sh('git tag v{}.{}.{} -m" "'.format(*version))
        return True

    elif revmin:
        version = get_version()
        version[1] += 1
        version[2] = 0
        sh('git tag v{}.{}.{} -m" "'.format(*version))
        return True

    elif revpatch:
        version = get_version()
        version[2] += 1
        sh('git tag v{}.{}.{} -m" "'.format(*version))
        return True

    return None


def get_version():
    try:
        vstr = sh("git describe", stdout=subprocess.PIPE).stdout.strip()
        res = re.search(r"v\d+\.\d+\.\d+", vstr)
        if res:
            version = res.group(0)
            return list(int(x) for x in version[1:].split("."))
    except Exception:
        pass
    return [0, 0, 0]


def get_current_branch():
    for line in sh("git branch", stdout=subprocess.PIPE).stdout.splitlines():
        if "*" in line:
            return line.split("*")[1].strip()
    raise Exception("no branch detected")


def get_remotes():
    return list(line.strip() for line in sh("git remote", stdout=subprocess.PIPE).stdout.splitlines())
