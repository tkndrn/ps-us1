import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı: Derin arama modu...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=None) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Site açıldı, 30 saniye bekleniyor (Daha uzun bekleme)...")
        time.sleep(30) 

        print("[+] Butona basılıyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
            if(btn) { btn.click(); }
        """)
        
        print("[*] Yönlendirme bekleniyor (20 sn)...")
        time.sleep(20)
        
        source = driver.page_source
        
        # SÜZGEÇ GENİŞLETİLDİ: Hem 10 hem 12 haneli rakamları yakalar
        # Bazı günlerde site 10 haneli de üretebiliyor, ikisini de kapsıyoruz.
        numbers = re.findall(r'value="([0-9]{10,12})"', source)

        if len(numbers) >= 2:
            user = numbers[0]
            pwd = numbers[1]
            
            output = f"USER: {user}\nPASS: {pwd}\nGUNCELLEME: {time.strftime('%d-%m-%Y %H:%M:%S')}"
            
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(output)
            
            print(f"✅ BAŞARILI! Veri yazıldı: {user} / {pwd}")
        else:
            print("[-] HATA: Rakamlar bulunamadı!")
            # Eğer rakam bulamazsa, dosyanın içine "HATA" yazsın ki boş kalmasın
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(f"HATA: Veri bulunamadı! Sayfa Başlığı: {driver.title}\nSaat: {time.strftime('%H:%M:%S')}")
            
    except Exception as e:
        print(f"[!] KRİTİK HATA: {e}")
    finally:
        if driver:
            driver.quit()
