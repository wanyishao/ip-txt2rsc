import requests
import os

def fetch_and_convert():
    url = "https://metowolf.github.io/iplist/data/country/CN.txt"
    rsc_file = "cn6.rsc"
    list_name = "CN_IPv6"

    print(f"正在从 {url} 获取数据...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            ips = response.text.splitlines()
            # 获取当前脚本所在目录，确保文件写在正确位置
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, rsc_file)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"/ipv6 firewall address-list remove [find list=\"{list_name}\"]\n")
                count = 0
                for ip in ips:
                    ip = ip.strip()
                    if ":" in ip:
                        f.write(f"/ipv6 firewall address-list add list=\"{list_name}\" address={ip}\n")
                        count += 1
            print(f"成功创建文件: {file_path}, 包含 {count} 条记录")
        else:
            print(f"下载失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"转换脚本出错: {e}")

if __name__ == "__main__":
    fetch_and_convert()
