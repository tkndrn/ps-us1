import undetected_chromedriver as uc
import time
import re
import os

def fetch_stream_data():
    print("[*] OPERASYON: Form zorlama ve prototip modu başlatıldı...")
    
    options = uc.ChromeOptions()
    is_github = os.getenv("GITHUB_ACTIONS") == "true"

    if is_github:
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        options.add_argument("--window-position=-3000,0")
        options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        # GitHub'daki Chrome 146 sürümüyle eşleşme
        driver = uc.Chrome(version_main=146, options=options)
        
        target_url = os.getenv("TARGET_URL", "https://freeiptv2023-d.ottc.xyz/index.php")
        print(f"[*] Siteye giriliyor: {target_url}")
        driver.get(target_url)
        
        # Sayfanın ve korumaların yüklenmesi için bekleme
        print("[*] Bekleniyor (20 sn)...")
        time.sleep(20)

        print("[*] Form gönderiliyor (Prototip metodu)...")
        # 'form.submit is not a function' hatasını aşmak için en sağlam yöntem:
        driver.execute_script("""
            try {
                var form = document.querySelector('form');
                if(form) {
                    var hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'submit';
                    hiddenInput.value = 'submit';
                    form.appendChild(hiddenInput);
                    
                    // Orijinal submit fonksiyonunu çağır (isim çakışmasını önler)
                    HTMLFormElement.prototype.submit.call(form);
                } else {
                    console.log("Form bulunamadı!");
                }
            } catch (e) {
                console.log("JS Hatası: " + e);
            }
        """)

        print("[*] Yönlendirme kontrol ediliyor...")
        found = False
        for i in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            if i % 10 == 0:
                print(f"[*] Bekleniyor... Mevcut URL: {driver.current_url}")
            time.sleep(1)
            
        if found:
            print("[+] BAŞARILI! Sayfa yönlendi, veriler çekiliyor...")
            time.sleep(5)
            source = driver.page_source
            
            # Regex ile bilgileri çekme
            values = re.findall(r'value="([^"]+)"', source)
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                host, user, pwd = links[0], creds[0], creds[1]
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"HOST : {host}\nUSER : {user}\nPASS : {pwd}\n")
                    f.write(f"Son Guncelleme: {time.ctime()}\n")
                print(f"[+] BİLGİLER ALINDI: {user}")
            else:
                print("[-] Bilgiler ayıklanamadı, sayfa yapısı farklı.")
        else:
            print(f"[!] HATA: Site geçişe izin vermedi. URL: {driver.current_url}")

    except Exception as e:
        print(f"[!] Kritik Hata: {e}")
    finally:
        if driver:
            print("[*] Tarayıcı kapatılıyor...")
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
