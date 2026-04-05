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
    # Siteyi kandırmak için gerçekçi bir pencere boyutu
    options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        print("[*] Tarayıcı başlatılıyor...")
        driver = uc.Chrome(options=options, version_main=None) 
        
        print("[*] Siteye gidiliyor...")
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        # Sitenin yüklenmesi ve bot kontrolü için uzun süre bekle
        print("[*] 25 saniye bekleniyor (Bot koruması için)...")
        time.sleep(25) 
        
        # Sayfa başlığını kontrol et (Doğru yerde miyiz?)
        print(f"[*] Şu anki sayfa başlığı: {driver.title}")

        print("[+] Butona basılıyor (JavaScript)...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
            if(btn) { btn.click(); }
        """)
        
        print("[*] Yönlendirme için 15 saniye bekleniyor...")
        time.sleep(15)
        
        print(f"[*] Mevcut URL: {driver.current_url}")
        
        # Sayfa içeriğini al
        source = driver.page_source
        
        # Rakamları ayıkla (User ve Pass)
        numbers = re.findall(r'value="([0-9]{10,12})"', source)

        if len(numbers) >= 2:
            user = numbers[0]
            pwd = numbers[1]
            
            # Dosyayı oluştur
            with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                f.write(f"USER: {user}\n")
                f.write(f"PASS: {pwd}\n")
                f.write(f"TARIH: {time.strftime('%d-%m-%Y %H:%M:%S')}\n")
            
            print(f"✅ BAŞARILI! Dosya oluşturuldu. User: {user}")
        else:
            print("[-] HATA: User/Pass bulunamadı! Sayfa içeriği bot korumasına takılmış olabilir.")
            # Hata varsa sayfanın bir kısmını yazdır ki ne gördüğümüzü anlayalım
            print(f"[*] Sayfa içeriği (İlk 500 karakter): {source[:500]}")
            
    except Exception as e:
        print(f"[!] KRİTİK HATA: {e}")
    finally:
        if driver:
            driver.quit()
            print("[*] Tarayıcı kapatıldı.")

if __name__ == "__main__":
    github_run()
