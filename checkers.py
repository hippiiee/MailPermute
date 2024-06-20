import aiosmtplib
import asyncio
from bs4 import BeautifulSoup
import dns.resolver
import random
import re
import requests
import string as s
from typing import Dict

uaLst = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
]

async def code250(mailProvider, target, timeout=10):
    providerLst = []
    error = ''

    randPref = ''.join(random.sample(s.ascii_lowercase, 6))
    fromAddress = f"{randPref}@{mailProvider}"
    targetMail = f"{target}@{mailProvider}"

    records = dns.resolver.Resolver().resolve(mailProvider, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    try:
        server = aiosmtplib.SMTP(timeout=timeout, validate_certs=False)

        await server.connect(hostname=mxRecord)
        await server.helo()
        await server.mail(fromAddress)
        code, message = await server.rcpt(targetMail)

        if code == 250:
            providerLst.append(targetMail)

        message_str = message.lower()
        if 'ban' in message_str or 'denied' in message_str:
            error = message_str

    except aiosmtplib.errors.SMTPRecipientRefused:
        pass
    except Exception as e:
        error = str(e)
    finally:
        await server.quit()

    return providerLst, error

async def duckduckgo(target, req_session_fun, *args, **kwargs) -> Dict:
    result = {}
    error = ""

    duckURL = "https://quack.duckduckgo.com/api/auth/signup"

    headers = {"User-Agent": random.choice(uaLst), "Origin": "https://duckduckgo.com", "Sec-Fetch-Dest": "empty",
               "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers", "Referer": "https://duckduckgo.com/"}

    data = {
        "code": (None, "01337"),
        "user": (None, target),
        "email": (None, "mail@example.com")

    }

    try:
        checkDuck = await req_session_fun.post(duckURL, headers=headers, data=data, timeout=kwargs.get('timeout', 5))

        resp = await checkDuck.text()
        if "unavailable_username" in resp:
            result["Duckduckgo"] = f"{target}@duck.com"

    except Exception as e:
        error = str(e)

    return result, error

async def gmail(target, req_session_fun, *args, **kwargs) -> Dict:
    result = {}
    gmailChkLst, error = await code250("gmail.com", target, kwargs.get('timeout', 10))
    if gmailChkLst:
        result["Gmail"] = gmailChkLst[0]

    await asyncio.sleep(0)
    return result, error

async def yahoo(target, req_session_fun, *args, **kwargs) -> Dict:
    result = {}
    error = ""

    # get AS cookie, acrumb & sessionIndex value
    url = "https://login.yahoo.com/account/create"
    response = requests.get(url)
    if response.status_code == 200:
        headers = response.headers
        set_cookie_header = headers.get('set-cookie', '')
        match = re.search(r'AS=([^;]+)', set_cookie_header)
        if match:
            as_value = match.group(1)
        soup = BeautifulSoup(response.content, 'html.parser')
        acrumb_value = soup.find('input', {'name': 'acrumb'})['value']
        session_index_value = soup.find('input', {'name': 'sessionIndex'})['value']

    else:
        error = "Error yahoo while getting header cookie", str(response.status_code)

    yahooURL = "https://login.yahoo.com/account/module/create?validateField=userId"
    yahooCookies = {"AS": as_value}
    headers = {"User-Agent": random.choice(uaLst),
               "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
               "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest",
               "DNT": "1", "Connection": "close"}

    yahooPOST = {"acrumb": acrumb_value, "sessionIndex": session_index_value, "userId": target}

    try:
        yahooChk = await req_session_fun.post(yahooURL, headers=headers, cookies=yahooCookies, data=yahooPOST, timeout=kwargs.get('timeout', 10))

        body = await yahooChk.text()
        if '"IDENTIFIER_EXISTS"' in body:
            result["Yahoo"] = f"{target}@yahoo.com"

    except Exception as e:
        error = str(e)

    return result, error


async def yandex(target, req_session_fun, *args, **kwargs) -> Dict:
    result = {}
    yaAliasesLst = ["yandex.by",
                    "yandex.kz",
                    "yandex.ua",
                    "yandex.com",
                    "ya.ru"]
    yaChkLst, error = await code250("yandex.ru", target, kwargs.get('timeout', 10))
    if yaChkLst:
        yaAliasesLst = [f'{target}@{yaAlias}' for yaAlias in yaAliasesLst]
        yaMails = list(set(yaChkLst + yaAliasesLst))
        result["Yandex"] = yaMails

    await asyncio.sleep(0)
    return result, error
