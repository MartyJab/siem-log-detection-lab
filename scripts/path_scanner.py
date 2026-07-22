import requests,time,random
TARGET="http://webserver"
paths=["/admin","/admin/login","/admin.php","/login","/login.php","/user","/account","/dashboard","/panel","/controlpanel","/.env","/config","/config.php","/settings","/settings.php","/database","/db","/db.sql","/backup","/backup.zip","/backup.tar.gz","/dump.sql","/.git","/.git/config","/wp-admin","/wp-login.php","/wp-content","/wp-config.php","/joomla","/drupal","/typo3","/magento","/debug","/console","/dev","/test","/staging","/api","/api/v1","/api/v2","/swagger","/docs","/server-status","/server-info","/status","/phpinfo.php","/info.php","/uploads","/files","/images","/downloads","/private","/tmp","/temp","/phpmyadmin","/pma","/webmail","/cpanel","/whm","/plesk","/old","/new","/v1","/v2","/backup_old","/data","/logs","/log","/errors"]
normal_paths=["/","/index.html","/home","/about","/contact"]

def send_request(url):
    try:
        headers={"User-Agent":random.choice(["Mozilla/5.0","curl/7.68.0","python-requests/2.28","ScannerBot/1.0"])}
        r=requests.get(url,headers=headers,timeout=2)
        print(f"{url} -> {r.status_code}")
    except:
        print(f"{url} -> ERROR")

def run_scan():
    print("Starting expanded scan simulation...")
    for _ in range(15):
        send_request(TARGET+random.choice(normal_paths))
    for path in paths:
        send_request(TARGET+path)
    for _ in range(120):
        send_request(TARGET+random.choice(paths+normal_paths))
    print("Scan simulation finished")

if __name__=="__main__":
    run_scan()