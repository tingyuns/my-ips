import urllib.request

def fetch_and_combine():
    # 你的三个目标优选 IP 链接
    urls = [
        "https://raw.githubusercontent.com/gslege/CloudflareIP/refs/heads/main/JP.txt",
        "https://raw.githubusercontent.com/gslege/CloudflareIP/refs/heads/main/SG.txt",
        "https://raw.githubusercontent.com/gslege/CloudflareIP/refs/heads/main/US.txt"
    ]
    
    all_ips = []
    
    for url in urls:
        try:
            # 伪装成浏览器请求，防止被部分 CDN 拦截
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                text = response.read().decode('utf-8').strip()
                if text:
                    # 按换行符分割并存入总列表
                    all_ips.extend(text.splitlines())
        except Exception as e:
            print(f"抓取失败: {url}, 错误信息: {e}")

    # 清洗数据：去前后空格，过滤掉不包含 . (IPv4) 或 : (IPv6) 的杂质行
    cleaned_ips = []
    for ip in all_ips:
        ip = ip.strip()
        if ip and ('.' in ip or ':' in ip):
            cleaned_ips.append(ip)
            
    # 精准去重（并保持抓取到的先后顺序）
    unique_ips = list(dict.fromkeys(cleaned_ips))

    # 将最终结果写入到当前目录下的 ip.txt 中
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_ips))
        
    print(f"汇总去重完成！共保留了 {len(unique_ips)} 个唯一 IP。")

if __name__ == "__main__":
    fetch_and_combine()
