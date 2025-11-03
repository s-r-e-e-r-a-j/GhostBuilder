# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from .utils import C

BANNER = r"""
   _____ _               _   ____        _ _     _ 
  / ____| |             | | |  _ \      (_) |   | |
 | |  __| |__   ___  ___| |_| |_) |_   _ _| | __| | ___ _ __
 | | |_ | '_ \ / _ \/ __| __|  _ <| | | | | |/ _` |/ _ \ '__|
 | |__| | | | | (_) \__ \ |_| |_) | |_| | | | (_| |  __/ |
  \_____|_| |_|\___/|___/\__|____/ \__,_|_|_|\__,_|\___|_|

"""

def show() -> None:
    print(C.GREEN)
    print(BANNER)
    print(C.RESET)
