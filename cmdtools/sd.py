#! /usr/bin/env python3
import time
import argparse
from .lib import sh


def main():
    parser = argparse.ArgumentParser(description="systemctl cmdline helper")
    parser.add_argument("service", help="service to be operated on", nargs="?")
    parser.add_argument("-e", "--enable", help="systemctl enable", action="store_true")
    parser.add_argument("-d", "--disable", help="systemctl disable", action="store_true")
    parser.add_argument("-s", "--start", help="systemctl start", action="store_true")
    parser.add_argument("-p", "--stop", help="systemctl stop", action="store_true")
    parser.add_argument("-r", "--restart", help="systemctl restart", action="store_true")
    parser.add_argument("-t", "--status", help="systemctl status", action="store_true")
    parser.add_argument("-g", "--grep", help="systemctl | grep {service}", action="store_true")
    parser.add_argument("-j", "--journal", help="journalctl -u {service}", action="store_true")
    parser.add_argument("-f", "--follow", help="journalctl -fu {service}", action="store_true")
    parser.add_argument("-l", "--daemonreload", help="systemctl daemon-reload", action="store_true")
    parser.add_argument("-u", "--user", help="--user param", action="store_true")

    args = parser.parse_args()

    exe = "sudo systemctl"
    if args.user:
        exe = f"{exe} --user"

    if args.daemonreload:
        sh(f"sudo systemctl daemon-reload")
        if (not args.service):
            return

    if args.enable:
        sh(f"{exe} enable {args.service}")
    elif args.disable:
        sh(f"{exe} disable {args.service}")
    elif args.start:
        sh(f"{exe} start {args.service}")
        time.sleep(1)
        sh(f"{exe} status {args.service}")
    elif args.stop:
        sh(f"{exe} stop {args.service}")
    elif args.restart:
        sh(f"{exe} restart {args.service}")
        time.sleep(1)
        sh(f"{exe} status {args.service}")
    elif args.grep:
        sh(f"{exe} | grep --color=always {args.service}")
    elif args.follow:
        sh(f"sudo journalctl -fu {args.service}")
    elif args.journal:
        sh(f"sudo journalctl -u {args.service}")
    elif args.status:
        sh(f"{exe} status {args.service}")
    else:
        sh(f"{exe} status {args.service}")


if __name__ == "__main__":
    main()

