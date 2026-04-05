import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı: 12 haneli güncel User/Pass avı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        # Sürüm hatası almamak için otomatik ayarlı başlatıyoruz
        driver = uc.Chrome(options=options, version_main=None) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Site açıldı, sayaç için 25 saniye bekleniyor...")
        time.sleep(25) 

        print("[+] Butona basılıyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
            if(btn) { btn.click(); }
        """)
        
        print("[*] Yeni sayfanın yüklenmesi bekleniyor (15 sn)...")
        time.sleep(15)
        
        source = driver.page_source
        
        # Sitenin o gün ürettiği her türlü 12 haneli rakamı yakalar
        numbers = re.findall(r'value="([0-9]{12})"', source)

        if len(numbers) >= 2:
            user = numbers[0]
            pwd = numbers[1]
            
            # Dosyayı her gün taze bilgilerle güncelliyoruz
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(f"USER: {user}\n")
                f.write(f"PASS: {pwd}\n")
                f.write(f"SON_GUNCELLEME: {time.strftime('%d-%m-%Y %H:%M:%S')}\n")
            
            print(f"✅ BAŞARILI! Bugünün verileri: {user} / {pwd}")
        else:
            print("[-] HATA: Rakamlar bulunamadı. Site botu engellemiş olabilir.")
            
    except Exception as e:
        print(f"[!] KRİTİK HATA: {e}")
    finally:
        if driver:
            driver.quit()
            print("[*] Tarayıcı kapatıldı.")

if __name__ == "__main__":
    github_run()
