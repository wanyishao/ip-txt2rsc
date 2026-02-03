import requests
import os

# --- 配置区：在此添加你的网址和对应的 ROS 列表名 ---
SOURCES = [
    {
        "url": "https://metowolf.github.io/iplist/data/country/CN.txt",
        "v4_list": "CN_IP",
        "v6_list": "CN_IPv6"
    },
    # 你可以继续添加其他源，例如：
    # {
    #     "url": "https://raw.githubusercontent.com/someuser/list/main/whitelist.txt",
    #     "v4_list": "Whitelist_v4",
    #     "v6_list": "Whitelist_v6"
    # }
]

def fetch_and_convert():
    v4_commands = []
    v6_commands = []
    
    # 用来记录每个 List 是否已经写过 remove 指令，防止重复删除
    v4_removed = set()
    v6_removed = set()

    for src in SOURCES:
        print(f"正在处理源: {src['url']}")
        try:
            resp = requests.get(src['url'], timeout=30)
            if resp.status_code != 200:
                print(f"跳过：下载失败({resp.status_code})")
                continue
            
            lines = resp.text.replace('\r', '').split('\n')
            
            for line in lines:
                ip = line.strip()
                if not ip or len(ip) < 3: continue
                
                # 处理 IPv6
                if ":" in ip:
                    list_name = src['v6_list']
                    if list_name not in v6_removed:
                        v6_commands.append(f'/ipv6 firewall address-list remove [find list="{list_name}"]')
                        v6_removed.add(list_name)
                    v6_commands.append(f'/ipv6 firewall address-list add list="{list_name}" address={ip}')
                
                # 处理 IPv4
                elif "." in ip:
                    list_name = src['v4_list']
                    if list_name not in v4_removed:
                        v4_commands.append(f'/ip firewall address-list remove [find list="{list_name}"]')
                        v4_removed.add(list_name)
                    v4_commands.append(f'/ip firewall address-list add list="{list_name}" address={ip}')

        except Exception as e:
            print(f"处理源时出错: {e}")

    # 写入文件
    if v4_commands:
        with open("cn_ipv4.rsc", "w", encoding="utf-8") as f:
            f.write("\n".join(v4_commands))
        print(f"已生成 cn_ipv4.rsc (共 {len(v4_commands)} 行)")

    if v6_commands:
        with open("cn_ipv6.rsc", "w", encoding="utf-8") as f:
            f.write("\n".join(v6_commands))
        print(f"已生成 cn_ipv6.rsc (共 {len(v6_commands)} 行)")

if __name__ == "__main__":
    fetch_and_convert()
