#encoding: utf8
from time import sleep
import requests
import re
import json
import os

proxies = {"https":"127.0.0.1:8080", "http":"127.0.0.1:8080"}
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}

def get_shellcode_list():
    r=requests.get("https://www.exploit-db.com//shellcodes?draw=1&columns%5B0%5D%5Bdata%5D=date_published&columns%5B0%5D%5Bname%5D=date_published&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=download&columns%5B1%5D%5Bname%5D=download&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=verified&columns%5B2%5D%5Bname%5D=verified&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=description&columns%5B3%5D%5Bname%5D=description&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=platform_id&columns%5B4%5D%5Bname%5D=platform_id&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=author_id&columns%5B5%5D%5Bname%5D=author_id&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&start=0&length=2000&search%5Bvalue%5D=&search%5Bregex%5D=false&author=&platform=&_=1651740707658 ",headers=headers)
    return json.loads(r.text)

def download(shellcode_list):
    for shellcode in shellcode_list:
        platform=shellcode["platform_id"]
        describe=shellcode["description"].split("-")[1].replace("</span></a>","").replace(" ","_").replace("/","_")
        if os.path.isdir("./Shellcode/"+platform):
            pass
        else:
            os.mkdir("./Shellcode/"+platform)
        if os.path.isdir("./Shellcode/"+platform+"/"+describe):
            pass
        else:
            os.mkdir("./Shellcode/"+platform+"/"+describe)
        try:
            url="https://www.exploit-db.com/download/{}".format(shellcode["id"])
            r=requests.get(url,headers=headers)
            path="./Shellcode/{}/{}/{}.txt".format(platform,describe,shellcode["id"])
            if os.path.exists(path):
                print("[-] {} 已存在".format(shellcode['id']))
                continue
            else:
                f=open("./Shellcode/{}/{}/{}.txt".format(platform,describe,shellcode["id"]),"wb")
                f.write(r.text)
                f.close()
                print("[+] {} 保存完成".format(shellcode["id"]))
            sleep(0.1)
        except:
            print("[-] {} 下载失败".format(shellcode["id"]))
            continue
        

if __name__ == '__main__':
    shellcode_list=get_shellcode_list()['data']
    download(shellcode_list)