import requests
import os

def fetch_and_convert():
    # 推荐使用这个混合源或按需修改 URL
    url = "https://metowolf.github.io/iplist/data/country/CN.txt"
    v4_rsc = "cn_ipv4.rsc"
    v6_rsc = "cn_ipv6.rsc"
    
    print(f"正在获取数据: {url}")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            lines = response.text.replace('\r', '').split('\n')
            
            v4_list = []
            v6_list = []

            for line in lines:
                ip = line.strip()
                if not ip: continue
                
                # 自动判定类型
                if ":" in ip:
                    v6_list.append(ip)
                elif "." in ip:
                    v4_list.append(ip)

            # 写入 IPv4 RSC
            with open(v4_rsc, "w", encoding="utf-8") as f:
                f.write('/ip firewall address-list remove [find list="CN_IP"]\n')
                for ip in v4_list:
                    f.write(f'/ip firewall address-list add list="CN_IP" address={ip}\n')
            
            # 写入 IPv6 RSC
            with open(v6_rsc, "w", encoding="utf-8") as f:
                f.write('/ipv6 firewall address-list remove [find list="CN_IPv6"]\n')
                for ip in v6_list:
                    f.write(f'/ipv6 firewall address-list add list="CN_IPv6" address={ip}\n')

            print(f"转换成功: IPv4({len(v4_list)}条), IPv6({len(v6_list)}条)")
            
            if len(v4_list) == 0 and len(v6_list) == 0:
                print("错误：未识别到任何 IP 数据！")
                exit(1)
        else:
            print(f"下载失败: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"运行出错: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_convert()
