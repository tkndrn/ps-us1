import undetected_chromedriver as uc
import time
import re
import os

def hibrit_sizma_v12():
    print("[*] OPERASYON: V12 Hibrit Sızma Başladı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    
    # Gerçekçi kimlik
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        # Sürüm 146 ile başlat (Senin sistemde çalışan tek sürüm)
        driver = uc.Chrome(version_main=146, options=options)
        
        print("[*] Siteye giriş yapılıyor...")
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        # Sitenin korumasını aşmak için en kritik bekleme (50 saniye)
        print("[*] JavaScript sayaçlarının dolması bekleniyor (50 sn)...")
        time.sleep(50) 

        print("[+] 'Zaman Doldu' hilesi ve Form tetikleme yapılıyor...")
        # İşte burası sihirli değnek: Sitenin içindeki formu zorla submit ediyoruz
        driver.execute_script("""
            var forms = document.forms;
            if(forms.length > 0) {
                // Formun içindeki gizli 'submit' sinyalini manuel oluşturup gönderiyoruz
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'submit';
                input.value = 'submit';
                forms[0].appendChild(input);
                forms[0].submit();
            }
        """)
        
        print("[*] Yönlendirme için 30 saniye pusuya yatıldı...")
        found = False
        for _ in range(30):
            # URL'de 'view' kelimesini veya sayfa değişimini yakala
            if "view" in driver.current_url or "index.php" not in driver.current_url:
                found = True
                break
            time.sleep(1)
            
        if found:
            print(f"[+] HEDEF SAYFA AÇILDI: {driver.current_url}")
            time.sleep(10) # Sayfa verilerinin (rakamların) gelmesi için
            
            source = driver.page_source
            # 10-12 haneli rakamları her yerden topla
            creds = re.findall(r'([0-9]{10,12})', source)
            # Host linkini bul
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(creds) >= 2:
                user, pwd = creds[0], creds[1]
                host = links[0] if links else "Host Bulunamadı"
                content = f"USER: {user}\nPASS: {pwd}\nHOST: {host}\nSAAT: {time.strftime('%H:%M:%S')}"
                print(f"✅ BİNGO! Veriler alındı: {user}")
            else:
                content = f"HATA: Sayfa açıldı ama rakamlar gelmedi. Başlık: {driver.title}"
                print("[-] Veri ayıklama hatası.")
        else:
            content = f"HATA: Site hala kapalı. Mevcut URL: {driver.current_url}"
            print("[!] Kapı hala açılmadı.")

    except Exception as e:
        content = f"SISTEM HATASI: {str(e)}"
        
    finally:
        # Sonucu mutlaka dosyaya yazalım
        with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
            f.write(content)
        if driver:
            driver.quit()

if __name__ == "__main__":
    hibrit_sizma_v12()
