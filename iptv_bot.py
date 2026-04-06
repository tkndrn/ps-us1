import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os

def fetch_stream_data():
    print("[*] Tarayıcı 'Ultra-Gizli' modda başlatılıyor...")

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Bot engelleme savar ayarlar
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    
    driver = None
    try:
        # Sürüm 146 hatasını çözmüştük
        driver = uc.Chrome(options=options, version_main=146)
        
        # Tarayıcıyı bot değilmiş gibi gösteren script
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        url = os.getenv("TARGET_URL")
        print(f"[*] Hedef siteye gidiliyor: {url}")
        driver.get(url)

        print("[*] Sayfa yükleniyor (25 sn)...")
        time.sleep(25)

        driver.save_screenshot("1_sayfa_yuklendi.png")

        print("[*] Buton aranıyor (Fare simülasyonu)...")
        try:
            # Butonu bulmaya çalış
            btn = driver.execute_script("""
                return document.querySelector('input[type="submit"]') || 
                       document.querySelector('button') ||
                       document.querySelector('.btn-primary') ||
                       document.querySelector('#submit');
            """)
            
            if btn:
                print("[+] Buton bulundu, üzerine gidiliyor ve tıklanıyor...")
                # Gerçek kullanıcı gibi butonun üzerine git ve tıkla
                actions = ActionChains(driver)
                # Script ile bulunan elementi selenium objesine çeviremediğimiz için 
                # selenium metoduyla tekrar seçiyoruz:
                elements = driver.find_elements("css selector", 'input[type="submit"], button, .btn-primary, #submit')
                if elements:
                    actions.move_to_element(elements[0]).click().perform()
                else:
                    # Eğer selenium bulamazsa JavaScript ile zorla tıkla
                    driver.execute_script("arguments[0].click();", btn)
            else:
                print("[-] Buton bulunamadı, form doğrudan gönderiliyor...")
                driver.execute_script("document.forms[0].submit();")
        except Exception as btn_err:
            print(f"[!] Buton tıklama hatası: {btn_err}")

        print("[*] Yönlendirme bekleniyor (35 sn)...")
        for i in range(35):
            if "action=view" in driver.current_url:
                print(f"[+] Başarılı! Yeni URL: {driver.current_url}")
                break
            if i % 5 == 0:
                print(f"[*] Bekleniyor... URL hala aynı: {driver.current_url}")
                driver.save_screenshot(f"debug_step_{i}.png")
            time.sleep(1)

        if "action=view" in driver.current_url:
            print("[+] Veriler çekiliyor...")
            time.sleep(5)
            source = driver.page_source
            values = re.findall(r'value="([^"]+)"', source)
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"HOST : {links[0]}\nUSER : {creds[0]}\nPASS : {creds[1]}\n")
                print("[+] BİLGİLER KAYDEDİLDİ.")
            else:
                print("[-] Sayfa açıldı ama veri formatı farklı.")
        else:
            print("[!] Yönlendirme gerçekleşmedi. Site GitHub'ı engellemiş olabilir.")

    except Exception as e:
        print(f"[!] Kritik Hata: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
