import requests

def fetch_and_convert():
    # 你的原始数据源
    url = "https://metowolf.github.io/iplist/data/country/CN.txt"
    rsc_file = "cn-ipv6.rsc"
    list_name = "CN"

    try:
        response = requests.get(url)
        # 确保下载成功
        if response.status_code == 200:
            ips = response.text.splitlines()
            
            with open(rsc_file, "w") as f:
                # 1. 写入开头：先清空该名字的旧列表
                f.write(f"/ipv6 firewall address-list remove [find list=\"{list_name}\"]\n")
                
                # 2. 写入数据：批量添加
                # 使用延迟(delay)或分组添加可以减轻低端路由器的压力
                count = 0
                for ip in ips:
                    ip = ip.strip()
                    if ":" in ip:  # 确保是 IPv6
                        f.write(f"/ipv6 firewall address-list add list=\"{list_name}\" address={ip}\n")
                        count += 1
            
            print(f"转换完成，共处理 {count} 条 IPv6 地址。")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    fetch_and_convert()
