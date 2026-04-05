import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı: Manuel sürüm kontrolü aktif...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Sisteme gerçekçi bir kimlik veriyoruz
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = None
    try:
        # Hata aldığımız 147 sürümüne gitmemesi için 146'yı açıkça belirtiyoruz
        # GitHub logunda 'Current browser version is 146' dediği için bunu kullanıyoruz
        print("[*] Chrome 146 için sürücü ayarlanıyor...")
        driver = uc.Chrome(options=options, version_main=146) 
        
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        print("[*] Site açıldı, sayaç bekleniyor (40 sn)...")
        time.sleep(40) 

        print("[+] Butona basılıyor...")
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        
        print("[*] Yönlendirme bekleniyor (20 sn)...")
        time.sleep(20)
        
        source = driver.page_source
        numbers = re.findall(r'value="([0-9]{10,12})"', source)

        if len(numbers) >= 2:
            user, pwd = numbers[0], numbers[1]
            content = f"USER: {user}\nPASS: {pwd}\nSAAT: {time.strftime('%H:%M:%S')}"
            print(f"✅ BAŞARILI: {user}")
        else:
            # Rakam yoksa sayfa içeriğine dair küçük bir ipucu alalım
            title = driver.title if driver.title else "Baslik Yok"
            content = f"HATA: Rakamlar bulunamadı! Sayfa Başlığı: {title}"
            print(f"[-] Rakam yok. Sayfa: {title}")

    except Exception as e:
        content = f"BOT HATASI (V146 Denemesi): {str(e)}"
        print(f"[!] HATA: {e}")
    
    with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    if driver:
        driver.quit()

if __name__ == "__main__":
    github_run()
