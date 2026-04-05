import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon: Derin sızma başladı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # Gerçekçi kimlik (User-Agent)
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=None) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Site açıldı, 35 saniye bekleniyor (Bot koruması geçiliyor)...")
        time.sleep(35) 

        print("[+] Butona basılıyor...")
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        
        print("[*] Yönlendirme bekleniyor (20 sn)...")
        time.sleep(20)
        
        source = driver.page_source
        # 10 ile 12 haneli rakamları arıyoruz
        numbers = re.findall(r'value="([0-9]{10,12})"', source)

        if len(numbers) >= 2:
            user, pwd = numbers[0], numbers[1]
            content = f"USER: {user}\nPASS: {pwd}\nSAAT: {time.strftime('%H:%M:%S')}\nTARIH: {time.strftime('%d-%m-%Y')}"
            
            # DOSYAYI YAZDIR
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ BAŞARILI: {user} / {pwd}")
        else:
            print("[-] HATA: Rakamlar bulunamadı. Sayfa başlığı: " + driver.title)
            # Hata varsa bile dosyaya yaz ki GitHub "değişiklik var" desin
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(f"HATA: Veri bulunamadı. Sayfa: {driver.title}\nZaman: {time.strftime('%H:%M:%S')}")
            
    except Exception as e:
        print(f"[!] KRİTİK HATA: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    github_run()
