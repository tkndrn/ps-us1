import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon: İnsan simülasyonu aktif...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    # Daha inandırıcı bir kimlik
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = None
    try:
        # Sürüm 146'da sabitliyoruz çünkü senin sistemde o çalışıyor
        driver = uc.Chrome(options=options, version_main=146) 
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        
        # Sitedeki reklamların ve sayacın dolması için uzun bekleme
        print("[*] Site açıldı, 45 saniye sabırla bekleniyor...")
        time.sleep(45) 

        print("[+] Butona basılıyor (Çift yöntem)...")
        # Hem JavaScript ile hem de form göndererek şansımızı deniyoruz
        driver.execute_script("""
            var forms = document.forms;
            if(forms.length > 0) { forms[0].submit(); }
            else { 
                var btn = document.querySelector('input[type="submit"]') || document.querySelector('button');
                if(btn) btn.click();
            }
        """)
        
        print("[*] Rakamların yüklenmesi için 25 saniye daha...")
        time.sleep(25)
        
        source = driver.page_source
        
        # SÜZGEÇ: Sadece value içinde değil, sayfanın herhangi bir yerindeki 10-12 haneli rakamları ara
        numbers = re.findall(r'([0-9]{10,12})', source)

        # Kendini tekrar eden rakamları temizle (Set kullanarak)
        unique_numbers = list(dict.fromkeys(numbers))

        if len(unique_numbers) >= 2:
            user, pwd = unique_numbers[0], unique_numbers[1]
            content = f"USER: {user}\nPASS: {pwd}\nSAAT: {time.strftime('%H:%M:%S')}"
            print(f"✅ BULDUM: {user} / {pwd}")
        else:
            # Eğer rakam bulamazsa sayfanın o anki görüntüsünü anlamak için kodun bir kısmını kaydedelim
            debug_info = source[:500].replace('\n', ' ')
            content = f"HATA: Rakam yok! Sayfa: {driver.title}\nLog: {debug_info}"
            print("[-] Maalesef rakamlar yakalanamadı.")

    except Exception as e:
        content = f"SISTEM HATASI: {str(e)}"
    
    with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    if driver:
        driver.quit()

if __name__ == "__main__":
    github_run()
