import undetected_chromedriver as uc
import re
import time
import os

def github_run():
    print("[*] Operasyon başladı...")
    
    # Klasör kontrolü (Dosya nereye yazılıyor görelim)
    print(f"[*] Mevcut dizin: {os.getcwd()}")

    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        # Sürüm hatasını aşmak için en garanti yöntem
        driver = uc.Chrome(options=options, version_main=None) 
        
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Ana sayfa açıldı, 15sn bekleniyor...")
        time.sleep(15)
        
        # Butona basma işlemi
        print("[+] Butona basılıyor...")
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        
        # Yönlendirme bekleme
        print("[*] Yönlendirme bekleniyor...")
        time.sleep(10)
        
        print(f"[*] Mevcut URL: {driver.current_url}")
        
        source = driver.page_source
        # Regex: Sayıları ve Linkleri ayıkla
        numbers = re.findall(r'value="([0-9]{10,12})"', source)
        links = re.findall(r'value="(http[^"]+)"', source)

        if len(numbers) >= 2 and links:
            user = numbers[0]
            pwd = numbers[1]
            host = links[0].rstrip('/') # Sondaki / işaretini temizle
            
            # M3U İçeriği
            m3u_content = f"#EXTM3U\n#EXTINF:-1,KRAL IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts\n"
            
            # DOSYAYI YAZMA (Tam yol belirterek)
            file_path = os.path.join(os.getcwd(), "iptv_listem.m3u")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(m3u_content)
            
            print(f"✅ BAŞARILI: Dosya oluşturuldu: {file_path}")
            print(f"👤 User: {user} | 🔑 Pass: {pwd}")
        else:
            print("[-] HATA: Veriler ayıklanamadı! Sayfa kaynağı eksik olabilir.")
            # Hata anında sayfa başlığını görelim
            print(f"[*] Sayfa Başlığı: {driver.title}")
            
    except Exception as e:
        print(f"[!] KRİTİK SİSTEM HATASI: {e}")
    finally:
        if driver:
            driver.quit()
            print("[*] Tarayıcı kapatıldı.")

if __name__ == "__main__":
    github_run()
