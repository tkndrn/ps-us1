
import undetected_chromedriver as uc
import time
import re
import os

def tam_gercekci_sizma_v7():
    print("[*] OPERASYON: GitHub Sunucusunda V7 Modu Başladı...")
    
    options = uc.ChromeOptions()
    
    # GitHub Actions için en stabil ayarlar bunlardır:
    options.add_argument('--headless') # Sunucuda ekran olmadığı için mecburuz
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    
    # Senin sürümle tam uyumlu User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        # Sürüm 146'yı zorla (Hata almamak için en kritik yer)
        driver = uc.Chrome(version_main=146, options=options)
        
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Site yüklendi, sayaç bekleniyor (20 sn)...")
        time.sleep(20)
        
        print("[+] Butona basılıyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
            if(btn) { 
                btn.scrollIntoView();
                btn.click(); 
            }
        """)
        
        print("[*] Yönlendirme kontrol ediliyor (Max 30 sn)...")
        found = False
        for _ in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            time.sleep(1)
            
        if found:
            print("[+] Hedef sayfa açıldı! Veriler çekiliyor...")
            time.sleep(5)
            
            source = driver.page_source
            # Value içindeki 10-12 haneli rakamları bul
            creds = re.findall(r'value="([0-9]{10,12})"', source)
            # URL'leri bul
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(creds) >= 2 and links:
                host, user, pwd = links[0], creds[0], creds[1]
                content = f"USER: {user}\nPASS: {pwd}\nHOST: {host}\nSAAT: {time.strftime('%H:%M:%S')}"
                print(f"✅ İŞLEM BAŞARILI: {user}")
            else:
                content = "HATA: Rakamlar veya Link bulunamadı. Sayfa içeriği değişmiş."
                print("[-] Bilgiler ayıklanamadı.")
        else:
            content = "HATA: Yönlendirme gerçekleşmedi (Timeout)."
            print("[!] Hata: Site hala bot olduğundan şüpheleniyor.")

    except Exception as e:
        content = f"BOT HATASI: {str(e)}"
        print(f"[!] Hata: {e}")
        
    finally:
        # SONUCU YAZ (Mutlaka hesap_bilgileri.txt adını kullan ki yml dosyası pushlasın)
        with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
            f.write(content)
        
        if driver:
            driver.quit()

if __name__ == "__main__":
    tam_gercekci_sizma_v7()
