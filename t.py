import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
import psutil
import socket
import os
import datetime
from pathlib import Path

class WindowsToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hızlı Yardım Aracı - Önder Mönder")
        self.root.geometry("1000x700")
        
        # Ana stil ayarları
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Ana frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(
            self.main_frame, 
            text="Hızlı Yardım Aracı - Önder Mönder", 
            font=('Helvetica', 16, 'bold'),
            foreground='green'
        )
        title_label.pack(pady=10)
        
        # Scroll Canvas
        self.canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Butonlar için frame
        self.buttons_frame = ttk.Frame(self.scrollable_frame)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Butonları oluştur
        self.create_buttons()
        
        # Çıktı alanı
        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = tk.Text(self.output_frame, height=15, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Çıktı scrollbar
        output_scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=output_scrollbar.set)

    def create_buttons(self):
        buttons = [
            ("1. Bilgisayar Bilgileri", self.show_system_info),
            ("2. IP Adresi", self.show_ip_address),
            ("3. Windows Lisans", self.show_windows_license),
            ("4. Sistem Bilgileri", self.show_detailed_system_info),
            ("5. Windows Sürüm", self.show_windows_version),
            ("6. Son Format Tarihi", self.show_install_date),
            ("7. Disk Durumu", self.show_disk_status),
            ("8. Windows Güncelleme", self.check_windows_updates),
            ("9. CPU Bilgileri", self.show_cpu_info),
            ("10. RAM Kullanımı", self.show_ram_usage),
            ("11. Grup Politikaları", self.update_group_policy),
            ("12. Kullanıcı Hesapları", self.list_user_accounts),
            ("13. Depolama Alanı", self.show_storage_info),
            ("14. Disk Tarama", self.check_disk),
            ("15. Güvenlik Duvarı Kapat", self.disable_firewall),
            ("16. Güvenlik Duvarı Aç", self.enable_firewall),
            ("17. Sistemi Onar", self.repair_system),
            ("18. Disk Temizliği", self.disk_cleanup),
            ("19. Tüm Programları Güncelle", self.update_all),
            ("20. Windows Store Güncelle", self.update_store),
            ("21. DNS Önbelleği Temizle", self.flush_dns),
            ("22. Temp Temizle", self.clean_temp),
            ("23. RAM Optimize Et", self.optimize_ram),
            ("24. Ping Testi", self.ping_test),
            ("25. Tracert", self.tracert_test),
            ("26. DNS Sorgula", self.nslookup_test),
            ("27. Ağ Durumu", self.show_network_status),
            ("28. ARP Tablosu", self.show_arp_table),
            ("29. Yönlendirme Tablosu", self.show_route_table),
            ("30. BIOS Durumu", self.show_bios_status),
            ("31. IP Yapılandırması", self.show_ip_config),
            ("32. IP Serbest Bırak", self.release_ip),
            ("33. IP Yenile", self.renew_ip),
            ("34. WiFi Durumu", self.show_wifi_status),
            ("35. Çık", self.quit_app)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                self.buttons_frame,
                text=text,
                command=command,
                width=40
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            
    def show_output(self, text):
        try:
            self.output_text.configure(state='normal')
            self.output_text.delete("1.0", "end")
            if text:
                self.output_text.insert("1.0", str(text))
            self.output_text.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Hata", f"Çıktı gösterilirken hata oluştu: {str(e)}")

    def convert_bytes(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"

    def run_command(self, command, shell=False):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                shell=shell
            )
            return result.stdout
        except Exception as e:
            return f"Hata: {str(e)}"

    def show_system_info(self):
        system_info = f"""
Bilgisayar Bilgileri:
    Bilgisayar Adı: {platform.node()}
    İşletim Sistemi: {platform.system()} {platform.release()}
    Sürüm: {platform.version()}
    Makine: {platform.machine()}
    İşlemci: {platform.processor()}
    """
        self.show_output(system_info)

    def show_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        info = f"""
Ağ Bilgileri:
    Bilgisayar Adı: {hostname}
    IP Adresi: {ip_address}
        """
        self.show_output(info)

    def show_windows_license(self):
        result = self.run_command(['slmgr', '/dli'])
        self.show_output(result if result else "Lisans bilgisi alınamadı.")

    def show_detailed_system_info(self):
        result = self.run_command(['systeminfo'])
        self.show_output(result)

    def show_windows_version(self):
        result = self.run_command(['ver'], shell=True)
        self.show_output(result)

    def show_disk_status(self):
        disks_info = []
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                info = f"""
Disk: {partition.device}
    Bağlantı Noktası: {partition.mountpoint}
    Dosya Sistemi: {partition.fstype}
    Toplam Alan: {self.convert_bytes(partition_usage.total)}
    Kullanılan: {self.convert_bytes(partition_usage.used)} ({partition_usage.percent}%)
    Boş Alan: {self.convert_bytes(partition_usage.free)}
"""
                disks_info.append(info)
            except Exception as e:
                disks_info.append(f"Disk {partition.device} bilgisi alınamadı: {str(e)}")
        
        self.show_output("\n".join(disks_info))

    def show_cpu_info(self):
        cpu_info = f"""
CPU Bilgileri:
    Fiziksel Çekirdek Sayısı: {psutil.cpu_count(logical=False)}
    Toplam Çekirdek Sayısı: {psutil.cpu_count()}
    CPU Kullanımı: {psutil.cpu_percent()}%
    
Frekans Bilgileri:
    Mevcut: {psutil.cpu_freq().current:.2f} MHz
    Minimum: {psutil.cpu_freq().min:.2f} MHz
    Maksimum: {psutil.cpu_freq().max:.2f} MHz
"""
        self.show_output(cpu_info)

    def show_ram_usage(self):
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        ram_info = f"""
RAM Kullanımı:
    Toplam RAM: {self.convert_bytes(ram.total)}
    Kullanılan RAM: {self.convert_bytes(ram.used)} ({ram.percent}%)
    Boş RAM: {self.convert_bytes(ram.available)}
    
Swap Kullanımı:
    Toplam Swap: {self.convert_bytes(swap.total)}
    Kullanılan Swap: {self.convert_bytes(swap.used)} ({swap.percent}%)
    Boş Swap: {self.convert_bytes(swap.free)}
"""
        self.show_output(ram_info)

    def show_install_date(self):
        result = self.run_command(['systeminfo'])
        for line in result.split('\n'):
            if "Original Install Date" in line or "Orijinal Kurulum Tarihi" in line:
                install_date = line.split(':', 1)[1].strip()
                self.show_output(f"Windows Kurulum Tarihi: {install_date}")
                return
        self.show_output("Kurulum tarihi bulunamadı.")
    def check_windows_updates(self):
        result = self.run_command(['wuauclt', '/detectnow'])
        self.show_output("""Windows güncelleme kontrolü başlatıldı.
1. Windows Update'i açın
2. "Güncellemeleri denetle" seçeneğine tıklayın
3. Varsa güncellemeleri yükleyin""")

    def update_group_policy(self):
        result = self.run_command(['gpupdate', '/force'])
        self.show_output(result if result else "Grup politikaları güncellendi.")

    def list_user_accounts(self):
        result = self.run_command(['net', 'user'])
        self.show_output(result)

    def show_storage_info(self):
        result = self.run_command(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'])
        self.show_output(result)

    def check_disk(self):
        result = self.run_command(['chkdsk', 'C:'])
        self.show_output(result)

    def disable_firewall(self):
        result = self.run_command(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'])
        self.show_output("Güvenlik duvarı kapatıldı.")

    def enable_firewall(self):
        result = self.run_command(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'])
        self.show_output("Güvenlik duvarı açıldı.")

    def repair_system(self):
        commands = [
            ['sfc', '/scannow'],
            ['DISM', '/Online', '/Cleanup-Image', '/RestoreHealth']
        ]
        for cmd in commands:
            result = self.run_command(cmd)
            self.show_output(result)

    def disk_cleanup(self):
        result = self.run_command(['cleanmgr', '/sagerun:1'])
        self.show_output("Disk temizliği başlatıldı...")

    def update_all(self):
        self.show_output("Tüm programlar güncelleniyor...")
        commands = [
            ['wuauclt', '/detectnow'],
            ['wuauclt', '/updatenow']
        ]
        for cmd in commands:
            result = self.run_command(cmd)
        self.show_output("Güncelleme kontrolleri tamamlandı.")

    def update_store(self):
        result = self.run_command(['wsreset'])
        self.show_output("Windows Store yenilendi. Güncellemeleri kontrol edin.")

    def flush_dns(self):
        result = self.run_command(['ipconfig', '/flushdns'])
        self.show_output("DNS önbelleği temizlendi.")

    def clean_temp(self):
        temp_paths = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            os.path.join(os.environ.get('WINDIR'), 'Temp')
        ]
        
        for temp_path in temp_paths:
            if temp_path and os.path.exists(temp_path):
                try:
                    files = os.listdir(temp_path)
                    for file in files:
                        file_path = os.path.join(temp_path, file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                os.rmdir(file_path)
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
        
        self.show_output("Geçici dosyalar temizlendi.")

    def optimize_ram(self):
        result = self.run_command(['wmic', 'os', 'set', 'FreePhysicalMemory'])
        self.show_output("RAM optimizasyonu yapıldı.")

    def ping_test(self):
        result = self.run_command(['ping', 'google.com'])
        self.show_output(result)

    def tracert_test(self):
        result = self.run_command(['tracert', 'google.com'])
        self.show_output(result)

    def nslookup_test(self):
        result = self.run_command(['nslookup', 'google.com'])
        self.show_output(result)

    def show_network_status(self):
        result = self.run_command(['netstat', '-an'])
        self.show_output(result)

    def show_arp_table(self):
        result = self.run_command(['arp', '-a'])
        self.show_output(result)

    def show_route_table(self):
        result = self.run_command(['route', 'print'])
        self.show_output(result)

    def show_bios_status(self):
        result = self.run_command(['wmic', 'bios', 'get', 'serialnumber,manufacturer,version'])
        self.show_output(result)

    def show_ip_config(self):
        result = self.run_command(['ipconfig', '/all'])
        self.show_output(result)

    def release_ip(self):
        result = self.run_command(['ipconfig', '/release'])
        self.show_output("IP adresi serbest bırakıldı.")

    def renew_ip(self):
        result = self.run_command(['ipconfig', '/renew'])
        self.show_output("IP adresi yenilendi.")

    def show_wifi_status(self):
        result = self.run_command(['netsh', 'wlan', 'show', 'all'])
        self.show_output(result)

    def quit_app(self):
        if messagebox.askokcancel("Çıkış", "Programdan çıkmak istediğinize emin misiniz?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowsToolsGUI(root)
    root.mainloop()