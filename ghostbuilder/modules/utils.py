# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from typing import List
import shutil
import subprocess
import os

class C:
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"

def info(text: str) -> None:
    print(f"{C.CYAN}[ * ]{C.RESET} {text}")

def ok(text: str) -> None:
    print(f"{C.GREEN}[ + ]{C.RESET} {text}")

def warn(text: str) -> None:
    print(f"{C.YELLOW}[ ! ]{C.RESET} {text}")

def fail(text: str) -> None:
    print(f"{C.RED}[ X ]{C.RESET} {text}")

def ask(prompt: str) -> str:
    return input(f"{C.MAGENTA}{prompt}{C.RESET}")

def run_cmd(cmd: List[str], silent: bool = False) -> int:
    try:
        if silent:
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            res = subprocess.run(cmd)
        return res.returncode
    except FileNotFoundError:
        return 127

def is_installed(name: str) -> bool:
    return shutil.which(name) is not None

def validate_ip(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        n = int(p)
        if n < 0 or n > 255:
            return False
    return True

def validate_port(p: str) -> bool:
    if not p.isdigit():
        return False
    n = int(p)
    return 1 <= n <= 65535

def clear() -> None:
    os.system("clear")
