import undetected_chromedriver as uc
import time
import re
import os

def fetch_stream_data():
    print("[*] Tarayıcı headless modda başlatılıyor...")

    options = uc.ChromeOptions()
    options.add_argument("--headless")  # GitHub Actions için zorunlu
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-gpu')

    # Gerçekçi bir User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        # HATA ÇÖZÜMÜ: GitHub'daki Chrome sürümüyle eşitlemek için version_main eklendi
        print("[*] ChromeDriver sürümü ayarlanıyor (Sürüm: 146)...")
        driver = uc.Chrome(options=options, version_main=146)
        
        # GitHub Secrets'tan URL'yi çekiyoruz
        url = os.getenv("TARGET_URL")
        if not url:
            print("[!] Hata: TARGET_URL bulunamadı! GitHub Secrets ayarlarını kontrol edin.")
            return

        print(f"[*] Hedef siteye gidiliyor: {url}")
        driver.get(url)

        print("[*] Sayfa yükleniyor (15 sn bekleniyor)...")
        time.sleep(15)

        print("[*] Buton aranıyor ve tıklanıyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary') ||
                      document.querySelector('#submit');
            if(btn) { 
                btn.scrollIntoView();
                btn.click(); 
            }
        """)

        print("[*] Yönlendirme kontrol ediliyor...")
        found = False
        for _ in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            time.sleep(1)

        if found:
            print("[+] Yeni sayfa açıldı, veriler çekiliyor...")
            time.sleep(5)
            source = driver.page_source
            
            # Değerleri ayıkla (value="içerik")
            values = re.findall(r'value="([^"]+)"', source)

            # Sayısal olanlar (User/Pass) ve Link (Host) ayıklama
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                host = links[0]
                user = creds[0]
                pwd = creds[1]

                print(f"\n✅ VERİLER ALINDI:\nHOST: {host}\nUSER: {user}")

                # Dosyaya kaydet
                with open("hesap_bilgileri.txt", "w", encoding="utf-8") as f:
                    f.write(f"--- IPTV GÜNCEL BİLGİLER ({time.ctime()}) ---\n")
                    f.write(f"HOST : {host}\n")
                    f.write(f"USER : {user}\n")
                    f.write(f"PASS : {pwd}\n")
                    f.write(f"M3U  : {host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts\n")
                
                print("[+] hesap_bilgileri.txt başarıyla güncellendi.")
            else:
                print("[-] Veriler sayfa kaynağında bulunamadı. Site yapısı değişmiş olabilir.")
                print("[DEBUG] Sayfa içeriği:", source[:500]) # Hata analizi için ilk 500 karakter
        else:
            print(f"[!] Beklenen sayfa açılmadı. Mevcut URL: {driver.current_url}")

    except Exception as e:
        print(f"[!] Hata oluştu: {e}")

    finally:
        if driver:
            print("[*] Tarayıcı kapatılıyor...")
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
