from typing import Dict
import random
import string as s
import dns.resolver
import aiosmtplib
import asyncio

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

async def gmail(target, req_session_fun, *args, **kwargs) -> Dict:
    result = {}
    gmailChkLst, error = await code250("gmail.com", target, kwargs.get('timeout', 10))
    if gmailChkLst:
        result["Gmail"] = gmailChkLst[0]

    await asyncio.sleep(0)
    return result, error

async def yahoo(target, req_session_fun, *args, **kwargs) -> Dict:
    result = {}
    error = ''

    yahooURL = "https://login.yahoo.com/account/module/create?validateField=userId"
    yahooCookies = {"AS": "v=1&s=AUeQM4bw&d=A6671ad9b|1ZGFUp3.2SoMaxdWYxbWRvFgae0EJkV2RE1Zh15A9Dk8OqO06kKdHBqlp5rJqwXaVQ4lu3M5TNOwnbvoCpEA3LVh7jxqo0tsE_fG8VToaWYwCBHZRosEiBp9z8t3G6vyTwguhQtzskCizS3tuzsAJMHrfqXVTKHJzqklfNrw.qvWLQAD_LmaSHfNzL3oenzORJxBK6bpEcRp13OhOcIg50Nw8jMtDJDeYzDJO58Q23hYrUEs2tYNp2Hwsr7m4jz.1r4ut29TlUQqO3J4YcdqsEPE6d5i22FD6Taxq.cr6vStRktze71NsZK5mGWTqvtTXLZvlYul.N2GTjDHwhSZPMHZz6oRYLzDpFEob.HDHxFRfz_zRQ7hRm38n1DBlrZ.UTvZPSYAZ_mKbmlK.k844Pg1zPsSsAO2J5Nr2bqMoXgpJ1SfcaMPa5UANzcewLW_Uw98GZ15chq0OByN2F3Hfdi8Dfg6MROaUIVU4aviTZ_BHkTTS4ZlnWalDCqjpigRxOGLS70NmnTRJzV7CDjPCjFXMaG06RtHVVXdSrE9H5xlGk5AsOttMwqypI0X280715oaTHIyRpJ.h0z4xclTLVX_pQG9t2otAHX8PZVl4V5nyY8FrJ5SwnZXav_4jqXbz4Ykqy03KoH5lj7wSJxB4EawphFO9ZSBqGil4.O.IO_XDp6s5BBbo11oJ4.bKZnWamYNt6Y0IgWLDcGDSe1S0vjXs3_NMLffIBkX_cGAnZ4acQqXGnbJK3pSbz4kwSRPB_sNfL5QWqeMwfuQByr8qNBOIizQZaFZdeVaDbqMIDQX8F2A3wUqslcoDRw_mOOxTjq8qtt0FdZGbHStNGqqSS0e~A|B6671ad9f|KMhhmJf.2Trlmcu3m7PbuKGc1enAEmiEOciWXqlkG5JyGbVVFVYbry_C6g39Ykc2CwmL4sIS9qotZzujd2_oMi6lD0Hp4vG0ezjdrTRmFRb7Zra1ihn9q3.Dr.v0_tJyscol1E1K374Mc9Ha6qHp2aPv4J6wApZtBWIA1eEMmB3SRNSQ1fHlMPko_b9Mm8UHTIZgwaU7zzHHu.qBx2I2TY85ywG6INEtaWkfoajFhuNNAIUq9KaR4I4RJM8jYjVhtp0ttaC02VkwXs_14c8QxWeRuWK1n_GGipM90REp1TgJYdL0kX2ha_r70Qzgw4ZxP90vBQxlXAIqyV_3xaqS_GnNdM4vauv.J8.kAeymggUE44SC_nIl3qOJM4CEQii8PH.sB9TFopbl8bafWgvy7W4CRyLlGvh1TeVnzpEktNp1.khnsr40adtULNA7IPSxUBbpZqxZUbHfK9r4EpIbyDJhMLZigJLlz9LfDZMKAwkhkgXSD7OAqQKZEYOwCJ2ZQePNneyFOswdWb.2uu.56GIi7mFOSFN1oTLIbQPJBhR94veVh8vypjkGVTdYA_UCkox05N.TcxrNNjccwI1bQ4kzBMVTpTTYSL9PGdhwiT4oTuFG3jIzukUPTh5T8Gzvn3PHfj.UASxfCs9MFkk7WBnXPzjQdbTM9INMKbnlTwFfwIlFUo4ypTgTJpLlEbkbzgJZjpVocDyTXmGUJL9XimdR7wrRBSrUKe9YH9ZDy8o0VmiKuoUUHKreQL1IF5D.M0WgmlEn0ha45gAKrYMeAfXM6n.O4.H_.sa.Vu0CaCGfS1nxzEmW04gdnoduaRReA0xzW4.FsLZBzKNKSFMqiSnIURjmast5sH1KtRHTJP9NU8YUBKUlb99PjwhG_.CIP01XReuH0T1lFGY.hHB0F1SZTDtFfI1inF3285qUHM7KeR7PI6cxxyAS64YonYaP8jbNt.YHI1HC.kHe.HasduhzuWSENVg0Euys~A"}
    headers = {"User-Agent": random.choice(uaLst),
               "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
               "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest",
               "DNT": "1", "Connection": "close"}

    yahooPOST = {"acrumb": "AUeQM4bw", "sessionIndex": "Qg--", "userId": target}

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
