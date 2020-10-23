# SprayBot
Selenium password spraying script.

Fully-automated browser-driven password sprayer that accepts element Xpaths for keyboard-only spraying.

## Requirements
* Windows\Linux\Mac (Designed to be in a VM, tested in Windows but should work for any distro with python3+chrome)
    - Having SprayBot run in a VM allows you to launch and then `HotKey` out of the VM to let SprayBot do its thing while you do your own thing. 
* Python3
* Selenium
* Chrome + its corresponding [WebDriver version](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* Proxy (Burp)
    - Hard to discern if a credential was successful or not for different web apps, best to filter for that in burp yourself

## Keyboard Only
Inspect each `username`, `password`, and `submit` button boxes of the web app to copy its XPATH into a file before running the bot ((XPATH is case sensitive):
- `//*[@id="username"]`
- `//*[@id="password"]`
- `/html/body/div/main/div/div/div/div[2]/div[1]/div[3]/div/form/div[4]/button`

SprayBot will take the above as separate inputs to perform a faster web browser driven spray. Can put into a file and load instead of inputting to command line (in the same order as the above example for each line: username, password, submit boxes)


# Install
## Python
```
pip3 install -r requirements.txt
```
## Chromedriver.exe for Selenium
Either move the `chromedriver.exe` that you downloaded for Selenium to your Google-Chrome main directory or just modify the PATH variable and uncomment/comment at the top of the script under `create_driver()` function:
```
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--incognito")
                chrome_options.add_argument('ignore-certificate-errors')
                chrome_options.add_argument("--window-size="+resolution)
Uncomment -->  # PATH = "C:\\Users\\user\\pathto\\chromedriver.exe"
Uncomment -->  # chrome_driver = webdriver.Chrome(executable_path=PATH,options=chrome_options,desired_capabilities=capability)
  Comment -->   chrome_driver = webdriver.Chrome(options=chrome_options,desired_capabilities=capability)
                return chrome_driver
```


SprayBot takes a `resolution`, `delay` and `pause` option as well if needed. `Delay` is the initial wait on page load AND login submit. `Pause` is for each action AFTER the initial page load.
```
usage: spraybot.py -t {URL} -p {PROXY} -u {PATHTOUSERSFILE} --password {PASSWORD}


            A Selenium password spraying script that accepts XPATHs as input (cmdline or from file).

            Example usage:  .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020!
                            .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020! -f xpathfile.txt
                            .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020! -r 1920,1080
                            .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020! -d 5 -s 2 -f xpathfile.txt

            Review README.md


optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -t URL, --url URL     Target URL (https://example.com/signin)
  -p PROXY, --proxy PROXY
                        Proxy IP:PORT (127.0.0.1:8080)
  -u USERS, --users USERS
                        List of users file to spray with
  --password PASSWORD   Password to spray with

optional arguments:
  -r RESOLUTION, --resolution RESOLUTION
                        Specify resolution (1920,1080), (DEFAULT:1200,1080)
  -d DELAY, --delay DELAY
                        Seeded DELAY between initial request & SprayBot's first instruction (DEFAULT:5)
  -s PAUSE, --pause PAUSE
                        Seeded PAUSE between SprayBot's keypresses (DEFAULT:1)
  -f FILE, --file FILE  Read XPATHs from file instead of inputing to prompt
```

