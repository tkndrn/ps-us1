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
    
    # GitHub'ın en güncel sürümünü kullanması için version_main=None
    driver = uc.Chrome(options=options, version_main=None) 
    
    try:
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Site açıldı, 20 saniye bekleniyor...")
        time.sleep(20) # Bekleme süresini biraz artırdık (Garanti olsun)
        
        print("[+] Butona basılıyor...")
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        
        time.sleep(10)
        print(f"[*] Mevcut sayfa: {driver.current_url}")
        
        if "action=view" in driver.current_url:
            source = driver.page_source
            # Regex ile verileri ayıkla
            numbers = re.findall(r'value="([0-9]{10,12})"', source)
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(numbers) >= 2 and links:
                user, pwd = numbers[0], numbers[1]
                host = links[0].rstrip('/')
                
                m3u_link = f"{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts"
                
                # VAR OLAN DOSYANIN ÜZERİNE YAZIYORUZ
                with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,KRAL IPTV\n{m3u_link}\n")
                
                print(f"✅ LİSTE GÜNCELLENDİ: {user}")
            else:
                print("[-] HATA: Veriler sayfada bulunamadı!")
        else:
            print("[-] HATA: Butona basıldı ama sayfa değişmedi.")
            
    except Exception as e:
        print(f"[!] HATA: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    github_run()
