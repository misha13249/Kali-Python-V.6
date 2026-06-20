#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
             MONOLITHIC KALI LINUX SUBSYSTEM SIMULATOR (v6.0)
=============================================================================
Добавлены: burpsuite, zaproxy, nikto, dirb, gobuster, wpscan, whatweb,
           theharvester, recon-ng, maltego, set, bettercap, ettercap,
           responder, bloodhound, mimikatz, hashcat, crunch, cupp, seclists,
           rsactftool, fcrackzip, pdfcrack, airgeddon, fluxion, kismet,
           dsniff, mitmproxy, sslstrip, sslsplit, tcpdump, tshark,
           medusa, ncrack, patator, а также новые PIP-модули.
=============================================================================
"""

import os
import sys
import time
import random
import re
import hashlib
import readline
from datetime import datetime

# =============================================================================
# РЕПОЗИТОРИИ УДАЛЕННЫХ СЕРВЕРОВ (с зависимостями)
# =============================================================================

APT_REMOTE_REPOSITORY = {
    # Базовые
    "python3": {"version": "3.11.2-1", "size": "34.2 MB", "desc": "Interactive high-level language", "deps": ["libpython3.11", "python3-minimal"]},
    "nmap": {"version": "7.93+dfsg1-1", "size": "5.8 MB", "desc": "Network Mapper", "deps": ["libpcap0.8", "liblua5.3"]},
    "hydra": {"version": "9.4-1", "size": "1.2 MB", "desc": "Network logon cracker", "deps": ["libssl3", "libc6"]},
    "macchanger": {"version": "1.7.0-1", "size": "220 KB", "desc": "MAC manipulator", "deps": []},
    "curl": {"version": "7.88.1-10", "size": "410 KB", "desc": "URL transfer tool", "deps": ["libcurl4"]},
    "htop": {"version": "3.2.2-1", "size": "1.1 MB", "desc": "Process viewer", "deps": ["libncursesw6", "libc6"]},
    "tree": {"version": "2.1.0-1", "size": "120 KB", "desc": "Directory tree", "deps": []},
    "nano": {"version": "7.2-1", "size": "450 KB", "desc": "Text editor", "deps": ["libncursesw6"]},
    "sqlmap": {"version": "1.8.2-1", "size": "3.2 MB", "desc": "Automatic SQL injection tool", "deps": ["python3", "python3-requests"]},
    "metasploit": {"version": "6.3.20-1", "size": "42 MB", "desc": "Penetration testing framework", "deps": ["ruby", "postgresql"]},
    "john": {"version": "1.9.0-1", "size": "2.1 MB", "desc": "Password cracker", "deps": ["libc6", "libssl3"]},
    "aircrack-ng": {"version": "1.7-1", "size": "1.5 MB", "desc": "WiFi security tools", "deps": ["libpcap0.8", "libsqlite3"]},
    "wireshark": {"version": "4.0.8-1", "size": "12 MB", "desc": "Network protocol analyzer", "deps": ["libwireshark13"]},
    "beef-xss": {"version": "0.5.4-1", "size": "8 MB", "desc": "Browser exploitation framework", "deps": ["ruby", "nodejs"]},
    "gcc": {"version": "12.2.0-14", "size": "18 MB", "desc": "GNU C compiler", "deps": ["binutils", "cpp"]},
    "make": {"version": "4.4.1-1", "size": "350 KB", "desc": "Build automation tool", "deps": []},
    "cmake": {"version": "3.25.1-1", "size": "6 MB", "desc": "Cross-platform build system", "deps": ["libarchive13"]},
    "wget": {"version": "1.21.3-1", "size": "450 KB", "desc": "Network downloader", "deps": ["libssl3"]},
    # Новые хакинговые инструменты
    "burpsuite": {"version": "2023.12.2-1", "size": "45 MB", "desc": "Web vulnerability scanner and proxy", "deps": ["default-jre"]},
    "zaproxy": {"version": "2.14.0-1", "size": "38 MB", "desc": "OWASP ZAP web app scanner", "deps": ["default-jre"]},
    "nikto": {"version": "2.5.0-1", "size": "1.2 MB", "desc": "Web server scanner", "deps": ["perl"]},
    "dirb": {"version": "2.22-1", "size": "200 KB", "desc": "Web directory brute forcer", "deps": []},
    "gobuster": {"version": "3.5.0-1", "size": "3.5 MB", "desc": "Directory/file busting tool", "deps": []},
    "wpscan": {"version": "3.8.25-1", "size": "4.2 MB", "desc": "WordPress security scanner", "deps": ["ruby"]},
    "whatweb": {"version": "0.5.5-1", "size": "250 KB", "desc": "Web technology identifier", "deps": ["ruby"]},
    "theharvester": {"version": "4.0.0-1", "size": "600 KB", "desc": "Email and subdomain gatherer", "deps": ["python3", "python3-requests"]},
    "recon-ng": {"version": "5.1.2-1", "size": "2.1 MB", "desc": "OSINT framework", "deps": ["python3", "python3-requests"]},
    "maltego": {"version": "4.3.0-1", "size": "28 MB", "desc": "Visual link analysis (emulated)", "deps": ["default-jre"]},
    "set": {"version": "8.0.3-1", "size": "5.8 MB", "desc": "Social-Engineer Toolkit", "deps": ["python3", "python3-requests"]},
    "bettercap": {"version": "2.31.0-1", "size": "9 MB", "desc": "MITM framework", "deps": ["libpcap0.8", "python3"]},
    "ettercap": {"version": "0.8.3.1-1", "size": "4.5 MB", "desc": "ARP spoofing and sniffing", "deps": ["libpcap0.8", "libnet1"]},
    "responder": {"version": "3.1.2-1", "size": "1.8 MB", "desc": "NTLM hash catcher", "deps": ["python3", "python3-requests"]},
    "bloodhound": {"version": "4.3.0-1", "size": "12 MB", "desc": "Active Directory analysis", "deps": ["neo4j"]},
    "mimikatz": {"version": "2.2.0-1", "size": "800 KB", "desc": "Windows credential extractor (emulated)", "deps": []},
    "hashcat": {"version": "6.2.6-1", "size": "6.5 MB", "desc": "Password cracker", "deps": ["libc6", "libssl3"]},
    "crunch": {"version": "3.6-1", "size": "180 KB", "desc": "Wordlist generator", "deps": []},
    "cupp": {"version": "3.0-1", "size": "120 KB", "desc": "Custom wordlist generator", "deps": ["python3"]},
    "seclists": {"version": "2023.1-1", "size": "150 MB", "desc": "Collection of wordlists", "deps": []},
    "rsactftool": {"version": "1.2-1", "size": "300 KB", "desc": "RSA CTF toolkit", "deps": ["python3", "python3-gmpy2"]},
    "fcrackzip": {"version": "1.0-1", "size": "60 KB", "desc": "ZIP password cracker", "deps": ["libc6"]},
    "pdfcrack": {"version": "0.19-1", "size": "70 KB", "desc": "PDF password cracker", "deps": ["libc6"]},
    "airgeddon": {"version": "11.21-1", "size": "2.5 MB", "desc": "Wi-Fi attack script", "deps": ["bash", "aircrack-ng"]},
    "fluxion": {"version": "6.0-1", "size": "1.8 MB", "desc": "WPA attack with fake AP", "deps": ["bash", "aircrack-ng"]},
    "kismet": {"version": "2023.03.R1-1", "size": "8 MB", "desc": "Wireless network detector", "deps": ["libpcap0.8", "libsqlite3"]},
    "dsniff": {"version": "2.4b1-1", "size": "450 KB", "desc": "Sniffing tools (arpspoof, dnsspoof, etc.)", "deps": ["libpcap0.8", "libnet1"]},
    "mitmproxy": {"version": "9.0.1-1", "size": "3 MB", "desc": "HTTP/HTTPS proxy", "deps": ["python3"]},
    "sslstrip": {"version": "0.9-1", "size": "100 KB", "desc": "SSL stripping attack", "deps": ["python3"]},
    "sslsplit": {"version": "0.5.5-1", "size": "150 KB", "desc": "SSL/TLS MITM tool", "deps": ["libssl3"]},
    "tcpdump": {"version": "4.99.3-1", "size": "400 KB", "desc": "Packet capture", "deps": ["libpcap0.8"]},
    "tshark": {"version": "4.0.8-1", "size": "1.2 MB", "desc": "Wireshark CLI", "deps": ["libwireshark13"]},
    "medusa": {"version": "2.2-1", "size": "200 KB", "desc": "Parallel network login brute forcer", "deps": ["libssl3"]},
    "ncrack": {"version": "0.7-1", "size": "350 KB", "desc": "High-speed network authentication cracker", "deps": ["libssl3"]},
    "patator": {"version": "1.0-1", "size": "180 KB", "desc": "Modular brute forcing tool", "deps": ["python3"]},
}

PIP_REMOTE_REPOSITORY = {
    "requests": {"version": "2.31.0", "deps": [], "desc": "HTTP for Humans"},
    "scapy": {"version": "2.5.0", "deps": [], "desc": "Packet manipulation"},
    "impacket": {"version": "0.11.0", "deps": ["pycryptodome"], "desc": "Network protocols"},
    "pycryptodome": {"version": "3.19.0", "deps": [], "desc": "Cryptographic tools"},
    "pwntools": {"version": "4.11.0", "deps": ["requests"], "desc": "CTF framework"},
    "beautifulsoup4": {"version": "4.12.0", "deps": [], "desc": "HTML/XML parser"},
    "selenium": {"version": "4.15.0", "deps": ["requests"], "desc": "Browser automation"},
    "scrapy": {"version": "2.11.0", "deps": ["requests"], "desc": "Web scraping framework"},
    "mitmproxy": {"version": "9.0.1", "deps": ["requests", "pyopenssl"], "desc": "MITM proxy"},
    "asyncio": {"version": "3.4.3", "deps": [], "desc": "Asynchronous I/O"},
    "sqlalchemy": {"version": "2.0.23", "deps": [], "desc": "SQL toolkit"},
    "cryptography": {"version": "41.0.7", "deps": [], "desc": "Cryptographic primitives"},
    "paramiko": {"version": "3.4.0", "deps": ["cryptography"], "desc": "SSH client"},
    "pyasn1": {"version": "0.5.0", "deps": [], "desc": "ASN.1 parser"},
    "twisted": {"version": "23.10.0", "deps": ["pyopenssl"], "desc": "Event-driven networking"},
    "pyopenssl": {"version": "23.3.0", "deps": ["cryptography"], "desc": "OpenSSL bindings"},
}

# =============================================================================
# ВИРТУАЛЬНАЯ ФАЙЛОВАЯ СИСТЕМА (VFS) – расширенная
# =============================================================================

class VirtualFileSystem:
    def __init__(self):
        self.root = {
            "bin": {"ls": "sys_bin", "cat": "sys_bin", "cd": "sys_bin", "pwd": "sys_bin", "echo": "sys_bin"},
            "usr": {"bin": {}, "share": {"wordlists": {"rockyou.txt": "admin\npassword\n123456\nqwerty\nletmein"}}},
            "etc": {"apt": {"sources.list": "deb http://http.kali.org/kali kali-rolling main contrib non-free"}, "passwd": "root:x:0:0:\nkali:x:1000:1000:"},
            "home": {
                "kali": {
                    "Desktop": {},
                    "Downloads": {},
                    "scripts": {
                        "test.py": "print('Hello from virtual Python inside Kali!')\nx = 10\ny = 20\nprint('Result:', x + y)"
                    }
                }
            },
            "var": {"log": {"apt": {"history.log": "Log started.\n"}}}
        }
        self.current_path = ["home", "kali"]

    def get_node(self, path_list):
        curr = self.root
        for step in path_list:
            if isinstance(curr, dict) and step in curr:
                curr = curr[step]
            else:
                return None
        return curr

    def change_dir(self, target):
        if not target or target == "~":
            self.current_path = ["home", "kali"]
            return True
        if target == "/":
            self.current_path = []
            return True

        parts = target.split("/")
        temp = list(self.current_path) if not target.startswith("/") else []
        for p in parts:
            if p == "" or p == ".": continue
            if p == "..":
                if temp: temp.pop()
            else:
                temp.append(p)
                if not isinstance(self.get_node(temp), dict):
                    return False
        self.current_path = temp
        return True

    def write_file(self, filename, content):
        node = self.get_node(self.current_path)
        if isinstance(node, dict):
            node[filename] = content
            return True
        return False

    def read_file(self, filename):
        node = self.get_node(self.current_path)
        if isinstance(node, dict) and filename in node and not isinstance(node[filename], dict):
            return node[filename]
        if "/" in filename:
            parts = filename.split("/")
            f_name = parts.pop()
            temp_path = list(self.current_path) if not filename.startswith("/") else []
            for p in parts:
                if p == "" or p == ".": continue
                if p == "..":
                    if temp_path: temp_path.pop()
                else: temp_path.append(p)
            target_node = self.get_node(temp_path)
            if isinstance(target_node, dict) and f_name in target_node:
                return target_node[f_name]
        return None

    def mkdir(self, dirname):
        node = self.get_node(self.current_path)
        if isinstance(node, dict):
            if dirname in node:
                return f"mkdir: cannot create directory '{dirname}': File exists"
            node[dirname] = {}
            return ""
        return "mkdir: cannot create directory: no such file or directory"

    def touch(self, filename):
        node = self.get_node(self.current_path)
        if isinstance(node, dict):
            if filename not in node:
                node[filename] = ""
            return ""
        return "touch: cannot touch file: no such file or directory"

    def rm(self, name, recursive=False):
        node = self.get_node(self.current_path)
        if isinstance(node, dict) and name in node:
            if isinstance(node[name], dict) and not recursive:
                return f"rm: cannot remove '{name}': Is a directory"
            del node[name]
            return ""
        return f"rm: cannot remove '{name}': No such file or directory"

    def cp(self, src, dst):
        node = self.get_node(self.current_path)
        if not isinstance(node, dict):
            return "cp: error"
        if src not in node:
            return f"cp: cannot stat '{src}': No such file or directory"
        if dst in node:
            return f"cp: will not overwrite just created '{dst}'"
        node[dst] = node[src]
        return ""

    def mv(self, src, dst):
        node = self.get_node(self.current_path)
        if not isinstance(node, dict):
            return "mv: error"
        if src not in node:
            return f"mv: cannot stat '{src}': No such file or directory"
        if dst in node:
            return f"mv: will not overwrite '{dst}'"
        node[dst] = node[src]
        del node[src]
        return ""

    def find(self, name, start_path=None):
        if start_path is None:
            start_path = self.current_path
        else:
            parts = start_path.split("/")
            start_path = parts if start_path.startswith("/") else self.current_path + parts
        result = []
        self._find_recursive(self.get_node(start_path), start_path, name, result)
        return result

    def _find_recursive(self, node, path_parts, name, result):
        if not isinstance(node, dict):
            return
        for key, val in node.items():
            full_path = "/" + "/".join(path_parts + [key])
            if key == name:
                result.append(full_path)
            if isinstance(val, dict):
                self._find_recursive(val, path_parts + [key], name, result)

    def grep(self, pattern, filename):
        content = self.read_file(filename)
        if content is None:
            return f"grep: {filename}: No such file or directory"
        lines = content.split("\n")
        matches = []
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                matches.append(f"{filename}:{i+1}:{line}")
        return "\n".join(matches) if matches else ""

    def tree(self, start_path=None):
        if start_path is None:
            start_path = self.current_path
        else:
            parts = start_path.split("/")
            start_path = parts if start_path.startswith("/") else self.current_path + parts
        node = self.get_node(start_path)
        if not isinstance(node, dict):
            return "tree: no such directory"
        out = [start_path[-1] if start_path else "/"]
        self._tree_recursive(node, start_path, out, "")
        return "\n".join(out)

    def _tree_recursive(self, node, path_parts, out, prefix):
        items = list(node.keys())
        for i, key in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            out.append(prefix + connector + key)
            if isinstance(node[key], dict):
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._tree_recursive(node[key], path_parts + [key], out, new_prefix)

    def df(self):
        total = 1024 * 1024
        used = 0
        def count_size(node):
            if not isinstance(node, dict):
                return len(node.encode('utf-8'))
            total_size = 0
            for v in node.values():
                total_size += count_size(v)
            return total_size
        used = count_size(self.root)
        used_kb = used // 1024
        total_kb = total // 1024
        available = total_kb - used_kb
        return f"Filesystem     1K-blocks      Used Available Use% Mounted on\n/dev/sda1         {total_kb:10} {used_kb:10} {available:10} {round(used_kb/total_kb*100)}% /"

    def free(self):
        total = 8192
        used = random.randint(3000, 6000)
        free = total - used
        shared = random.randint(200, 800)
        buff_cache = random.randint(500, 1500)
        available = free + buff_cache
        return f"              total        used        free      shared  buff/cache   available\nMem:          {total:10} {used:10} {free:10} {shared:10} {buff_cache:10} {available:10}\nSwap:         2048       0       2048"

    def git_clone(self, url, dest=None):
        if dest is None:
            repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
        else:
            repo_name = dest
        node = self.get_node(self.current_path)
        if not isinstance(node, dict):
            return "git clone: not in a directory"
        if repo_name in node:
            return f"fatal: destination path '{repo_name}' already exists"
        node[repo_name] = {}
        node[repo_name]['README.md'] = f"# {repo_name}\nCloned from {url}"
        node[repo_name]['.git'] = {}
        node[repo_name]['.git']['HEAD'] = 'ref: refs/heads/main'
        node[repo_name]['.git']['config'] = f'[remote "origin"]\n\turl = {url}\n'
        node[repo_name]['src'] = {}
        node[repo_name]['src']['main.py'] = 'print("Hello from cloned repo")'
        return f"Cloning into '{repo_name}'...\nremote: Enumerating objects: 10, done.\nremote: Counting objects: 100% (10/10), done.\nremote: Compressing objects: 100% (5/5), done.\nremote: Total 10 (delta 0), reused 0 (delta 0)\nReceiving objects: 100% (10/10), done.\n"

    def download_file(self, url, output=None):
        if output is None:
            output = url.split('/')[-1]
        node = self.get_node(self.current_path)
        if not isinstance(node, dict):
            return "wget: not in a directory"
        if output in node:
            return f"wget: '{output}' already exists"
        content = f"Downloaded from {url}\nTimestamp: {datetime.now()}\n"
        node[output] = content
        return f"Downloading {url}...\nSaving to: '{output}'\n100%[===================>] 1.2K  --.-KB/s    in 0.1s\n"

# =============================================================================
# СЕТЕВАЯ ПОДСИСТЕМА И ИНСТРУМЕНТЫ БЕЗОПАСНОСТИ
# =============================================================================

class NetworkInterface:
    def __init__(self, name, ip, mac, state="UP"):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.state = state

class NetworkAndSecurityEngine:
    def __init__(self):
        self.interfaces = {
            "lo": NetworkInterface("lo", "127.0.0.1", "00:00:00:00:00:00"),
            "eth0": NetworkInterface("eth0", "192.168.1.15", "00:0c:29:ed:14:a2")
        }
        self.dns = {"kali.org": "192.124.249.10", "google.com": "142.250.185.78"}
        self.hostname = "kali"

    def ip_cmd(self, args):
        if not args or args[0] not in ["addr", "a"]:
            return "Использование: ip addr"
        out = []
        for name, iface in self.interfaces.items():
            out.append(f"{name}: <BROADCAST,MULTICAST,{iface.state}> mtu 1500")
            out.append(f"    link/ether {iface.mac} brd ff:ff:ff:ff:ff:ff")
            if iface.state == "UP":
                out.append(f"    inet {iface.ip}/24 brd {iface.ip.rpartition('.')[0]}.255 scope global {name}")
        return "\n".join(out)

    def ping_cmd(self, args):
        if not args: return "ping: missing host operand"
        host = args[0]
        ip = self.dns.get(host, host)
        print(f"PING {host} ({ip}) 56(84) bytes of data.")
        for i in range(3):
            time.sleep(0.5)
            print(f"64 bytes from {ip}: icmp_seq={i+1} ttl=64 time={round(random.uniform(15, 40), 1)} ms")
        return f"--- {host} ping statistics --- \n3 packets transmitted, 3 received, 0% packet loss"

    def macchanger_cmd(self, args):
        if not args or args[0] != "-r":
            return "Использование: macchanger -r [interface]\nПример: macchanger -r eth0"
        iface = args[1] if len(args) > 1 else "eth0"
        if iface not in self.interfaces:
            return f"Interface {iface} not found."
        old_mac = self.interfaces[iface].mac
        new_mac = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
        self.interfaces[iface].mac = new_mac
        return f"Current MAC:   {old_mac}\nNew MAC:       {new_mac}\nAddress successfully changed."

    def nmap_cmd(self, args):
        if not args: return "Использование: nmap [target IP/Host]"
        target = args[-1]
        print(f"Starting Nmap 7.93 at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        time.sleep(1.5)
        print(f"Nmap scan report for {target}\nHost is up.\n\nPORT     STATE SERVICE")
        print("22/tcp   open  ssh\n80/tcp   open  http\n443/tcp  open  https")
        return "Nmap done: 1 IP address scanned in 1.52 seconds."

    def hydra_cmd(self, args, vfs):
        if len(args) < 4:
            return "Использование: hydra -l [user] -P [wordlist] [target] ssh\nПример: hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.1.15 ssh"
        try:
            wl_path = args[args.index("-P") + 1]
            user = args[args.index("-l") + 1]
        except (ValueError, IndexError):
            return "Ошибка синтаксиса. Проверьте флаги -l и -P."
        words = vfs.read_file(wl_path)
        if not words:
            return f"hydra: Ошибка: Словник {wl_path} не найден."
        passwords = words.strip().split("\n")
        print(f"Hydra v9.4 initialized. Attacking target {args[-2]}...")
        for p in passwords:
            time.sleep(0.3)
            print(f"[Attempt] User: {user} | Password: {p:<10} -> Access Denied")
            if p == "letmein":
                return f"\n[+][DATA] target un-locked!\nHost: {args[-2]} | User: {user} | Password: {p}"
        return "Attack finished: No credentials found."

    def sqlmap_cmd(self, args, vfs):
        if not args:
            return "sqlmap: missing URL or options\nПример: sqlmap -u http://example.com/vuln.php?id=1 --dbs"
        target = args[-1]
        print(f"        ___\n       _ H_\n ___ ___[(]_____ ___ ___  {datetime.now().strftime('%H:%M:%S')}\n|_ -| . [']     | .'| . |\n|___|_  [']_|_|_|__,|  _|\n      |_|V...       |_|   http://sqlmap.org")
        time.sleep(1)
        print(f"[*] starting @ {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(1.5)
        print(f"[*] testing connection to target...\n[+] target appears to be vulnerable to SQL injection\n")
        print("available databases [5]:\n[*] information_schema\n[*] mysql\n[*] performance_schema\n[*] sys\n[*] target_db")
        return "\n[+] SQL injection successful."

    def msfconsole_cmd(self, args):
        print("  =[ metasploit v6.3.20-dev                          ]")
        print("+ -- --=[ 2365 exploits - 1237 auxiliary - 412 post   ]")
        print("+ -- --=[ 862 payloads - 45 encoders - 11 nops        ]")
        print("+ -- --=[ 7 evasion modules                           ]")
        print("\n[*] Starting the Metasploit console...")
        time.sleep(1)
        print("msf6 > use exploit/multi/handler")
        print("msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp")
        print("msf6 exploit(multi/handler) > set LHOST 192.168.1.15")
        print("msf6 exploit(multi/handler) > set LPORT 4444")
        print("msf6 exploit(multi/handler) > exploit")
        print("[*] Started reverse TCP handler on 192.168.1.15:4444")
        return "[*] Meterpreter session 1 opened."

    # --- Эмуляции новых инструментов ---
    def burpsuite_cmd(self, args):
        print("Burp Suite Community Edition v2023.12.2")
        print("Proxy: http://127.0.0.1:8080")
        print("Spider started...")
        time.sleep(0.5)
        return "Burp is running. Intercept traffic with proxy."

    def zaproxy_cmd(self, args):
        print("OWASP ZAP v2.14.0 - Starting")
        print("Proxy: localhost:8080")
        print("Loading passive scan rules...")
        time.sleep(0.5)
        return "ZAP ready. Use 'zap-cli' for automation."

    def nikto_cmd(self, args):
        if not args:
            return "nikto -host <target>\nПример: nikto -host http://example.com"
        print("Nikto v2.5.0 - Web server scanner")
        time.sleep(1)
        print(f"Target: {args[0]}")
        print("Scanning...")
        time.sleep(1.5)
        print("+ /: Server: Apache/2.4.54\n+ /robots.txt: 7 entries\n+ /admin: directory found")
        return "Nikto scan completed."

    def dirb_cmd(self, args):
        if not args:
            return "dirb <URL> [wordlist]\nПример: dirb http://example.com"
        print(f"DIRB v2.22 - Directory brute forcer")
        print(f"Target: {args[0]}")
        print("Scanning...")
        time.sleep(1)
        print("+ http://example.com/admin (CODE:200)\n+ http://example.com/login (CODE:200)\n+ http://example.com/backup (CODE:301)")
        return "Scan finished."

    def gobuster_cmd(self, args):
        if not args:
            return "gobuster dir -u <URL> -w <wordlist>\nПример: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt"
        print("Gobuster v3.5.0 - Directory/file busting")
        print(f"Target: {args[0] if args else 'http://example.com'}")
        time.sleep(0.8)
        print("Found: /admin (Status: 200)\nFound: /wp-admin (Status: 301)")
        return "Gobuster finished."

    def wpscan_cmd(self, args):
        if not args:
            return "wpscan --url <URL>\nПример: wpscan --url http://wordpress-site.com"
        print("WPScan v3.8.25 - WordPress scanner")
        time.sleep(1)
        print(f"Target: {args[0]}")
        print("[+] WordPress version: 6.2\n[+] Theme: twenty-twenty-three\n[+] Vulnerable plugins found: 2")
        return "WPScan completed."

    def whatweb_cmd(self, args):
        if not args:
            return "whatweb <URL>\nПример: whatweb example.com"
        print(f"WhatWeb v0.5.5 - Web technology identifier")
        time.sleep(0.5)
        print(f"Target: {args[0]}")
        print("Apache 2.4.54, PHP 8.1, jQuery 3.6.0")
        return "Detection done."

    def theharvester_cmd(self, args):
        if not args:
            return "theharvester -d <domain> -b <source>\nПример: theharvester -d example.com -b google"
        print(f"theHarvester v4.0.0 - Email/Subdomain gatherer")
        time.sleep(0.5)
        print(f"Target: {args[0]}")
        print("Found emails: admin@example.com, support@example.com, sales@example.com")
        return "Harvesting finished."

    def recon_ng_cmd(self, args):
        print("Recon-ng v5.1.2 - OSINT framework")
        time.sleep(0.5)
        print("[recon-ng] > use recon/domains-hosts/brute_hosts")
        print("[recon-ng] > set SOURCE example.com")
        print("[recon-ng] > run\n[+] Found 5 hosts")
        return "Recon-ng finished."

    def maltego_cmd(self, args):
        return "Maltego GUI (emulated) - Launching visual analysis...\nRun Maltego with its own GUI."

    def set_cmd(self, args):
        print("Social-Engineer Toolkit v8.0.3")
        print("1) Spear-Phishing Attack\n2) Website Attack\n3) Infectious Media Generator")
        time.sleep(0.5)
        return "SET main menu displayed."

    def bettercap_cmd(self, args):
        print("BetterCap v2.31.0 - MITM framework")
        time.sleep(0.5)
        print("Starting bettercap...")
        print("Gateway: 192.168.1.1")
        print("Targets: 192.168.1.10, 192.168.1.11")
        return "BetterCap running. Use 'net.sniff on' to capture."

    def ettercap_cmd(self, args):
        print("Ettercap v0.8.3.1 - ARP spoofing")
        time.sleep(0.5)
        print("ARP poisoning started on interface eth0")
        print("Sniffing HTTP traffic...")
        return "Ettercap running."

    def responder_cmd(self, args):
        print("Responder v3.1.2 - NTLM hash catcher")
        time.sleep(0.5)
        print("Listening for NTLM hashes on port 445, 389, 80...")
        print("Waiting for connections...")
        return "Responder active."

    def bloodhound_cmd(self, args):
        print("BloodHound v4.3.0 - Active Directory analysis")
        time.sleep(0.5)
        print("Collecting AD data with SharpHound...")
        print("Uploading to Neo4j...")
        return "BloodHound ready. Visit http://localhost:7474"

    def mimikatz_cmd(self, args):
        print("mimikatz v2.2.0 (emulated)")
        time.sleep(0.5)
        print("mimikatz # sekurlsa::logonpasswords")
        print("Username: admin\nDomain: DOMAIN\nPassword: P@ssw0rd")
        return "Credentials extracted."

    def hashcat_cmd(self, args):
        if len(args) < 2:
            return "hashcat -m <mode> <hashfile> <wordlist>\nПример: hashcat -m 0 hash.txt wordlist.txt"
        print(f"hashcat v6.2.6 - Password cracker")
        time.sleep(0.5)
        print(f"Mode: {args[0]}, Hash: {args[1]}")
        time.sleep(1)
        print("Session started...")
        print("Found password: 'letmein'")
        return "Hashcat finished."

    def crunch_cmd(self, args):
        if not args:
            return "crunch <min> <max> [charset] -o <output>\nПример: crunch 6 8 0123456789 -o wordlist.txt"
        print(f"Crunch v3.6 - Wordlist generator")
        time.sleep(0.5)
        print(f"Generating {args[0]}-{args[1]} length words...")
        print(f"Wordlist saved to {args[-1] if '-o' in args else 'wordlist.txt'}")
        return "Crunch done."

    def cupp_cmd(self, args):
        print("CUPP v3.0 - Custom wordlist generator")
        time.sleep(0.5)
        print("Interactive mode: asking user details...")
        print("Wordlist generated: passwords.txt")
        return "CUPP finished."

    def seclists_cmd(self, args):
        return "SecLists installed. Available wordlists in /usr/share/seclists"

    def rsactftool_cmd(self, args):
        print("RsaCtfTool v1.2 - RSA CTF toolkit")
        time.sleep(0.5)
        print("Trying common attacks...")
        print("Found private key!")
        return "Key recovered."

    def fcrackzip_cmd(self, args):
        if not args:
            return "fcrackzip -b -v -u <zipfile>\nПример: fcrackzip -b -v -u secret.zip"
        print(f"fcrackzip v1.0 - ZIP password cracker")
        time.sleep(0.5)
        print(f"Trying passwords on {args[0]}")
        print("Found password: '1234'")
        return "Zip cracked."

    def pdfcrack_cmd(self, args):
        if not args:
            return "pdfcrack -f <pdf>\nПример: pdfcrack -f document.pdf"
        print(f"pdfcrack v0.19 - PDF password cracker")
        time.sleep(0.5)
        print(f"Cracking {args[0]}...")
        print("Password found: 'letmein'")
        return "PDF cracked."

    def airgeddon_cmd(self, args):
        print("Airgeddon v11.21 - Wi-Fi attack script")
        time.sleep(0.5)
        print("Interface selected: wlan0")
        print("1) Handshake capture\n2) Evil Twin\n3) WPS attack")
        return "Airgeddon menu ready."

    def fluxion_cmd(self, args):
        print("Fluxion v6.0 - WPA attack with fake AP")
        time.sleep(0.5)
        print("Selecting target AP...")
        print("Fake AP created: 'FreeWiFi'")
        print("Waiting for handshake...")
        return "Fluxion running."

    def kismet_cmd(self, args):
        print("Kismet v2023.03.R1 - Wireless network detector")
        time.sleep(0.5)
        print("Scanning for networks...")
        print("Found: Net1 (BSSID: AA:BB:CC:DD:EE:FF, ESSID: 'KaliNet')")
        return "Kismet scan completed."

    def dsniff_cmd(self, args):
        if not args:
            return "dsniff: use arpspoof, dnsspoof, etc.\nПример: arpspoof -t 192.168.1.10 192.168.1.1"
        print(f"dsniff - Sniffing tools")
        time.sleep(0.5)
        print("Executing ARP spoofing...")
        print("Capturing traffic...")
        return "Sniffing started."

    def mitmproxy_cmd(self, args):
        print("mitmproxy v9.0.1 - HTTP/HTTPS proxy")
        time.sleep(0.5)
        print("Proxy running on port 8080")
        return "mitmproxy console. Use 'mitmweb' for GUI."

    def sslstrip_cmd(self, args):
        print("sslstrip v0.9 - SSL stripping")
        time.sleep(0.5)
        print("Listening on port 10000")
        print("Stripping SSL from traffic...")
        return "sslstrip active."

    def sslsplit_cmd(self, args):
        print("sslsplit v0.5.5 - SSL/TLS MITM")
        time.sleep(0.5)
        print("Proxy on port 8443")
        return "sslsplit running."

    def tcpdump_cmd(self, args):
        print("tcpdump v4.99.3 - Packet capture")
        time.sleep(0.5)
        print("Capturing on interface eth0...")
        print("3 packets captured, 3 packets received")
        return "tcpdump done."

    def tshark_cmd(self, args):
        print("tshark v4.0.8 - Wireshark CLI")
        time.sleep(0.5)
        print("Capturing on eth0...")
        print("Packet 1: TCP 192.168.1.10:80 -> 192.168.1.15:443")
        return "tshark finished."

    def medusa_cmd(self, args):
        if len(args) < 4:
            return "medusa -h <host> -u <user> -P <passlist> -M <module>\nПример: medusa -h 192.168.1.15 -u root -P passlist.txt -M ssh"
        print("Medusa v2.2 - Parallel brute forcer")
        time.sleep(0.5)
        print(f"Target: {args[0]}, User: {args[2]}")
        print("Brute forcing...")
        print("Password found: 'password123'")
        return "Medusa attack complete."

    def ncrack_cmd(self, args):
        if len(args) < 4:
            return "ncrack -p <port> -u <user> -P <passlist> <host>\nПример: ncrack -p ssh -u root -P passlist.txt 192.168.1.15"
        print("Ncrack v0.7 - High-speed cracker")
        time.sleep(0.5)
        print("Cracking SSH on target...")
        print("Credentials found: root:letmein")
        return "Ncrack finished."

    def patator_cmd(self, args):
        if len(args) < 3:
            return "patator <module> <params>\nПример: patator ssh_login host=192.168.1.15 user=root password=FILE0 0=passlist.txt"
        print("Patator v1.0 - Modular brute forcer")
        time.sleep(0.5)
        print("Starting module...")
        print("Trying passwords...")
        print("Success: root:toor")
        return "Patator done."

# =============================================================================
# СИСТЕМА КОНТРОЛЯ ВЕРСИЙ (GIT ENGINE)
# =============================================================================

class GitEngine:
    def __init__(self):
        self.repo_active = False
        self.staged = []
        self.history = []

    def execute(self, args, current_files):
        if not args: return "git: missing command. Commands: init, add, commit, log, clone"
        action = args[0]
        if action == "clone":
            return "git clone: use as standalone command"
        if action == "init":
            self.repo_active = True
            return "Initialized empty Git repository in current directory."
        if not self.repo_active:
            return "fatal: not a git repository"
        if action == "add":
            files = args[1:]
            if not files: return "Nothing specified, nothing added."
            if files[0] == ".":
                self.staged.extend([f for f in current_files if not f.startswith(".")])
            else:
                for f in files:
                    if f in current_files: self.staged.append(f)
                    else: return f"fatal: pathspec '{f}' did not match any files"
            return f"Staged {len(self.staged)} files."
        elif action == "commit":
            if "-m" not in args or len(args) < 3: return "error: switch 'm' requires a value"
            if not self.staged: return "nothing to commit, working tree clean"
            msg = " ".join(args[args.index("-m")+1:]).strip('"')
            c_hash = hashlib.md5(str(time.time()).encode()).hexdigest()[:7]
            self.history.append({"hash": c_hash, "msg": msg, "date": datetime.now().strftime("%c"), "files": list(self.staged)})
            self.staged.clear()
            return f"[main {c_hash}] {msg}\n Files committed into local tree."
        elif action == "log":
            if not self.history: return "No commits yet."
            return "\n".join([f"\033[1;33mcommit {c['hash']}\033[0m\nDate: {c['date']}\n\n    {c['msg']}\n" for c in reversed(self.history)])
        return f"git: '{action}' is not a valid command."

# =============================================================================
# МЕНЕДЖЕРЫ ПАКЕТОВ (APT & PIP) – с зависимостями и виртуальными окружениями
# =============================================================================

class PackageManagerSystem:
    def __init__(self):
        self.installed_apt = ["ls", "cat", "cd", "pwd", "echo", "apt", "pip"]
        self.installed_pip = {"pip": "23.0.1"}
        self.apt_updated = False
        self.venvs = {}
        self.current_venv = None

    def apt_execute(self, args):
        if not args: return "Advanced Package Tool. Commands: update, install [pkg], remove [pkg]"
        action = args[0]
        if action == "update":
            print("Get:1 http://http.kali.org/kali kali-rolling InRelease [41.2 kB]")
            time.sleep(0.5)
            print("Get:2 http://http.kali.org/kali kali-rolling/main amd64 Packages [19.5 MB]")
            time.sleep(1.0)
            self.apt_updated = True
            return "Reading package lists... Done.\nBuilding dependency tree... Done."
        if action == "install":
            if len(args) < 2: return "E: You must specify at least one package to install"
            pkg = args[1]
            if pkg in self.installed_apt:
                return f"{pkg} is already the newest version."
            if pkg in APT_REMOTE_REPOSITORY:
                deps = APT_REMOTE_REPOSITORY[pkg].get("deps", [])
                for dep in deps:
                    if dep not in self.installed_apt:
                        print(f"Installing dependency: {dep}")
                        self.apt_execute(["install", dep])
                print(f"Reading package lists... Done\nBuilding dependency tree... Done")
                print(f"The following NEW packages will be installed:\n  {pkg}")
                print(f"Need to get {APT_REMOTE_REPOSITORY[pkg]['size']} of archives.")
                time.sleep(1.2)
                print(f"Unpacking {pkg} ({APT_REMOTE_REPOSITORY[pkg]['version']})...")
                time.sleep(0.5)
                print(f"Setting up {pkg}...")
                self.installed_apt.append(pkg)
                return "Processing triggers for man-db (2.11.2-1)... Done."
            else:
                return f"E: Unable to locate package {pkg}"
        elif action == "remove":
            if len(args) < 2: return "E: You must specify at least one package to remove"
            pkg = args[1]
            if pkg in self.installed_apt:
                self.installed_apt.remove(pkg)
                return f"Removing {pkg}... Done."
            return f"Package {pkg} is not installed."
        return f"Unknown apt command: {action}"

    def pip_execute(self, args):
        if "python3" not in self.installed_apt:
            return "bash: pip: command not found (Установите python3 через apt install)"
        if not args: return "Pip Core Interface. Commands: list, install [package], install git+..., venv [name], activate [name], deactivate"
        action = args[0]

        if action == "list":
            return "\n".join([f"{k:<15} {v}" for k, v in self.installed_pip.items()])

        if action == "install":
            if len(args) < 2: return "error: Minimum arguments not reached."
            target = args[1]
            if target.startswith("git+"):
                url = target[4:]
                print(f"Collecting {url}...\n  Cloning repository...")
                time.sleep(1.5)
                pkg_name = url.rstrip('/').split('/')[-1].replace('.git', '')
                version = "1.0.0"
                self.installed_pip[pkg_name] = version
                return f"Successfully installed {pkg_name} from git"
            else:
                pkg = target.lower()
                if pkg in self.installed_pip:
                    return f"Requirement already satisfied: {pkg}"
                if pkg in PIP_REMOTE_REPOSITORY:
                    print(f"Collecting {pkg}...\n  Downloading {pkg}-{PIP_REMOTE_REPOSITORY[pkg]['version']}-py3-none-any.whl")
                    time.sleep(1.0)
                    self.installed_pip[pkg] = PIP_REMOTE_REPOSITORY[pkg]['version']
                    return f"Successfully installed {pkg}"
                return f"ERROR: Could not find a version that satisfies the requirement {pkg}"

        if action == "venv":
            if len(args) < 2: return "Usage: pip venv <name>"
            name = args[1]
            if name in self.venvs:
                return f"Virtual environment '{name}' already exists."
            self.venvs[name] = []
            return f"Created virtual environment '{name}'."

        if action == "activate":
            if len(args) < 2: return "Usage: pip activate <name>"
            name = args[1]
            if name not in self.venvs:
                return f"Virtual environment '{name}' does not exist."
            self.current_venv = name
            return f"Activated virtual environment '{name}'. Now all pip install will use this environment."

        if action == "deactivate":
            if self.current_venv is None:
                return "No virtual environment activated."
            self.current_venv = None
            return "Deactivated virtual environment."

        if self.current_venv and action == "install":
            if len(args) < 2: return "error: Minimum arguments not reached."
            pkg = args[1]
            if pkg in self.venvs[self.current_venv]:
                return f"{pkg} already installed in this environment."
            print(f"Installing {pkg} into environment '{self.current_venv}'...")
            time.sleep(0.5)
            self.venvs[self.current_venv].append(pkg)
            return f"Successfully installed {pkg} in '{self.current_venv}'"

        return f"Unknown pip command."

    def run_python_runtime(self, filename, vfs):
        if "python3" not in self.installed_apt:
            return "bash: python3: command not found (Установите python3 с помощью apt install)"
        code = vfs.read_file(filename)
        if not code:
            return f"python3: can't open file '{filename}': [Errno 2] No such file or directory"
        print(f"--- [Executing {filename} via Python Virtual Runtime] ---")
        lines = code.split("\n")
        local_vars = {}
        for index, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line.startswith("print("):
                content_match = re.match(r"print\((.*)\)", line)
                if content_match:
                    args_str = content_match.group(1)
                    parts = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", args_str)
                    out_parts = []
                    for p in parts:
                        p = p.strip()
                        if (p.startswith("'") and p.endswith("'")) or (p.startswith('"') and p.endswith('"')):
                            out_parts.append(p[1:-1])
                        elif p in local_vars:
                            out_parts.append(str(local_vars[p]))
                        else:
                            try:
                                out_parts.append(str(eval(p, {}, local_vars)))
                            except:
                                out_parts.append(p)
                    print(" ".join(out_parts))
            elif "=" in line:
                var_name, expr = line.split("=", 1)
                var_name = var_name.strip()
                expr = expr.strip()
                try:
                    local_vars[var_name] = eval(expr, {}, local_vars)
                except Exception as e:
                    print(f"Python Runtime Error [Line {index+1}]: Сбой парсинга выражения '{expr}'")
        return "--- [Process completed with exit code 0] ---"

# =============================================================================
# АВТОДОПОЛНЕНИЕ (readline)
# =============================================================================

class Completer:
    def __init__(self, commands, vfs):
        self.commands = commands
        self.vfs = vfs

    def complete(self, text, state):
        line = readline.get_line_buffer()
        words = line.split()
        if not words:
            options = [c for c in self.commands if c.startswith(text)]
        elif len(words) == 1 and text == words[-1]:
            options = [c for c in self.commands if c.startswith(text)]
        else:
            prefix = words[-1] if text else ""
            node = self.vfs.get_node(self.vfs.current_path)
            if isinstance(node, dict):
                options = [k for k in node.keys() if k.startswith(prefix)]
            else:
                options = []
        try:
            return options[state]
        except IndexError:
            return None

# =============================================================================
# ЦЕНТРАЛЬНАЯ ОПЕРАЦИОННАЯ СИСТЕМА (MAIN INTERACTIVE SHELL CONTEXT)
# =============================================================================

class KaliOperatingSystem:
    def __init__(self):
        self.vfs = VirtualFileSystem()
        self.net_sec = NetworkAndSecurityEngine()
        self.git = GitEngine()
        self.pkg = PackageManagerSystem()
        self.running = True
        self.history = []
        self.commands = [
            "help", "clear", "exit", "ls", "cd", "pwd", "cat", "echo",
            "apt", "pip", "python3", "ip", "ping", "macchanger", "nmap", "hydra",
            "git", "nano", "touch", "mkdir", "rm", "cp", "mv", "find", "grep",
            "htop", "hostname", "tree", "history", "df", "free",
            "sqlmap", "msfconsole", "wget", "curl", "gcc", "make", "cmake", "sudo",
            "burpsuite", "zaproxy", "nikto", "dirb", "gobuster", "wpscan", "whatweb",
            "theharvester", "recon-ng", "maltego", "set", "bettercap", "ettercap",
            "responder", "bloodhound", "mimikatz", "hashcat", "crunch", "cupp",
            "seclists", "rsactftool", "fcrackzip", "pdfcrack", "airgeddon", "fluxion",
            "kismet", "dsniff", "mitmproxy", "sslstrip", "sslsplit", "tcpdump",
            "tshark", "medusa", "ncrack", "patator"
        ]
        completer = Completer(self.commands, self.vfs)
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")

    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[1;31m")
        print(r"  _  __     _ _   _     _                     ____   ____  ")
        print(r" | |/ /__ _| (_) | |   (_)_ __  _   ___  __  / ___| / ___| ")
        print(r" | ' // _` | | | | |   | | '_ \| | | \ \/ /  \___ \| |     ")
        print(r" | . \ (_| | | | | |___| | | | | |_| |>  <    ___) | |___  ")
        print(r" |_|\_\__,_|_|_| |_____|_|_| |_|\__,_/_/\_\  |____/ \____| ")
        print("\033[0m")
        print(f" Kali Linux OS Core Simulation Ecosystem [Kernel: 6.1.0-kali7-amd64] (v6.0)")
        print(f" Текущее время системы: {datetime.now().strftime('%A, %B %d, %Y')}")
        print(f" ПРЕДУПРЕЖДЕНИЕ: Инструменты хакинга требуют установки через apt.")
        print(f" Введите '\033[1;32mhelp\033[0m' для получения списка команд.\n")

    def show_matrix_help(self):
        print("""
 Доступные команды в сборке v6.0:
 -----------------------------------------------------------------
 [Система и ФС]       ls, cd [dir], pwd, cat [file], clear, exit
 [Работа с файлами]   echo, touch, mkdir, rm, cp, mv, find, grep
 [Текстовый редактор] nano [файл]
 [Менеджер APT]       apt update, apt install [имя_пакета]
 [Менеджер PIP]       pip list, pip install [pkg], pip install git+...
                      pip venv [name], pip activate [name], pip deactivate
 [Интерпретатор]      python3 [файл.py]
 [Сеть и Линки]       ip addr, ping [host], hostname
 [Инструменты Kali]   macchanger -r, nmap [IP], hydra, sqlmap, msfconsole
 [Загрузка файлов]    wget [URL], curl [URL]
 [Компиляция]         gcc [файл], make, cmake
 [Мониторинг]         htop, df, free
 [Дерево и история]   tree [dir], history
 [Локальный Git]      git init, git add ., git commit -m, git log, git clone [URL]
 [Привилегии]         sudo [команда] (эмуляция)
 -----------------------------------------------------------------
 Дополнительные инструменты хакинга (требуют apt install):
 burpsuite, zaproxy, nikto, dirb, gobuster, wpscan, whatweb,
 theharvester, recon-ng, maltego, set, bettercap, ettercap,
 responder, bloodhound, mimikatz, hashcat, crunch, cupp,
 seclists, rsactftool, fcrackzip, pdfcrack, airgeddon, fluxion,
 kismet, dsniff, mitmproxy, sslstrip, sslsplit, tcpdump,
 tshark, medusa, ncrack, patator
 -----------------------------------------------------------------
        """)

    def enforce_execution_security(self, command_name):
        # Проверяем, установлен ли пакет, кроме команд, которые не требуют apt (например, sudo, ls и т.д.)
        if command_name in self.commands and command_name not in ["help", "clear", "exit", "ls", "cd", "pwd", "cat", "echo",
                                                                   "touch", "mkdir", "rm", "cp", "mv", "find", "grep",
                                                                   "sudo", "history", "df", "free", "hostname", "git"]:
            if command_name not in self.pkg.installed_apt and command_name != "msfconsole":  # msfconsole симулируется
                print(f"bash: {command_name}: command not found. Попробуйте выполнить: apt install {command_name}")
                return False
        return True

    def process_input(self):
        curr_path_string = "/" + "/".join(self.vfs.current_path)
        prompt = f"\033[1;31m┌──(kali💀kali)-[{curr_path_string}]\n└─$ \033[0m"
        try:
            raw_line = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nВведите 'exit' для завершения сессии.")
            return
        if not raw_line.strip(): return
        self.history.append(raw_line)
        tokens = raw_line.strip().split()
        cmd = tokens[0]
        args = tokens[1:]

        if cmd == "sudo":
            if not args:
                print("sudo: no command given")
                return
            cmd = args[0]
            args = args[1:]
            self._execute_command(cmd, args, sudo=True)
            return

        self._execute_command(cmd, args, sudo=False)

    def _execute_command(self, cmd, args, sudo=False):
        if not self.enforce_execution_security(cmd):
            return

        # Обработка встроенных команд
        if cmd == "help":
            self.show_matrix_help()
        elif cmd == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd == "exit":
            print("\nShutting down virtualization cores safely... Goodbye!")
            self.running = False
        elif cmd == "ls":
            node = self.vfs.get_node(self.vfs.current_path)
            if isinstance(node, dict):
                for k, v in node.items():
                    if isinstance(v, dict): print(f"\033[1;34m{k}/\033[0m  ", end="")
                    else: print(f"{k}  ", end="")
                print()
        elif cmd == "cd":
            target = args[0] if args else "~"
            if not self.vfs.change_dir(target):
                print(f"bash: cd: {target}: No such file or directory")
        elif cmd == "pwd":
            print("/" + "/".join(self.vfs.current_path))
        elif cmd == "cat":
            if not args:
                print("cat: missing file operand")
                return
            res = self.vfs.read_file(args[0])
            if res is not None: print(res)
            else: print(f"cat: {args[0]}: No such file or directory")
        elif cmd == "echo":
            line_str = " ".join(args)
            if " > " in line_str:
                content, filename = line_str.split(" > ", 1)
                content = content.strip('"').strip("'")
                self.vfs.write_file(filename.strip(), content)
            else:
                print(line_str.strip('"').strip("'"))
        elif cmd == "touch":
            if not args:
                print("touch: missing file operand")
            else:
                for f in args:
                    res = self.vfs.touch(f)
                    if res: print(res)
        elif cmd == "mkdir":
            if not args:
                print("mkdir: missing operand")
            else:
                for d in args:
                    res = self.vfs.mkdir(d)
                    if res: print(res)
        elif cmd == "rm":
            if not args:
                print("rm: missing operand")
                return
            recursive = False
            if args[0] == "-r":
                recursive = True
                args = args[1:]
                if not args:
                    print("rm: missing operand")
                    return
            for item in args:
                res = self.vfs.rm(item, recursive)
                if res: print(res)
        elif cmd == "cp":
            if len(args) < 2:
                print("cp: missing file operand")
            else:
                src, dst = args[0], args[1]
                res = self.vfs.cp(src, dst)
                if res: print(res)
        elif cmd == "mv":
            if len(args) < 2:
                print("mv: missing file operand")
            else:
                src, dst = args[0], args[1]
                res = self.vfs.mv(src, dst)
                if res: print(res)
        elif cmd == "find":
            if not args:
                print("find: missing operand")
            else:
                name = args[0]
                results = self.vfs.find(name)
                if results:
                    print("\n".join(results))
                else:
                    print(f"find: '{name}' not found")
        elif cmd == "grep":
            if len(args) < 2:
                print("grep: missing pattern or file")
            else:
                pattern = args[0]
                filename = args[1]
                res = self.vfs.grep(pattern, filename)
                if res:
                    print(res)
                else:
                    print(f"grep: no matches in {filename}")
        elif cmd == "htop":
            if "htop" not in self.pkg.installed_apt:
                print("htop not installed. Run 'apt install htop'")
                return
            print("\033[2J\033[H", end="")
            print("  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND")
            for i in range(20):
                pid = random.randint(1000, 9999)
                user = random.choice(["root", "kali", "www-data"])
                mem = random.randint(1000, 50000)
                cpu = random.randint(0, 100)
                cmd2 = random.choice(["python3", "nano", "bash", "sshd", "nginx", "systemd"])
                print(f"{pid:6} {user:8} {random.randint(10,30):3} {random.randint(0,10):3} {mem:8} {mem:8} {random.randint(1000,5000):6} S {cpu:5} {random.randint(0,100):5} {random.random():6.2f} {cmd2}")
            time.sleep(3)
            print("\nPress any key to exit htop...")
            input()
        elif cmd == "hostname":
            print(self.net_sec.hostname)
        elif cmd == "tree":
            if "tree" not in self.pkg.installed_apt:
                print("tree not installed. Run 'apt install tree'")
                return
            if args:
                res = self.vfs.tree(args[0])
            else:
                res = self.vfs.tree()
            print(res)
        elif cmd == "history":
            for i, line in enumerate(self.history, 1):
                print(f"{i:4}  {line}")
        elif cmd == "df":
            print(self.vfs.df())
        elif cmd == "free":
            print(self.vfs.free())
        elif cmd == "nano":
            if "nano" not in self.pkg.installed_apt:
                print("nano not installed. Run 'apt install nano'")
                return
            if not args:
                print("nano: missing file operand")
                return
            filename = args[0]
            existing = self.vfs.read_file(filename)
            if existing is None:
                existing = ""
            print(f"--- nano: editing {filename} (press Ctrl+X to save and exit) ---")
            print("Enter new content (finish with empty line):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            content = "\n".join(lines)
            self.vfs.write_file(filename, content)
            print(f"Saved to {filename}")
        elif cmd == "wget" or cmd == "curl":
            if cmd == "wget" and "wget" not in self.pkg.installed_apt:
                print("wget not installed. Run 'apt install wget'")
                return
            if not args:
                print(f"{cmd}: missing URL")
                return
            url = args[0]
            output = None
            if "-O" in args:
                idx = args.index("-O")
                if idx+1 < len(args):
                    output = args[idx+1]
            res = self.vfs.download_file(url, output)
            print(res)
        elif cmd == "gcc":
            if "gcc" not in self.pkg.installed_apt:
                print("gcc not installed. Run 'apt install gcc'")
                return
            if not args:
                print("gcc: no input files")
                return
            source = args[0]
            print(f"gcc: {source} -> a.out")
            self.vfs.write_file("a.out", "ELF binary (simulated)")
            print("Compilation successful.")
        elif cmd == "make":
            if "make" not in self.pkg.installed_apt:
                print("make not installed. Run 'apt install make'")
                return
            print("make: Nothing to be done for 'all'.")
        elif cmd == "cmake":
            if "cmake" not in self.pkg.installed_apt:
                print("cmake not installed. Run 'apt install cmake'")
                return
            print("-- The C compiler identification is GNU 12.2.0")
            print("-- Configuring done")
            print("-- Generating done")
            print("-- Build files have been written to: ...")
        elif cmd == "sqlmap":
            if "sqlmap" not in self.pkg.installed_apt:
                print("sqlmap not installed. Run 'apt install sqlmap'")
                return
            print(self.net_sec.sqlmap_cmd(args, self.vfs))
        elif cmd == "msfconsole":
            if "metasploit" not in self.pkg.installed_apt:
                print("metasploit not installed. Run 'apt install metasploit'")
                return
            print(self.net_sec.msfconsole_cmd(args))
        elif cmd == "git":
            if args and args[0] == "clone":
                if len(args) < 2:
                    print("git clone: missing URL")
                    return
                url = args[1]
                dest = args[2] if len(args) > 2 else None
                print(self.vfs.git_clone(url, dest))
                return
            else:
                files = list(self.vfs.get_node(self.vfs.current_path).keys())
                print(self.git.execute(args, files))
        # Новые инструменты
        elif cmd == "burpsuite":
            if "burpsuite" not in self.pkg.installed_apt:
                print("burpsuite not installed. Run 'apt install burpsuite'")
                return
            print(self.net_sec.burpsuite_cmd(args))
        elif cmd == "zaproxy":
            if "zaproxy" not in self.pkg.installed_apt:
                print("zaproxy not installed. Run 'apt install zaproxy'")
                return
            print(self.net_sec.zaproxy_cmd(args))
        elif cmd == "nikto":
            if "nikto" not in self.pkg.installed_apt:
                print("nikto not installed. Run 'apt install nikto'")
                return
            print(self.net_sec.nikto_cmd(args))
        elif cmd == "dirb":
            if "dirb" not in self.pkg.installed_apt:
                print("dirb not installed. Run 'apt install dirb'")
                return
            print(self.net_sec.dirb_cmd(args))
        elif cmd == "gobuster":
            if "gobuster" not in self.pkg.installed_apt:
                print("gobuster not installed. Run 'apt install gobuster'")
                return
            print(self.net_sec.gobuster_cmd(args))
        elif cmd == "wpscan":
            if "wpscan" not in self.pkg.installed_apt:
                print("wpscan not installed. Run 'apt install wpscan'")
                return
            print(self.net_sec.wpscan_cmd(args))
        elif cmd == "whatweb":
            if "whatweb" not in self.pkg.installed_apt:
                print("whatweb not installed. Run 'apt install whatweb'")
                return
            print(self.net_sec.whatweb_cmd(args))
        elif cmd == "theharvester":
            if "theharvester" not in self.pkg.installed_apt:
                print("theharvester not installed. Run 'apt install theharvester'")
                return
            print(self.net_sec.theharvester_cmd(args))
        elif cmd == "recon-ng":
            if "recon-ng" not in self.pkg.installed_apt:
                print("recon-ng not installed. Run 'apt install recon-ng'")
                return
            print(self.net_sec.recon_ng_cmd(args))
        elif cmd == "maltego":
            if "maltego" not in self.pkg.installed_apt:
                print("maltego not installed. Run 'apt install maltego'")
                return
            print(self.net_sec.maltego_cmd(args))
        elif cmd == "set":
            if "set" not in self.pkg.installed_apt:
                print("SET not installed. Run 'apt install set'")
                return
            print(self.net_sec.set_cmd(args))
        elif cmd == "bettercap":
            if "bettercap" not in self.pkg.installed_apt:
                print("bettercap not installed. Run 'apt install bettercap'")
                return
            print(self.net_sec.bettercap_cmd(args))
        elif cmd == "ettercap":
            if "ettercap" not in self.pkg.installed_apt:
                print("ettercap not installed. Run 'apt install ettercap'")
                return
            print(self.net_sec.ettercap_cmd(args))
        elif cmd == "responder":
            if "responder" not in self.pkg.installed_apt:
                print("responder not installed. Run 'apt install responder'")
                return
            print(self.net_sec.responder_cmd(args))
        elif cmd == "bloodhound":
            if "bloodhound" not in self.pkg.installed_apt:
                print("bloodhound not installed. Run 'apt install bloodhound'")
                return
            print(self.net_sec.bloodhound_cmd(args))
        elif cmd == "mimikatz":
            if "mimikatz" not in self.pkg.installed_apt:
                print("mimikatz not installed. Run 'apt install mimikatz'")
                return
            print(self.net_sec.mimikatz_cmd(args))
        elif cmd == "hashcat":
            if "hashcat" not in self.pkg.installed_apt:
                print("hashcat not installed. Run 'apt install hashcat'")
                return
            print(self.net_sec.hashcat_cmd(args))
        elif cmd == "crunch":
            if "crunch" not in self.pkg.installed_apt:
                print("crunch not installed. Run 'apt install crunch'")
                return
            print(self.net_sec.crunch_cmd(args))
        elif cmd == "cupp":
            if "cupp" not in self.pkg.installed_apt:
                print("cupp not installed. Run 'apt install cupp'")
                return
            print(self.net_sec.cupp_cmd(args))
        elif cmd == "seclists":
            if "seclists" not in self.pkg.installed_apt:
                print("seclists not installed. Run 'apt install seclists'")
                return
            print(self.net_sec.seclists_cmd(args))
        elif cmd == "rsactftool":
            if "rsactftool" not in self.pkg.installed_apt:
                print("rsactftool not installed. Run 'apt install rsactftool'")
                return
            print(self.net_sec.rsactftool_cmd(args))
        elif cmd == "fcrackzip":
            if "fcrackzip" not in self.pkg.installed_apt:
                print("fcrackzip not installed. Run 'apt install fcrackzip'")
                return
            print(self.net_sec.fcrackzip_cmd(args))
        elif cmd == "pdfcrack":
            if "pdfcrack" not in self.pkg.installed_apt:
                print("pdfcrack not installed. Run 'apt install pdfcrack'")
                return
            print(self.net_sec.pdfcrack_cmd(args))
        elif cmd == "airgeddon":
            if "airgeddon" not in self.pkg.installed_apt:
                print("airgeddon not installed. Run 'apt install airgeddon'")
                return
            print(self.net_sec.airgeddon_cmd(args))
        elif cmd == "fluxion":
            if "fluxion" not in self.pkg.installed_apt:
                print("fluxion not installed. Run 'apt install fluxion'")
                return
            print(self.net_sec.fluxion_cmd(args))
        elif cmd == "kismet":
            if "kismet" not in self.pkg.installed_apt:
                print("kismet not installed. Run 'apt install kismet'")
                return
            print(self.net_sec.kismet_cmd(args))
        elif cmd == "dsniff":
            if "dsniff" not in self.pkg.installed_apt:
                print("dsniff not installed. Run 'apt install dsniff'")
                return
            print(self.net_sec.dsniff_cmd(args))
        elif cmd == "mitmproxy":
            if "mitmproxy" not in self.pkg.installed_apt:
                print("mitmproxy not installed. Run 'apt install mitmproxy'")
                return
            print(self.net_sec.mitmproxy_cmd(args))
        elif cmd == "sslstrip":
            if "sslstrip" not in self.pkg.installed_apt:
                print("sslstrip not installed. Run 'apt install sslstrip'")
                return
            print(self.net_sec.sslstrip_cmd(args))
        elif cmd == "sslsplit":
            if "sslsplit" not in self.pkg.installed_apt:
                print("sslsplit not installed. Run 'apt install sslsplit'")
                return
            print(self.net_sec.sslsplit_cmd(args))
        elif cmd == "tcpdump":
            if "tcpdump" not in self.pkg.installed_apt:
                print("tcpdump not installed. Run 'apt install tcpdump'")
                return
            print(self.net_sec.tcpdump_cmd(args))
        elif cmd == "tshark":
            if "tshark" not in self.pkg.installed_apt:
                print("tshark not installed. Run 'apt install tshark'")
                return
            print(self.net_sec.tshark_cmd(args))
        elif cmd == "medusa":
            if "medusa" not in self.pkg.installed_apt:
                print("medusa not installed. Run 'apt install medusa'")
                return
            print(self.net_sec.medusa_cmd(args))
        elif cmd == "ncrack":
            if "ncrack" not in self.pkg.installed_apt:
                print("ncrack not installed. Run 'apt install ncrack'")
                return
            print(self.net_sec.ncrack_cmd(args))
        elif cmd == "patator":
            if "patator" not in self.pkg.installed_apt:
                print("patator not installed. Run 'apt install patator'")
                return
            print(self.net_sec.patator_cmd(args))
        # Основные модули
        elif cmd == "apt":
            print(self.pkg.apt_execute(args))
        elif cmd == "pip":
            print(self.pkg.pip_execute(args))
        elif cmd == "python3":
            if not args:
                print("Python 3.11.2 (default, Feb 12 2026)\nType 'exit' to leave interactive shell simulation (only files execution supported now).")
                return
            print(self.pkg.run_python_runtime(args[0], self.vfs))
        elif cmd == "ip":
            print(self.net_sec.ip_cmd(args))
        elif cmd == "ping":
            print(self.net_sec.ping_cmd(args))
        elif cmd == "macchanger":
            print(self.net_sec.macchanger_cmd(args))
        elif cmd == "nmap":
            print(self.net_sec.nmap_cmd(args))
        elif cmd == "hydra":
            print(self.net_sec.hydra_cmd(args, self.vfs))
        else:
            print(f"bash: {cmd}: command not found")

    def run(self):
        self.boot()
        while self.running:
            self.process_input()

# =============================================================================
# ТОЧКА ВХОДА (START RUNTIME)
# =============================================================================
if __name__ == "__main__":
    kali_env = KaliOperatingSystem()
    kali_env.run()
