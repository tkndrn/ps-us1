import undetected_chromedriver as uc
import time
import re
import os

def github_run():
    options = uc.ChromeOptions()
    options.add_argument('--headless') # GitHub'da ekran yok, bu şart
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # GitHub sunucuları en güncel Chrome'u kullanır, sürüm belirtmiyoruz
    driver = uc.Chrome(options=options)
    
    try:
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        time.sleep(15)
        
        # Butona basma
        driver.execute_script("document.querySelector('input[type=\"submit\"]').click();")
        time.sleep(10)
        
        if "action=view" in driver.current_url:
            source = driver.page_source
            values = re.findall(r'value="([^"]+)"', source)
            creds = [v for v in values if v.isdigit() and len(v) >= 10]
            links = [v for v in values if v.startswith("http")]

            if creds and links:
                m3u = f"{links[0]}/get.php?username={creds[0]}&password={creds[1]}&type=m3u_plus&output=ts"
                with open("iptv_listem.m3u", "w") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1,KRAL IPTV\n{m3u}\n")
    finally:
        driver.quit()

if __name__ == "__main__":
    github_run()
