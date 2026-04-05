import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = None
    try:
        # Botu başlat
        driver = uc.Chrome(options=options, version_main=None) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Bekleniyor...")
        time.sleep(30) # Sitenin açılması için süre

        # Butona tıkla
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        time.sleep(20) # Yönlendirme süresi
        
        source = driver.page_source
        numbers = re.findall(r'value="([0-9]{10,12})"', source)

        if len(numbers) >= 2:
            user, pwd = numbers[0], numbers[1]
            content = f"USER: {user}\nPASS: {pwd}\nSAAT: {time.strftime('%H:%M:%S')}"
            print(f"✅ BULDUM: {user}")
        else:
            content = f"HATA: Rakamlar bulunamadı! Sayfa Başlığı: {driver.title}\nZaman: {time.strftime('%H:%M:%S')}"
            print("[-] Rakamlar yok.")

    except Exception as e:
        content = f"KRITIK HATA: {str(e)}"
        print(f"[!] Hata: {e}")
    
    # NE OLURSA OLSUN DOSYAYA YAZ!
    with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    if driver:
        driver.quit()

if __name__ == "__main__":
    github_run()
