import requests
import os

# --- 配置区：在此定义你的源、ROS列表名、以及输出的文件名 ---
SOURCES = [
    {
        "url": "https://metowolf.github.io/iplist/data/country/CN.txt",
        "v4_list": "CN_IP",
        "v6_list": "CN_IPv6",
        "filename": "china_ip.rsc"
    },
    {
        "url": "https://ispip.clang.cn/all_cn_ipv6.txt",
        "v6_list": "CN_IPv6_HighPrecision", 
        "filename": "high_precision_v6.rsc" 
    }
]

def fetch_and_convert():
    # 存储每个文件的指令集合，格式为 { filename: [commands] }
    file_map = {}
    # 记录每个 (文件名, 列表名) 是否已经写过 remove 语句
    removed_records = set()

    for src in SOURCES:
        fname = src.get("filename", "default.rsc")
        if fname not in file_map:
            file_map[fname] = []
            
        print(f"正在处理: {src['url']} -> {fname}")
        try:
            resp = requests.get(src['url'], timeout=30)
            if resp.status_code != 200: continue
            
            lines = resp.text.replace('\r', '').split('\n')
            for line in lines:
                ip = line.strip()
                if not ip or len(ip) < 3: continue
                
                # 处理 IPv6
                if ":" in ip and "v6_list" in src:
                    lname = src["v6_list"]
                    if (fname, lname, "v6") not in removed_records:
                        file_map[fname].append(f'/ipv6 firewall address-list remove [find list="{lname}"]')
                        removed_records.add((fname, lname, "v6"))
                    file_map[fname].append(f'/ipv6 firewall address-list add list="{lname}" address={ip}')
                
                # 处理 IPv4
                elif "." in ip and "v4_list" in src:
                    lname = src["v4_list"]
                    if (fname, lname, "v4") not in removed_records:
                        file_map[fname].append(f'/ip firewall address-list remove [find list="{lname}"]')
                        removed_records.add((fname, lname, "v4"))
                    file_map[fname].append(f'/ip firewall address-list add list="{lname}" address={ip}')

        except Exception as e:
            print(f"处理出错: {e}")

    # 写入所有自定义文件
    for fname, cmds in file_map.items():
        if cmds:
            with open(fname, "w", encoding="utf-8") as f:
                f.write("\n".join(cmds))
            print(f"成功生成文件: {fname} (共 {len(cmds)} 行)")

if __name__ == "__main__":
    fetch_and_convert()
