import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os
import random

def fetch_stream_data():
    print("[*] OPERASYON: İleri seviye insan simülasyonu başlatıldı...")
    
    options = uc.ChromeOptions()
    is_github = os.getenv("GITHUB_ACTIONS") == "true"

    if is_github:
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        options.add_argument("--window-position=-3000,0")
        options.add_argument("--window-size=1920,1080")

    # Bot korumalarını aşmak için kritik ayarlar
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = None
    try:
        driver = uc.Chrome(version_main=146, options=options)
        
        # Webdriver izlerini temizle
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

        target_url = os.getenv("TARGET_URL", "https://freeiptv2023-d.ottc.xyz/index.php")
        print(f"[*] Siteye giriş yapılıyor: {target_url}")
        driver.get(target_url)
        
        # 1. Adım: Sayfada rastgele kaydırma yap (İnsan gibi davran)
        print("[*] Sayfada insan simülasyonu yapılıyor...")
        time.sleep(random.randint(5, 10))
        driver.execute_script(f"window.scrollTo(0, {random.randint(300, 700)});")
        time.sleep(random.randint(5, 10))

        # 2. Adım: Butonu bul ve fareyi üzerine getir
        print("[+] Buton aranıyor...")
        try:
            # Selenium ile butonu bul
            elements = driver.find_elements("css selector", 'input[type="submit"], button, .btn-primary, #submit')
            
            if elements:
                btn = elements[0]
                print("[+] Buton bulundu. Fare simülasyonu ile tıklanıyor...")
                
                # Fareyi butonun üzerine götür ve tıkla
                actions = ActionChains(driver)
                actions.move_to_element(btn).pause(random.uniform(0.5, 1.5)).click().perform()
            else:
                print("[-] Buton seçici ile bulunamadı, JS ile zorlanıyor...")
                driver.execute_script("document.querySelector('form').submit();")
        except Exception as e:
            print(f"[!] Tıklama hatası: {e}")

        # 3. Adım: Yönlendirme Bekle (Sabırlı ol)
        print("[*] Yönlendirme bekleniyor (45 sn)...")
        found = False
        for i in range(45):
            if "action=view" in driver.current_url:
                found = True
                break
            if i % 10 == 0:
                print(f"[*] Bekleniyor... Mevcut URL: {driver.current_url}")
            time.sleep(1)
            
        if found:
            print("[+] BAŞARILI! Bilgiler çekiliyor...")
            time.sleep(5)
            source = driver.page_source
            
            # Veri ayıklama
            values = re.findall(r'value="([^"]+)"', source)
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"HOST : {links[0]}\nUSER : {creds[0]}\nPASS : {creds[1]}\n")
                    f.write(f"Guncelleme: {time.ctime()}\n")
                print("[+] Bilgiler dosyaya yazıldı.")
            else:
                print("[-] Sayfa açıldı ama değerler bulunamadı.")
        else:
            print(f"[!] BAŞARISIZ: Site hala geçişe izin vermedi. URL: {driver.current_url}")
            # Hata anında ne gördüğümüzü kaydet
            driver.save_screenshot("hata_anlik.png")

    except Exception as e:
        print(f"[!] Hata: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
