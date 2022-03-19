# findBirthday
자가진단으로 생일 찾기

## 유의 사항
 - 따로 날짜를 입력하지 않았을 경우, 찾기 시작하는 날짜는 1960년 01월 01일입니다.
 - 생년, 생월, 생일 중 모르는 부분은 0, False 등으로 처리합니다. None은 실행되지 않습니다.
 - 충청남도교육청 소속 학교만 찾을 수 있습니다.(예: 부성초등학교, 서일중학교, 서일고등학교···)
 - **이 프로그램을 사용함으로써 발생하는 책임은 전적으로 프로그램을 실행하는 사용자에게 있습니다.**
 <details markdown="1">
 <summary>학교급 펼치기 · 접기</summary>
  - 1: 유치원
  - 2: 초등학교
  - 3: 중학교
  - 4: 고등학교
  - 5: 특수학교
 </details>

## findBirthday 사용법
 `yy, mm, dd`을 모를 경우 `0`이나 `False` 또는 `None` 등으로 놓으면 기본으로 `1960, 1, 1`로 들어갑니다.

 - find(기본형)
    ```python
    findBirthday.find(name, yy=None, mm=None, dd=None, sName='서일중학교', level=3, ey=False)
    ```
    | 인자  | 내용(타입) | 예시 |
    | ----- | ---------- | ---- |
    | `name` | 찾을 이름(str) | `'홍길동'` |
    | `yy` | 생년(int 또는 str) | `1960` 또는 `'1960'` |
    | `mm` | 생월(int 또는 str) | `1` 또는 `'1'` |
    | `dd` | 생일(int 또는 str) | `1` 또는 `'1'` |
    | `sName` | 학교 이름(str) | `'서일중학교'` |
    | `level` | 학교급(int 또는 str) | `1` 또는 `'1'` |
    | `ey` | 검색 중단 연도(int 또는 str) | `2000` 또는 `'2000'` |

 - multiFind(다중형)
    ```python
    findBirthday.multiFind(nameList, *args, **kwargs)
    ```
    | 인자 | 내용(타입) | 예시 |
    | ---- | ---------- | ---- |
    | `nameList` | 찾을 이름 목록(list 또는 tuple) | `['홍길동', '홍길순']` 또는 `['홍길동', '홍길순']` |
    | `*args` | `findBirthday.find`에 들어갈 인자 |  |
    | `**kwargs` | `findBirthday.find`에 들어갈 인자 |  |

## support 사용법
 - 기본형
    - `support` `findBirthday.find 인자`
 - 다중형
    - `support` `multi` `findBirthday.multifind 인자`
 - 주의사항
    - 띄어쓰기가 포함될 경우 큰따옴표(")로 감싸야 합니다.
    - 파이썬 파일이지만 명령 프롬프트 등에서 직접 실행해야 합니다.
    - 다중형을 쓸 경우 nameList 인자에 `"['홍길동', '홍길순']"`의 형태로 입력해야 합니다. 