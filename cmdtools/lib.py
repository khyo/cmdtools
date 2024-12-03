import subprocess


def sh(cmd: str, shell=True, check=True, stdout=None, encoding="utf-8", **kwargs):
    return subprocess.run(cmd, shell=shell, check=check, stdout=stdout, encoding=encoding, **kwargs)


def sh_output(cmd: str):
    out = sh(cmd, stdout=subprocess.PIPE).stdout.strip()
    print(out)
    return out
