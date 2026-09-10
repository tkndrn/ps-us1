import undetected_chromedriver as uc
import time
import re
import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def freeiptv_enigma2_ready():
    print("[*] FreeIPTV - GitHub Actions Başlatılıyor...")

    cache_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'undetected_chromedriver')
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path)
        except:
            pass

    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # GitHub bulut sunucusunda ekran olmadığı için headless mod zorunludur:
    options.add_argument("--headless=new")

    driver = None
    try:
        driver = uc.Chrome(options=options)

        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Sayfa açıldı, Cloudflare / Turnstile bekleniyor...")

        # Turnstile doğrulamasının tamamlanıp butona tıklanabilir olmasını bekle
        wait = WebDriverWait(driver, 30)
        create_btn = wait.until(EC.element_to_be_clickable((By.ID, "create-btn")))
        
        print("[*] Buton aktifleşti, tıklanıyor...")
        create_btn.click()

        print("[*] Form gönderildi, sonuç sayfası bekleniyor...")
        time.sleep(10)

        source = driver.page_source

        # Kullanıcı adı ve şifre desenlerini yakala
        username_match = re.search(r'Username.*?(\d{9,})', source, re.IGNORECASE | re.DOTALL)
        password_match = re.search(r'Password.*?(\d{9,})', source, re.IGNORECASE | re.DOTALL)
        
        # CDN / Bootstrap linklerini eleyip gerçek IPTV host adresini bul
        host_matches = re.findall(r'(http[s]?://[^\s"\'<>]+)', source)
        real_host = "http://freeiptv.ottc.xyz:80"
        
        for h in host_matches:
            h_lower = h.lower()
            if not any(x in h_lower for x in ["jsdelivr", "bootstrap", "cdnjs", "google", "fonts", "iconify"]):
                if ":" in h.replace("https://", "").replace("http://", "") or "ottc" in h or "server" in h or "shop" in h:
                    real_host = h.rstrip('/')
                    break

        if username_match and password_match:
            # Gelen verilerin doğru sırayla yerleşmesi için eşleşme düzeni
            user = password_match.group(1)
            pwd = username_match.group(1)

            print("\n" + "💎" * 30)
            print(f"✅ BAŞARILI!")
            print(f"Host     : {real_host}")
            print(f"Username : {user}")
            print(f"Password : {pwd}")
            print("💎" * 30)

            m3u_content = f"#EXTM3U\n#EXTINF:-1,Free IPTV\n{real_host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts"
            
            with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)

            print("[+] M3U dosyası oluşturuldu: iptv_listem.m3u")
        else:
            print("[-] Credential bulunamadı. 'son_sayfa.html' kaydediliyor.")
            with open("son_sayfa.html", "w", encoding="utf-8") as f:
                f.write(source)

    except Exception as e:
        print(f"[!] Kritik Hata: {e}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    freeiptv_enigma2_ready()
