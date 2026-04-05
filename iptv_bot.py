import undetected_chromedriver as uc
import time
import re
import os
import random

def tam_gercekci_sizma_v10():
    print("[*] OPERASYON: V10 Arka Kapı Sızması Başladı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        driver = uc.Chrome(version_main=146, options=options)
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Ana sayfa yüklendi...")
        
        # Siteyi "hazır olduğuna" ikna etmek için bekleme
        time.sleep(40) 

        print("[+] Zorla Yönlendirme (Form Force) başlatılıyor...")
        # Butona basmak yerine formu doğrudan POST ediyoruz
        driver.execute_script("""
            var forms = document.forms;
            if (forms.length > 0) {
                var formData = new FormData(forms[0]);
                // Eğer submit butonu bir değer bekliyorsa onu da ekliyoruz
                formData.append('submit', 'submit'); 
                
                // Formu AJAX veya normal yolla değil, doğrudan submit metoduyla tetikle
                forms[0].submit();
            }
        """)
        
        print("[*] Yönlendirme ve Veri yakalama fazı (50 sn)...")
        found = False
        for i in range(50):
            # Sitenin URL'sinin değiştiği anı yakala
            if "action=view" in driver.current_url or "view.php" in driver.current_url:
                found = True
                break
            time.sleep(1)
            
        if found:
            print(f"[+] Hedef sayfa açıldı! URL: {driver.current_url}")
            time.sleep(8) # Verilerin render edilmesi için
            
            source = driver.page_source
            # Yeni regex: Hem inputlardaki değerleri hem de düz metni yakala
            creds = re.findall(r'value="([0-9]{10,12})"', source)
            if not creds: # Eğer value içinde yoksa düz metin ara
                creds = re.findall(r'([0-9]{10,12})', source)
                
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(creds) >= 2 and links:
                host, user, pwd = links[0], creds[0], creds[1]
                content = f"USER: {user}\nPASS: {pwd}\nHOST: {host}\nSAAT: {time.strftime('%H:%M:%S')}"
                print(f"✅ HEDEF VURULDU: {user}")
            else:
                content = f"HATA: Sayfa açıldı ama veri ayıklanamadı. Kaynak boyutu: {len(source)}"
                print("[-] Veri ayıklama başarısız.")
        else:
            content = f"HATA: Kapı hala kilitli. URL: {driver.current_url}\nBaşlık: {driver.title}"
            print("[!] Yönlendirme yine başarısız.")

    except Exception as e:
        content = f"SISTEM HATASI: {str(e)}"
        
    finally:
        with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
            f.write(content)
        if driver:
            driver.quit()

if __name__ == "__main__":
    tam_gercekci_sizma_v10()
