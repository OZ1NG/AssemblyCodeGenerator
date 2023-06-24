# Assembly Generator

## 방식
1. 랜덤한 연산을 하는 C 코드를 작성
2. 컴파일
3. 실행 (결과값 확인)

## 사용법
### 실행
```bash
$ python3 main.py
usage: main.py [-h] [--level {0,1,2}] [--use_template_flag]
main.py: error: Either --level or --use_template_flag must be provided.
```
- 아래의 두 인자중 하나는 무조건 들어가야한다.
- `--level` : 난이도 설정 (0 ~ 2)
    - ./template 디렉토리에 존재하는 난이도별 템플릿 사용
- `--use_template_flag` : 완전 랜덤 코드 생성

### requirements.txt
```bash
$ python3 -m pip install -r requirements.txt

# or 

$ pip3 install colorma
```

### 난이도 조절 및 템플릿 선택 규칙
- 완전 랜덤 코드 생성 시 다음과 같이 코드 수정 (디폴트)
```python
# main.py
aq = Asm_quiz(level=<0~2 아무 값이던 상관 없음>, use_template_flag=False)
```

- 임의 템플릿 사용하여 랜덤한 값만 생성하기 원하는 경우 다음과 같이 코드 수정
```python
# main.py
aq = Asm_quiz(level=<0~2>, use_template_flag=True)
```
- ./template 경로에 템플릿 파일이 존재해야 함.
    - 임의 템플릿 코드를 사용하고자 한다면, 난이도 별로 다음의 경로 밑에 임의 템플리 코드를 저장 할 것
        > 이곳에 저장된 임의 템플릿 코드는 난이도에 맞춰 랜덤으로 선택됨.
        - low 난이도: `./template/low/<your template>`
        - medium 난이도: `./template/medium/<your template>`
        - high 난이도: `./template/high/<your template>`
    - 완전 랜덤 코드 생성을 하고자 한다면, 다음의 경로 밑에 다음의 이름으로 템플릿을 작성해주어야함.
        - `./template/template_sample2.c`

## 값 조절 
### main.py
- level: 난이도
    > 임의 템플릿 코드를 사용하여 값만 변경하기 원하는 경우에만 의미 있음
    - level=0 : low 난이도 템플릿 중 선택
    - level=1 : medium 난이도 템플릿 중 선택
    - level=2 : high 난이도 템플릿 중 선택

### gencode.py
- `__MAX_LOOP_COUNT` : 최대 루프 횟수 # default=5
- `__MIN_LOOP_COUNT` : 최소 루프 횟수 # default=1
- `__MAX_LOOP_NUM` : 최대 루프문 개수 # default=3
- `__MIN_LOOP_NUM` : 최소 루프문 개수 # default=0
- `__MAX_CODE_LINE` : 최대 연산 코드 개수(전체) # default=15
    - 루프문이 존재하는 경우 코드 길이가 몇줄 정도 더 나올 수 있음
- `__MAX_LOOP_CODE_LINE` : 최대 연산 코드 개수(각각의 루프문) = 5
- `MAX_VALUES_COUNT` : 최대 변수 개수(result 변수 제외) # default=3 
- `MIN_VALUES_COUNT` : 최소 변수 개수(result 변수 제외) # default=1

## 템플릿 작성 규칙
> 다음의 문자열을 포함하여 작성 할 것
- `{{return_type}}` : 함수의 리턴 타입 및 리턴할 변수의 타입
- `{{code}}` : `완전 랜덤 코드 생성`을 통해 코드를 생성하는 경우 생성된 코드가 들어갈 위치
- `{{init_0}}` : 이미 지정된 변수의 초기 값(랜덤 생성)
- `{{v_<num>}}` : 랜덤으로 생성할 변수의 이름
    - `<num>` : 0부터 시작할 것 ((e.g) v_0, v_1, v_2, ...)
- `{{loop_count_<num>}}` : 루프문의 루프 횟수(랜덤 생성)
