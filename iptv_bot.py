import undetected_chromedriver as uc
import time
import re
import os

def fetch_stream_data():
    print("[*] OPERASYON: Chrome maskesiyle sızılıyor...")
    
    options = uc.ChromeOptions()
    
    # GitHub Actions ortamında mıyız kontrol et
    is_github = os.getenv("GITHUB_ACTIONS") == "true"

    if is_github:
        # GitHub'da headless yerine sanal ekran (Xvfb) kullanılacağı için pencereyi normal açıyoruz
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        # Kendi PC'nde tarayıcıyı yana kaydırır
        options.add_argument("--window-position=-3000,0")
        options.add_argument("--window-size=1920,1080")

    # Gerçekçi User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        # Sürüm hatasını çözmek için 146'ya sabitledik
        driver = uc.Chrome(version_main=146, options=options)
        
        # URL'yi Secret'tan al, yoksa manuel linki kullan
        target_url = os.getenv("TARGET_URL", "https://freeiptv2023-d.ottc.xyz/index.php")
        
        print(f"[*] Siteye giriliyor: {target_url}")
        driver.get(target_url)
        
        print("[*] Sayfa yüklendi, 20 sn bekleniyor...")
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
        
        print("[*] Yönlendirme kontrol ediliyor...")
        found = False
        for i in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            time.sleep(1)
            
        if found:
            print("[+] Hedef sayfa açıldı! Veriler çekiliyor...")
            time.sleep(5)
            source = driver.page_source
            values = re.findall(r'value="([^"]+)"', source)
            
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                host, user, pwd = links[0], creds[0], creds[1]
                print(f"\n✅ BAŞARILI! HOST: {host} USER: {user}")

                # Dosyaya kaydet (YAML bu ismi arayacak)
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"HOST : {host}\nUSER : {user}\nPASS : {pwd}\n")
                    f.write(f"M3U  : {host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts\n")
            else:
                print("[-] Bilgiler ayıklanamadı.")
        else:
            print(f"[!] HATA: Yönlendirme olmadı. Mevcut URL: {driver.current_url}")

    except Exception as e:
        print(f"[!] Kritik Hata: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
