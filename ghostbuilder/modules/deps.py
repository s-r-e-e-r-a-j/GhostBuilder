# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import json
# import urllib.request
import subprocess
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

def install_with_manager(manager: str, packages: list[str]) -> int:
    if not manager:
        return 2
    cmds: list[list[str]] = []
    if manager == "apt":
        cmds = [
            ["sudo", "apt-get", "update"],
            ["sudo", "apt-get", "install", "-y"] + packages
        ]
    elif manager == "dnf":
        cmds = [["sudo", "dnf", "install", "-y"] + packages]
    elif manager == "pacman":
        cmds = [["sudo", "pacman", "-Syu", "--noconfirm"] + packages]
    for c in cmds:
        rc = run_cmd(c)
        if rc != 0:
            return rc
    if manager == "pacman":
        warn("A restart may be required after full system upgrade.")
        try:
            input("Press Enter to continue...")
        except EOFError:
               pass
    return 0

# TEMP DISABLED: Apktool 3.x compatibility issue.
# Re-enable after Rapid7 adds Apktool 3.x support to Metasploit Framework
# def get_latest_apktool_url() -> str | None:
#    api = "https://api.github.com/repos/iBotPeaches/Apktool/releases/latest"
#    req = urllib.request.Request(
#            api,
#            headers={"User-Agent": "Python"}
#          )
#    try:
#        with urllib.request.urlopen(req) as r:
#              data = json.loads(r.read().decode())
#    except Exception as e:
#            fail(f"failed to fetch latest apktool version: {e}")
#            return None
#    version = data["tag_name"].lstrip("v")
#    return (
#        f"https://github.com/iBotPeaches/Apktool/"
#        f"releases/download/v{version}/apktool_{version}.jar"
#    )

def install_apktool_wget() -> int:
    url = "https://github.com/iBotPeaches/Apktool/releases/download/v2.12.1/apktool_2.12.1.jar"
    if not url:
        return 1

    steps = [
        ["wget", "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool", "-O", "apktool"],
        ["chmod", "+x", "apktool"],
        ["sudo", "mv", "apktool", "/usr/local/bin/"],
        ["wget", url, "-O", "apktool.jar"],
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

def apktool_version_supported() -> bool:
    try:
        output = subprocess.check_output(
            ["apktool", "--version"],
            stderr=subprocess.STDOUT,
            text=True
        ).strip()

        version = output.lstrip("v").split("-")[0]
        major, minor, patch = map(int, version.split(".")[:3])

        return (major, minor, patch) < (3, 0, 0)

    except (FileNotFoundError, ValueError, subprocess.CalledProcessError):
        return False

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
           if t == "apktool" and  ok:
               condition = apktool_version_supported()
               if not condition:
                  res["apktool"] = False
                  ok = False
                  warn("Apktool version >= 3.0.0 detected (unsupported). Removing...")                  
                  steps = [
                      ["sudo", "rm", "-f", "/usr/local/bin/apktool"],
                      ["sudo", "rm", "-f", "/usr/local/bin/apktool.jar"]		
                  ]
                  for s in steps:
                     rc = run_cmd(s)
                     if rc != 0:
                         warn(f"Failed to run: {' '.join(s)}")
        if ok:
            info(f"{t} found")
        else:
            warn(f"{t} missing")
    return res

def auto_install(missing: list[str], auto: bool = False) -> tuple[bool, list[str]]:
    manager = detect_pkg_manager()
    if not manager:
        fail("no supported package manager detected (apt, dnf, pacman)")
        return False, []
    pkgs: list[str] = []
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
            fail(f"package manager install failed for: {pkgs}")
            return False, pkgs
    if need_wget_apktool:
        rc = install_apktool_wget()
        if rc != 0:
            fail("apktool wget install failed")
            return False, pkgs
    return True, pkgs
