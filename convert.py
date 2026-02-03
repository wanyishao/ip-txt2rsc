import requests
import os

def fetch_and_convert():
    # 建议换成这个更直接的源
    url = "https://metowolf.github.io/iplist/data/country/CN.txt"
    rsc_file = "cn6.rsc"
    list_name = "CN_IPv6"

    print(f"正在获取: {url}")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # 兼容多种换行符并过滤掉空行
            lines = response.text.replace('\r', '').split('\n')
            
            with open(rsc_file, "w", encoding="utf-8") as f:
                f.write(f"/ipv6 firewall address-list remove [find list=\"{list_name}\"]\n")
                
                count = 0
                for line in lines:
                    clean_ip = line.strip()
                    # 只要包含冒号且长度超过 2 (排除只有 : 的异常情况)
                    if ":" in clean_ip and len(clean_ip) > 2:
                        f.write(f"/ipv6 firewall address-list add list=\"{list_name}\" address={clean_ip}\n")
                        count += 1
            
            print(f"转换成功！共写入 {count} 条 IPv6 地址到 {rsc_file}")
            
            # 关键调试：如果 count 是 0，强制报错让 Action 失败，方便排查
            if count == 0:
                print("警告：没有找到任何有效 IPv6 地址，请检查源文件内容！")
                print(f"原始数据前 100 字符: {response.text[:100]}")
                exit(1)
        else:
            print(f"下载失败，状态码: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"脚本运行出错: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_convert()
