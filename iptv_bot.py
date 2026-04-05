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
    
    try:
        # Sürüm hatasını aşmak için headless modda tarayıcıyı otomatik yakalattırıyoruz
        # version_main=None yaparak en uygun sürücüye kendini uydurmasını sağlıyoruz
        driver = uc.Chrome(options=options, version_main=None) 
        
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Siteye giriş yapıldı, 15sn bekleniyor...")
        time.sleep(15)
        
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        print("[+] Butona basıldı, yönlendirme bekleniyor...")
        time.sleep(10)
        
        if "action=view" in driver.current_url:
            source = driver.page_source
            # Regex ile bilgileri çekiyoruz
            numbers = re.findall(r'value="([0-9]{10,12})"', source)
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(numbers) >= 2 and links:
                user = numbers[0]
                pwd = numbers[1]
                host = links[0]
                
                m3u_content = f"#EXTM3U\n#EXTINF:-1,KRAL IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts\n"
                
                with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u_content)
                print(f"✅ Başarılı: User: {user}")
            else:
                print("[-] HATA: Veriler ayıklanamadı.")
        else:
            print(f"[-] HATA: Yönlendirme başarısız. URL: {driver.current_url}")

    except Exception as e:
        print(f"[!] KRİTİK HATA: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    github_run()
