# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from typing import List, Tuple
import shutil, os
from .utils import is_installed, info, warn, fail, run_cmd

REQUIRED = ["msfvenom", "msfconsole"]
ANDROID_TOOLS = ["apktool", "zipalign", "jarsigner", "keytool", "aapt", "apksigner"]

def detect_pkg_manager() -> str:
    if shutil.which("apt-get"):
        return "apt"
    if shutil.which("dnf"):
        return "dnf"
    if shutil.which("pacman"):
        return "pacman"
    return ""

def install_with_manager(manager: str, packages: List[str]) -> int:
    if not manager:
        return 2
    cmds: List[List[str]] = []
    if manager == "apt":
        cmds = [
            ["sudo", "apt-get", "update"],
            ["sudo", "apt-get", "install", "-y"] + packages
        ]
    elif manager == "dnf":
        cmds = [["sudo", "dnf", "install", "-y"] + packages]
    elif manager == "pacman":
        cmds = [["sudo", "pacman", "-Sy", "--noconfirm"] + packages]
    for c in cmds:
        rc = run_cmd(c)
        if rc != 0:
            return rc
    return 0

def install_apktool_wget() -> int:
    steps = [
        ["wget", "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool", "-O", "apktool"],
        ["chmod", "+x", "apktool"],
        ["sudo", "mv", "apktool", "/usr/local/bin/"],
        ["wget", "https://github.com/iBotPeaches/Apktool/releases/download/v2.9.3/apktool_2.9.3.jar", "-O", "apktool.jar"],
        ["chmod", "+x", "apktool.jar"],
        ["sudo", "mv", "apktool.jar", "/usr/local/bin/"]
    ]
    for s in steps:
        rc = run_cmd(s)
        if rc != 0:
            return rc
    if not os.path.exists("/usr/local/bin/apktool.jar"):
        fail("apktool.jar missing after install")
        return 1
    return 0

def check_required() -> dict:
    res = {}
    for t in REQUIRED:
        ok = is_installed(t)
        res[t] = ok
        if ok:
            info(f"{t} found")
        else:
            warn(f"{t} missing")
    return res

def check_android_tools() -> dict:
    res = {}
    for t in ANDROID_TOOLS:
        ok = is_installed(t)
        res[t] = ok
        if ok:
            info(f"{t} found")
        else:
            warn(f"{t} missing")
    return res

def auto_install(missing: List[str], auto: bool = False) -> Tuple[bool, List[str]]:
    manager = detect_pkg_manager()
    if not manager:
        fail("no supported package manager detected (apt, dnf, pacman)")
        return False, []
    pkgs: List[str] = []
    need_wget_apktool = False
    for m in missing:
        if m == "apktool":
            need_wget_apktool = True
        elif m == "zipalign":
            pkgs.append("zipalign")
        elif m in ("jarsigner", "keytool"):
            if manager == "apt":
               pkgs.append("openjdk-11-jdk")
            elif manager == "dnf":
                pkgs.append("java-11-openjdk-devel")
            elif manager == "pacman":
                pkgs.append("jdk-openjdk")
        elif m == "aapt":
            pkgs.append("aapt")
        elif m == "apksigner":
            if manager == "apt":
                pkgs.append("android-sdk-build-tools")
            elif manager == "dnf":
                pkgs.append("android-tools")
            elif manager == "pacman":
                pkgs.append("android-sdk-build-tools")
        elif m in ("msfvenom","msfconsole"):
            if manager == "apt":
               pkgs.append("metasploit-framework")
            elif manager == "dnf":
                 pkgs.append("metasploit")
            elif manager == "pacman":
                 pkgs.append("metasploit")
            else:
                 pkgs.append("metasploit-framework")
        else:
            pkgs.append(m)
    if not auto:
        choice = input(f"Install missing packages with {manager}? [y/N]: ").strip().lower()
        if choice != "y":
            return False, pkgs
    if pkgs:
        pkgs = list(dict.fromkeys(pkgs))
        rc = install_with_manager(manager, pkgs)
        if rc != 0:
            fail("package manager install failed for: {pkgs}")
            return False, pkgs
    if need_wget_apktool:
        rc = install_apktool_wget()
        if rc != 0:
            fail("apktool wget install failed")
            return False, pkgs
    return True, pkgs
