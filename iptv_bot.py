import undetected_chromedriver as uc
import time
import re
import os

def fetch_stream_data():
    print("[*] SON DENEME: Form verisi zorlama modu...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        driver = uc.Chrome(version_main=146, options=options)
        target_url = os.getenv("TARGET_URL", "https://freeiptv2023-d.ottc.xyz/index.php")
        
       try:
        driver = uc.Chrome(version_main=146, options=options)
        target_url = os.getenv("TARGET_URL", "https://freeiptv2023-d.ottc.xyz/index.php")
        
        print(f"[*] Ana sayfaya giriliyor: {target_url}")
        driver.get(target_url)
        time.sleep(15) 

        print("[*] Form verileri zorlanıyor...")
        driver.execute_script("""
            try {
                var form = document.querySelector('form');
                if(form) {
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'submit';
                    input.value = 'submit';
                    form.appendChild(input);
                    HTMLFormElement.prototype.submit.call(form);
                }
            } catch (e) {
                console.log("JS Hatası: " + e);
            }
        """)

        print("[*] Yönlendirme bekleniyor...")
        found = False
        for i in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            time.sleep(1)

        if found:
            print("[+] SIZMA BAŞARILI!")
            time.sleep(5)
            source = driver.page_source
            values = re.findall(r'value="([^"]+)"', source)
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"HOST : {links[0]}\nUSER : {creds[0]}\nPASS : {creds[1]}\n")
                print("[+] VERİLER REPOYA YAZILDI.")
            else:
                print("[-] Sayfa açıldı ama değerler boş.")
        else:
            print(f"[!] Site geçişi engelledi. Mevcut URL: {driver.current_url}")
            # Bu aşamada hala olmuyorsa site GitHub IP'sini tamamen bloklamıştır.
            
    except Exception as e:
        print(f"[!] Hata: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
