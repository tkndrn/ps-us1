import undetected_chromedriver as uc
import time
import re
import os
import random

def tam_gercekci_sizma_v9():
    print("[*] OPERASYON: V9 Kapı Kırıcı Başladı...")
    
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
        print("[*] Site açıldı, sinsi bekleme moduna geçildi...")
        
        # 45-55 saniye arası uzun bekleme (Sitenin içindeki gizli kontrollerin dolması için)
        time.sleep(random.randint(45, 55)) 

        print("[+] Buton üzerinde 'İnsan Simülasyonu' yapılıyor...")
        # JavaScript ile butonu bul ve "İnsan gibi" etkileşime gir
        driver.execute_script("""
            var forms = document.forms;
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') || 
                      document.querySelector('.btn-primary');
            
            if(btn) {
                btn.focus(); // Butona odaklan
                btn.dispatchEvent(new MouseEvent('mouseover', {bubbles: true})); // Fareyi üzerine getir
                setTimeout(function(){ 
                    btn.click(); // 1 saniye sonra tıkla
                    if(forms.length > 0) forms[0].submit(); // Eğer tıklama yemezse formu zorla gönder
                }, 1000);
            }
        """)
        
        print("[*] Yönlendirme bekleniyor (Max 45 sn)...")
        found = False
        for i in range(45):
            # URL'de değişim var mı? (index.php dışına çıktı mı?)
            if "index.php" not in driver.current_url or "action=view" in driver.current_url:
                found = True
                break
            time.sleep(1)
            if i % 10 == 0: print(f"[*] Bekleniyor... {i}. saniye")
            
        if found:
            print(f"[+] Sayfa değişti! Yeni URL: {driver.current_url}")
            time.sleep(10) # Sayfa tam otursun
            
            source = driver.page_source
            creds = re.findall(r'value="([0-9]{10,12})"', source)
            links = re.findall(r'value="(http[^"]+)"', source)

            if len(creds) >= 2 and links:
                host, user, pwd = links[0], creds[0], creds[1]
                content = f"USER: {user}\nPASS: {pwd}\nHOST: {host}\nSAAT: {time.strftime('%H:%M:%S')}"
                print(f"✅ ZAFER: {user}")
            else:
                content = f"HATA: Sayfa açıldı ama veri yok. URL: {driver.current_url}"
                print("[-] Veri çekilemedi.")
        else:
            # Hala aynı sayfadaysak ekranın "görüntüsünü" (source) bir miktar analiz edelim
            content = f"HATA: Site hala index.php'de çakılı. Sayfa Başlığı: {driver.title}"
            print("[!] Kapı açılmadı.")

    except Exception as e:
        content = f"SİSTEM HATASI: {str(e)}"
        
    finally:
        with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
            f.write(content)
        if driver:
            driver.quit()

if __name__ == "__main__":
    tam_gercekci_sizma_v9()
