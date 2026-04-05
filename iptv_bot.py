import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı: 12 haneli User/Pass avı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=None) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Site yüklendi, bot koruması için 25 saniye bekleniyor...")
        time.sleep(25) 

        print("[+] Butona basılıyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
            if(btn) { btn.click(); }
        """)
        
        print("[*] Yönlendirme bekleniyor (15 sn)...")
        time.sleep(15)
        
        source = driver.page_source
        
        # SENİN VERDİĞİN FORMAT: 12 haneli rakamları yakalar
        # Bu Regex tam olarak 12 haneli sayıları hedef alır
        numbers = re.findall(r'value="([0-9]{12})"', source)

        if len(numbers) >= 2:
            # İlk 12 hane User, ikinci 12 hane Pass
            user = numbers[0]
            pwd = numbers[1]
            
            # Dosyaya tertemiz yazıyoruz
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(f"USER: {user}\n")
                f.write(f"PASS: {pwd}\n")
                f.write(f"GUNCELLEME: {time.strftime('%d-%m-%Y %H:%M:%S')}\n")
            
            print(f"✅ BAŞARILI! Yakalanan Veri: {user} / {pwd}")
        else:
            print("[-] HATA: 12 haneli rakamlar bulunamadı. Sayfa yapısı değişmiş olabilir.")
            print(f"[*] Sayfa özeti: {driver.title}")
            
    except Exception as e:
        print(f"[!] KRİTİK HATA: {e}")
    finally:
        if driver:
            driver.quit()
            print("[*] Tarayıcı kapatıldı.")

if __name__ == "__main__":
    github_run()
