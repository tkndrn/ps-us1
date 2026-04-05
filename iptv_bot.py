import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı: Sadece User ve Pass çekiliyor...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless') # GitHub için ekran kapalı mod şart
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        # Sürüm çakışmasını önlemek için version_main=None
        driver = uc.Chrome(options=options, version_main=None) 
        
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Site açıldı, 20 saniye bekleniyor...")
        time.sleep(20) 
        
        print("[+] Butona basılıyor...")
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        
        print("[*] Yönlendirme bekleniyor...")
        time.sleep(10)
        
        if "action=view" in driver.current_url:
            source = driver.page_source
            # 10-12 haneli rakamları ayıklıyoruz (User ve Pass)
            numbers = re.findall(r'value="([0-9]{10,12})"', source)

            if len(numbers) >= 2:
                user = numbers[0]
                pwd = numbers[1]
                
                # Dosyayı oluşturup içine yazıyoruz
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"USER: {user}\n")
                    f.write(f"PASS: {pwd}\n")
                    f.write(f"SON GUNCELLEME: {time.strftime('%d-%m-%Y %H:%M:%S')}\n")
                
                print(f"✅ BAŞARILI! User: {user} | Pass: {pwd}")
            else:
                print("[-] HATA: Sayfada User/Pass bulunamadı.")
        else:
            print(f"[-] HATA: Sayfa yönlenmedi. Mevcut URL: {driver.current_url}")
            
    except Exception as e:
        print(f"[!] HATA OLUŞTU: {e}")
    finally:
        if driver:
            driver.quit()
            print("[*] Tarayıcı kapatıldı.")

if __name__ == "__main__":
    github_run()
