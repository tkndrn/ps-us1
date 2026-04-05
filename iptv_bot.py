import undetected_chromedriver as uc
import time
import re
import os

def fetch_stream_data():
    print("[*] Tarayıcı başlatılıyor...")

    options = uc.ChromeOptions()

    # Tarayıcıyı görünmeyen bir konumda aç (headless yerine)
    options.add_argument("--window-position=-3000,0")
    options.add_argument("--window-size=1920,1080")

    # User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    try:
        driver = uc.Chrome(version_main=146, options=options)

        # Kullanıcıdan URL al
        url = input("Site URL gir: ")
        driver.get(url)

        print("[*] Sayfa yükleniyor...")
        time.sleep(15)

        print("[*] Buton kontrol ediliyor...")
        driver.execute_script("""
            var btn = document.querySelector('input[type="submit"]') || 
                      document.querySelector('button') ||
                      document.querySelector('.btn-primary');
            if(btn) { 
                btn.scrollIntoView();
                btn.click(); 
            }
        """)

        print("[*] Yönlendirme bekleniyor...")
        found = False

        for _ in range(30):
            if "action=view" in driver.current_url:
                found = True
                break
            time.sleep(1)

        if found:
            print("[+] Yeni sayfa açıldı, veri çekiliyor...")
            time.sleep(3)

            source = driver.page_source

            values = re.findall(r'value="([^"]+)"', source)

            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if len(creds) >= 2 and links:
                host = links[0]
                user = creds[0]
                pwd = creds[1]

                print("\n" + "="*40)
                print("✅ İŞLEM BAŞARILI")
                print(f"HOST : {host}")
                print(f"USER : {user}")
                print(f"PASS : {pwd}")
                print("="*40)

                m3u_path = os.path.join(os.getcwd(), "iptv_listem.m3u")

                with open(m3u_path, "w", encoding="utf-8") as f:
                    f.write("#EXTM3U\n")
                    f.write(f"#EXTINF:-1,OTOMATIK IPTV\n")
                    f.write(f"{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts\n")

                print(f"[+] M3U oluşturuldu: {m3u_path}")

            else:
                print("[-] Gerekli veriler bulunamadı.")

        else:
            print("[!] Yönlendirme olmadı veya sayfa değişmedi.")

    except Exception as e:
        print(f"[!] Hata: {e}")

    finally:
        print("[*] Tarayıcı kapatılıyor...")
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    fetch_stream_data()
