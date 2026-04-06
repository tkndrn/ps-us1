import undetected_chromedriver as uc
import time
import re
import os

def fetch_stream_data():
    print("[*] Tarayıcı headless modda başlatılıyor...")

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Bot algılamasını zorlaştırmak için ek ayarlar
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = None
    try:
        # Sürüm hatasını çözmüştük (146)
        driver = uc.Chrome(options=options, version_main=146)
        
        url = os.getenv("TARGET_URL")
        if not url:
            print("[!] Hata: TARGET_URL bulunamadı!")
            return

        print(f"[*] Hedef siteye gidiliyor: {url}")
        driver.get(url)

        print("[*] Sayfa yükleniyor (20 sn bekleniyor)...")
        time.sleep(20)

        # Hata ayıklama: Sayfa yüklendiğinde ne görüyoruz?
        print(f"[DEBUG] Mevcut URL: {driver.current_url}")
        driver.save_screenshot("debug_sayfa_ilk.png") 

        print("[*] Buton aranıyor ve tıklanıyor (Agresif Mod)...")
        # Tüm olası buton tiplerini deneyen gelişmiş script
        driver.execute_script("""
            var forms = document.forms;
            if(forms.length > 0) {
                forms[0].submit(); // Doğrudan formu gönder
            } else {
                var btn = document.querySelector('input[type="submit"]') || 
                          document.querySelector('button') ||
                          document.querySelector('.btn-primary') ||
                          document.querySelector('a[href*="action"]');
                if(btn) btn.click();
            }
        """)

        print("[*] Yönlendirme bekleniyor (30 sn)...")
        found = False
        for i in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            if i % 5 == 0:
                print(f"[*] Bekleniyor... Şimdiki URL: {driver.current_url}")
            time.sleep(1)

        if found:
            print("[+] Hedef sayfa açıldı! Veriler çekiliyor...")
            time.sleep(5)
            source = driver.page_source
            
            # Veri çekme mantığı aynı
            values = re.findall(r'value="([^"]+)"', source)
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                host = links[0]; user = creds[0]; pwd = creds[1]
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"HOST : {host}\nUSER : {user}\nPASS : {pwd}\n")
                print("[+] hesap_bilgileri.txt güncellendi.")
            else:
                print("[-] Veri bulunamadı. Sayfa kaynağını kontrol edin.")
                driver.save_screenshot("debug_hata_sayfasi.png")
        else:
            print(f"[!] Yönlendirme başarısız. Son URL: {driver.current_url}")
            driver.save_screenshot("debug_final_url.png")

    except Exception as e:
        print(f"[!] Hata: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
