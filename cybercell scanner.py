# ================================================
#       CYBERCELL SCANNER v1.0
#       Coded by Mr. Sabaz Ali Khan
#       Advanced Network & Port Scanner with GUI
# ================================================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import subprocess
import platform
import time
from datetime import datetime
import sys


class CyberCellScanner(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🛡️ CyberCell Scanner - Coded by Mr. Sabaz Ali Khan")
        self.geometry("1000x720")
        self.configure(bg="#0a0a0a")
        self.resizable(True, True)

        self.create_widgets()
        self.print_banner()

    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                 CYBERCELL SCANNER v1.0                       ║
║           Coded by Mr. Sabaz Ali Khan                        ║
║           Advanced Port & Network Scanner                    ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def create_widgets(self):
        # Header
        header = tk.Label(self, text="🛡️ CyberCell Scanner", 
                         font=("Consolas", 24, "bold"), bg="#0a0a0a", fg="#00ff9d")
        header.pack(pady=15)

        author = tk.Label(self, text="Coded by Mr. Sabaz Ali Khan • Ethical Hacking Tool", 
                         font=("Consolas", 12), bg="#0a0a0a", fg="#00cc7a")
        author.pack(pady=5)

        # Notebook (Tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # ================== PORT SCANNER TAB ==================
        port_tab = ttk.Frame(notebook)
        notebook.add(port_tab, text="🔌 Port Scanner")

        ttk.Label(port_tab, text="Target IP / Hostname:", font=("Consolas", 11)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self.target_entry = ttk.Entry(port_tab, width=45, font=("Consolas", 11))
        self.target_entry.grid(row=0, column=1, padx=10, pady=12)
        self.target_entry.insert(0, "192.168.1.1")

        ttk.Label(port_tab, text="Start Port:", font=("Consolas", 11)).grid(row=1, column=0, padx=15, pady=8, sticky="w")
        self.start_port = ttk.Entry(port_tab, width=20, font=("Consolas", 11))
        self.start_port.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.start_port.insert(0, "1")

        ttk.Label(port_tab, text="End Port:", font=("Consolas", 11)).grid(row=2, column=0, padx=15, pady=8, sticky="w")
        self.end_port = ttk.Entry(port_tab, width=20, font=("Consolas", 11))
        self.end_port.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.end_port.insert(0, "1024")

        self.scan_btn = ttk.Button(port_tab, text="🚀 START PORT SCAN", command=self.start_port_scan)
        self.scan_btn.grid(row=3, column=1, pady=15)

        self.port_results = scrolledtext.ScrolledText(port_tab, height=22, font=("Consolas", 10), bg="#000000", fg="#00ff9d")
        self.port_results.grid(row=4, column=0, columnspan=2, padx=15, pady=10, sticky="nsew")

        # ================== NETWORK SCANNER TAB ==================
        net_tab = ttk.Frame(notebook)
        notebook.add(net_tab, text="🌐 Network Scanner")

        ttk.Label(net_tab, text="Network Base (e.g. 192.168.1):", font=("Consolas", 11)).grid(row=0, column=0, padx=15, pady=20, sticky="w")
        self.net_base = ttk.Entry(net_tab, width=35, font=("Consolas", 11))
        self.net_base.grid(row=0, column=1, padx=10, pady=20)
        self.net_base.insert(0, "192.168.1")

        self.net_scan_btn = ttk.Button(net_tab, text="🔍 SCAN LOCAL NETWORK", command=self.start_network_scan)
        self.net_scan_btn.grid(row=1, column=1, pady=10)

        self.net_results = scrolledtext.ScrolledText(net_tab, height=24, font=("Consolas", 10), bg="#000000", fg="#00ff9d")
        self.net_results.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="nsew")

        # Status Bar
        self.status = tk.Label(self, text=" Ready | Educational Purpose Only | Mr. Sabaz Ali Khan ", 
                              bg="#111827", fg="#00cc7a", anchor="w")
        self.status.pack(side="bottom", fill="x", padx=20, pady=8)

    def log_port(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.port_results.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.port_results.see(tk.END)

    def start_port_scan(self):
        target = self.target_entry.get().strip()
        try:
            start = int(self.start_port.get())
            end = int(self.end_port.get())
        except ValueError:
            messagebox.showerror("Error", "Ports must be valid numbers!")
            return

        if not target:
            messagebox.showerror("Error", "Please enter a target IP or hostname!")
            return

        self.port_results.delete(1.0, tk.END)
        self.log_port(f"Starting scan on {target} from port {start} to {end}")
        self.scan_btn.config(state="disabled")

        def scan():
            open_count = 0
            for port in range(start, end + 1):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_count += 1
                        try:
                            banner = sock.recv(2048).decode(errors='ignore').strip()
                            self.log_port(f"✅ OPEN  → Port {port:<5} | {banner[:70]}")
                        except:
                            self.log_port(f"✅ OPEN  → Port {port}")
                    sock.close()
                except:
                    pass
                time.sleep(0.02)

            self.log_port(f"✅ Scan Complete! Found {open_count} open ports.")
            self.scan_btn.config(state="normal")

        threading.Thread(target=scan, daemon=True).start()

    def start_network_scan(self):
        base = self.net_base.get().strip()
        if not base.endswith("."):
            base += "."

        self.net_results.delete(1.0, tk.END)
        self.net_results.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Starting Network Scan on {base}0/24...\n\n")
        self.net_scan_btn.config(state="disabled")

        def ping_sweep():
            count = "-n 1" if platform.system().lower() == "windows" else "-c 1"
            live = 0

            for i in range(1, 255):
                ip = f"{base}{i}"
                try:
                    output = subprocess.Popen(["ping", count, "-w", "2", ip],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE).communicate()[0]

                    if b"Reply from" in output or b"bytes from" in output:
                        live += 1
                        self.net_results.insert(tk.END, f"✅ LIVE → {ip}\n")
                        self.net_results.see(tk.END)
                except:
                    pass

                time.sleep(0.08)

            self.net_results.insert(tk.END, f"\n🎉 Network Scan Completed! {live} live hosts found.\n")
            self.net_scan_btn.config(state="normal")

        threading.Thread(target=ping_sweep, daemon=True).start()


# ============================ CLI MODE ============================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("CyberCell Scanner CLI Mode (Coming Soon...)")
    else:
        app = CyberCellScanner()
        app.mainloop()