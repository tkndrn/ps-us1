import undetected_chromedriver as uc
import time
import re
import os
import random

def tam_gercekci_sizma_v8():
    print("[*] OPERASYON: V8 Kilid Kırıcı Başladı...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    
    # Her seferinde biraz farklı bir kimlik (User-Agent)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        # Sürüm 146 zorunlu
        driver = uc.Chrome(version_main=146, options=options)
        
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Site açıldı, insan simülasyonu yapılıyor...")
        
        # Sayfayı yavaşça aşağı kaydır (İnsan taklidi)
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(random.randint(35, 45)) # 35-45 sn arası rastgele bekle (Sabit değil)

        print("[+] Buton aranıyor ve tetikleniyor...")
        # Butonu bulup hem tıkla hem de formu zorla gönder
        driver.execute_script("""
            var forms = document.forms;
            if(forms.length > 0) {
                console.log("Form bulundu, gönderiliyor...");
                forms[0].submit();
            } else {
                var btn = document.querySelector('input[type="submit"]') || document.querySelector('button');
                if(btn) btn.click();
            }
        """)
        
        print("[*] Yönlendirme bekleniyor (Max 40 sn)...")
        found = False
        for i in range(40):
            # Eğer URL değiştiyse veya yeni sayfa geldiyse
            if "action=view" in driver.current_url or "view.php" in driver.current_url:
                found = True
                break
            time.sleep(1)
            if i % 10 == 0: print(f"[*] Bekleniyor... {i}. saniye")
            
        if found:
            print("[+] BİNGO! Hedef sayfa açıldı.")
            time.sleep(7) # Verilerin tam yüklenmesi için biraz daha sabır
            
            source = driver.page_source
            # Value içindeki rakamları ve linkleri topla
            creds = re.findall(r'value="([0-9]{10,12})"', source)
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(creds) >= 2 and links:
                host, user, pwd = links[0], creds[0], creds[1]
                content = f"USER: {user}\nPASS: {pwd}\nHOST: {host}\nSAAT: {time.strftime('%H:%M:%S')}"
                print(f"✅ ZAFER: {user} / {pwd}")
            else:
                content = f"HATA: Sayfa açıldı ama rakamlar saklanmış. Başlık: {driver.title}"
                print("[-] Veri çekilemedi.")
        else:
            # Burası önemli: Eğer hala yönlenmiyorsa sayfanın ne dediğini görelim
            content = f"HATA: Site bizi içeri almadı (Timeout). Mevcut URL: {driver.current_url}"
            print(f"[!] Giriş başarısız. URL: {driver.current_url}")

    except Exception as e:
        content = f"SİSTEM HATASI: {str(e)}"
        print(f"[!] Hata: {e}")
        
    finally:
        with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
            f.write(content)
        if driver:
            driver.quit()

if __name__ == "__main__":
    tam_gercekci_sizma_v8()
