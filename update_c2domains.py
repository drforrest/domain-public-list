import urllib.request
import re

URL = "https://threatfox-api.abuse.ch/v2/files/exports/06b6689a164e6a92fc82084977e3993772336b04d5ae0ff8/hostfile.txt"
OUTPUT_FILE = "c2domains.txt"

def fetch_and_clean_domains():
    print(f"正在從 {URL} 下載清單...")
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "ThreatFox-Extractor/1.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8", errors="ignore")

    domains = set()
    for line in content.splitlines():
        line = line.strip()
        # 略過註解行與空行
        if not line or line.startswith("#"):
            continue

        # 拆分 127.0.0.1 與 domain (空白或 Tab 分隔)
        parts = line.split()
        if len(parts) >= 2:
            domain = parts[1].strip().lower()
            # 排除本機保留位址
            if domain and domain != "localhost":
                domains.add(domain)

    sorted_domains = sorted(domains)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for domain in sorted_domains:
            f.write(f"{domain}\n")

    print(f"處理完成！共取得 {len(sorted_domains)} 筆不重複域名，已儲存至 {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_clean_domains()
