import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı: Sürüm uyumlu mod...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = None
    try:
        # version_main=None ve suppress_welcome=True ile en uyumlu hali başlatıyoruz
        driver = uc.Chrome(options=options, version_main=None, suppress_welcome=True) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Site açıldı, bekleme moduna geçildi (35 sn)...")
        time.sleep(35) 

        print("[+] Butona basılıyor...")
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        
        print("[*] Sonuç sayfası bekleniyor (20 sn)...")
        time.sleep(20)
        
        source = driver.page_source
        numbers = re.findall(r'value="([0-9]{10,12})"', source)

        if len(numbers) >= 2:
            user, pwd = numbers[0], numbers[1]
            content = f"USER: {user}\nPASS: {pwd}\nSAAT: {time.strftime('%H:%M:%S')}"
            print(f"✅ BAŞARILI: {user}")
        else:
            content = f"HATA: Rakamlar bulunamadı! Sayfa: {driver.title}"
            print("[-] Rakam yok.")

    except Exception as e:
        # Hata mesajını txt dosyasına yazdır ki görelim
        content = f"BOT HATASI: {str(e)}"
        print(f"[!] HATA: {e}")
    
    # SONUCU DOSYAYA YAZ
    with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    if driver:
        driver.quit()

if __name__ == "__main__":
    github_run()
