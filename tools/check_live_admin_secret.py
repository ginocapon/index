#!/usr/bin/env python3
import re
import urllib.request

url = "https://righettoimmobiliare.it/admin.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
m = re.search(r"RIG_ADMIN_RLS_SECRET = '([^']+)'", html)
if not m:
    print("NOT FOUND")
else:
    s = m.group(1)
    print("placeholder:", "CAMBIA_QUESTO" in s)
    print("matches_repo:", s.startswith("sEwKPRkWMb"))
