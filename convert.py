import requests
import os

# --- 配置区 ---
SOURCES = [
    {
        "url": "https://metowolf.github.io/iplist/data/country/CN.txt",
        "v4_list": "CN_IP",
        "v6_list": "CN_IPv6",
        "filename": "china_ip.rsc"
    }
]

def fetch_and_convert():
    output_dir = "output"
    # 确保 output 文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_map = {}
    removed_records = set()

    for src in SOURCES:
        fname = src.get("filename", "default.rsc")
        # 路径拼接
        fpath = os.path.join(output_dir, fname)
        
        if fpath not in file_map:
            file_map[fpath] = []
            
        print(f"正在处理: {src['url']} -> {fpath}")
        try:
            resp = requests.get(src['url'], timeout=30)
            if resp.status_code != 200: continue
            
            lines = resp.text.replace('\r', '').split('\n')
            for line in lines:
                ip = line.strip()
                if not ip or len(ip) < 3: continue
                
                # IPv6 逻辑
                if ":" in ip and "v6_list" in src:
                    lname = src["v6_list"]
                    if (fpath, lname, "v6") not in removed_records:
                        file_map[fpath].append(f'/ipv6 firewall address-list remove [find list="{lname}"]')
                        removed_records.add((fpath, lname, "v6"))
                    file_map[fpath].append(f'/ipv6 firewall address-list add list="{lname}" address={ip}')
                
                # IPv4 逻辑
                elif "." in ip and "v4_list" in src:
                    lname = src["v4_list"]
                    if (fpath, lname, "v4") not in removed_records:
                        file_map[fpath].append(f'/ip firewall address-list remove [find list="{lname}"]')
                        removed_records.add((fpath, lname, "v4"))
                    file_map[fpath].append(f'/ip firewall address-list add list="{lname}" address={ip}')
        except Exception as e:
            print(f"处理出错: {e}")

    # 写入文件
    for fpath, cmds in file_map.items():
        if cmds:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("\n".join(cmds))
            print(f"成功生成: {fpath} ({len(cmds)} 行)")

if __name__ == "__main__":
    fetch_and_convert()
