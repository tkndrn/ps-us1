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

    # User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        # Sürümü otomatik algılaması için version_main'i kaldırdık
        driver = uc.Chrome(options=options)

        # URL'yi GitHub Secrets'tan veya environment'tan alıyoruz
        # Eğer manuel girmek istersen burayı 'https://site.com' yapabilirsin
        url = os.getenv("TARGET_URL")
        if not url:
            print("[!] Hata: TARGET_URL bulunamadı!")
            return

        print(f"[*] Hedef siteye gidiliyor: {url}")
        driver.get(url)

        print("[*] Sayfa yükleniyor (15 sn bekleniyor)...")
        time.sleep(15)

        print("[*] Buton aranıyor ve tıklanıyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
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
            print("[+] Sayfa yakalandı, veriler ayrıştırılıyor...")
            time.sleep(5)
            source = driver.page_source
            values = re.findall(r'value="([^"]+)"', source)

            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                host = links[0]
                user = creds[0]
                pwd = creds[1]

                result = f"""
========================================
✅ İŞLEM BAŞARILI
HOST : {host}
USER : {user}
PASS : {pwd}
========================================
"""
                print(result)

                # M3U Dosyasını oluştur
                m3u_content = f"#EXTM3U\n#EXTINF:-1,OTOMATIK IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts\n"
                with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u_content)
                
                print("[+] iptv_listem.m3u dosyası oluşturuldu.")
            else:
                print("[-] Gerekli veriler (user/pass/host) bulunamadı.")
        else:
            print("[!] Beklenen sayfa yönlendirmesi gerçekleşmedi.")

    except Exception as e:
        print(f"[!] Beklenmedik Hata: {e}")

    finally:
        if driver:
            print("[*] Tarayıcı kapatılıyor...")
            driver.quit()

if __name__ == "__main__":
    fetch_stream_data()
