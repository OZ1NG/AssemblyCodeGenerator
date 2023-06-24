import gencode
import getasm
import time
import os
import colorama
import math
import signal
import sys
import argparse

def print_red(msg:str):
    print(colorama.Fore.RED + msg + colorama.Fore.WHITE)
    
def print_blue(msg:str):
    print(colorama.Fore.BLUE + msg + colorama.Fore.WHITE)

TIMEOUT = 300
START_TIME = None

def timeout(a, b):
    print_red(f"\n[!] TIMEOUT!")
    exit(0)

class Asm_quiz():
    def __init__(self, level:int, arch:str='x64', timeout_sec:int=300, debug=False, use_template_flag=True):
        """클래스 변수 초기화

        Args:
            level (int): 난이도 선택
            arch (str, optional): 아키택쳐 선택. Defaults to 'x64'.
            time_sec (int, optional): 타임아웃 시간. Defaults to 300.
            debug (bool, optional): 디버깅 플래그. Defaults to False.
            use_template_flag (bool, optional): Defaults to True.
                - True : 완전 랜덤 생성 코드 사용.
                - False: 어느정도 구성된 템플릿 코드 사용.
        """
        self.gencode = gencode.Gencode(level=level, arch=arch, use_template_flag=use_template_flag)
        self.time_sec = timeout_sec
        self.DEBUG = debug
    
    def run(self):
        global START_TIME
        if (not self.DEBUG):
            os.system('clear')
        
        answer = self.gencode.run()
        asm_code = getasm.Getasm('calc_func', './result').getasm()
        # print(hex(answer))
        
        START_TIME = time.time()
        # to = threading.Thread(target=timeout)
        # to.start()
        
        signal.signal(signalnum=signal.SIGALRM, handler=timeout)
        signal.alarm(self.time_sec)
        
        while(1):
            print(asm_code)
            try:
                user_answer = int(input("Answer (hex) > "), 16)
            except (KeyboardInterrupt, TimeoutError):
                print("")
                break
            except Exception as e:
                print(e)
                print_red("[!] Wrong input")
                time.sleep(1)
                # os.system('clear')
                continue
            
            if user_answer == answer:
                print_blue(f"[O] congratulations!")
                break
            else:
                print_red(f"[!] Wrong! Try Again...")
                time.sleep(1)
                os.system('clear')
                

        # 맞추는데 걸린 소요 시간 출력
        consumed_time = time.time() - START_TIME
        minutes, seconds = divmod(consumed_time, 60)
        print(f'소요시간: {int(minutes)}분 {math.trunc(seconds)}초')
 

def parse_argv():
    parser = argparse.ArgumentParser(description='Process some integers.')

    # 인자 추가
    parser.add_argument('--level', type=int, choices=range(3), help='an integer for the level (0~2)')
    parser.add_argument('--use_template_flag', action='store_true', help='a flag for using template')

    args = parser.parse_args()

    if args.level is None and args.use_template_flag is False:
        parser.error('Either --level or --use_template_flag must be provided.')

    if (args.level == None):
        args.level = 0
    return args.level, args.use_template_flag
    
if __name__ == '__main__':
    level, use_template_flag = parse_argv()
    
    aq = Asm_quiz(level=level, use_template_flag=use_template_flag, timeout_sec=300)
    while(1):
        try:
            aq.run()
        except ValueError:
            continue
        break
