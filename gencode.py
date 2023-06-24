import random
import os

class Gencode():
    __ARCH_LIST = ['x64','x86']
    __TEMPLATE_DIR_PATH = './template'
    
    __OPERATOR_LIST = ['+=', '-=', '*=', '/=', '%=', '^=', '|=']
    
    __MAX_LOOP_COUNT = 5 # 최대 루프 횟수
    __MIN_LOOP_COUNT = 1 # 최소 루프 횟수
    
    __MAX_LOOP_NUM = 3 # 최대 루프문 개수
    __MIN_LOOP_NUM = 0 # 최소 루프문 개수
    
    __MAX_CODE_LINE = 15
    __MAX_LOOP_CODE_LINE = 5
    
    MAX_VALUES_COUNT = 3
    MIN_VALUES_COUNT = 1
    
    def __init__(self, level=2, arch='x64', use_template_flag=False, template_dir_path='./template', template_file_name='template_sample2.c'):
        """__init__: set parameters

        Args:
            level (int, optional): Defaults to 2. 
              level 0 : Easy
              level 1 : Middle
              level 2 : Hard
            arch (str, optional): Defaults to 'x64'. : 'x64', 'x86'
            use_template_flag (boolean, optional): 기존에 존재하는 템플릿을 사용할지 안할지 설정하는 플래그
            template_path (str, optional): 템플릿 파일들 경로
        """
        self.level = level
        if (self.level < 0 and self.level > 2):
            raise KeyError (f"[!] Wrong level. 0 < level < 2")
        
        self.arch = arch.lower()
        if (self.arch not in self.__ARCH_LIST):
            raise KeyError (f"[!] Wrong Architecture. You can only {self.__ARCH_LIST}")
        
        self.use_template_flag = use_template_flag
        self.template_dir_path = template_dir_path
        self.template_file_name = template_file_name

    def __get_template(self):
        filepath = self.template_dir_path
        templates_path = ''
        if (self.use_template_flag):
            templates = self.template_file_name
            templates_path = os.path.join(filepath, templates)
        else:
            if self.level == 0:
                filepath = os.path.join(self.__TEMPLATE_DIR_PATH, 'low')
            elif self.level == 1:
                filepath = os.path.join(self.__TEMPLATE_DIR_PATH, 'medium')
            elif self.level == 2:
                filepath = os.path.join(self.__TEMPLATE_DIR_PATH, 'high')

            templates = random.choice(os.listdir(filepath))
            templates_path = os.path.join(filepath, templates)
        
        with open(templates_path, 'r') as fp:
            template_data = fp.read()
        
        return template_data
        
    def __gen_loop_codes(self, value_type_dict:dict) -> str:
        """loop문을 생성하는 코드

        Args:
            value_type_dict (dict): _description_

        Returns:
            list[str]: _description_
        """
        
        # 루프문 생성하기
        loop_tempalte = """
    for (int i = 0; i < {{loop_count}}; i++) {
{{loop_code}}
    }
""" 
        
        # 루프 횟수 정하기
        loop_count = random.randrange(self.__MIN_LOOP_COUNT, self.__MAX_LOOP_COUNT + 1)
        # print(f'loop_count:{loop_count}')
        loop_tempalte = loop_tempalte.replace('{{loop_count}}', str(loop_count))
        # print('[debug]', loop_tempalte)
        
        # 몇줄의 코드를 생성할 것인지 정하기
        total_code_line = random.randrange(0, self.__MAX_LOOP_CODE_LINE + 1)
        
        code = []
        for i in range(total_code_line):
            code.append(self.__gen_code_one_line(value_type_dict))
        
        loop_tempalte = loop_tempalte.replace('{{loop_code}}', ''.join(code))
        
        return loop_tempalte, total_code_line
        
        
    def __gen_code_one_line(self, value_type_dict:dict) -> str:
        # 연산 코드 format
        calc_code_format_dict = {
            0:'\t{operand_0} {operator} ({operand_0_type}) {operand_1};\n',  # 변수와 변수를 연산하는 것
            1:'\t{operand_0} {operator} {operand_1};\n' # 변수와 숫자를 연산하는 것
        }

        # 루프문 내의 연산 코드 생성하기
        operand_0 = random.choice(list(value_type_dict.keys()))
        operator = random.choice(self.__OPERATOR_LIST)
        operand_1 = random.choice(list(value_type_dict.keys()))
        ## 어떤 포멧을 사용할 건지 고르기
        # calc_code_format_num = random.choice(list(calc_code_format_dict.keys()))
        if (value_type_dict[operand_0] != value_type_dict[operand_1]):
            calc_code_format_num = 0
        else:
            calc_code_format_num = 1
        
        ## 포멧의 맞춰 코드 생성하기
        calc_code_format = calc_code_format_dict[calc_code_format_num]
        if (calc_code_format_num == 0):
            calc_code = calc_code_format.format(operand_0=operand_0, operator=operator, operand_0_type=value_type_dict[operand_0] ,operand_1=operand_1)
        elif(calc_code_format_num == 1):
            calc_code = calc_code_format.format(operand_0=operand_0, operator=operator, operand_1=operand_1)
            
        return calc_code
        
    def __create_code(self):
        code = []
        
        # 변수 개수 정하기
        value_count = random.randrange(self.MIN_VALUES_COUNT, self.MAX_VALUES_COUNT + 1)
        
        # 루프문 개수 정하기
        loop_count = random.randrange(self.__MIN_LOOP_NUM, self.__MAX_LOOP_NUM + 1)
        
        # 변수 생성
        value_code_list = []
        value_type_dict = {}
        for i in range(value_count):
            ## 변수 타입 정하기
            value_type, max_range = self.__set_value_type()
            value_code_list.append(f"\t{value_type} v_{i} = {hex(random.randrange(0, max_range + 1))};")
            value_type_dict[f'v_{i}'] = value_type
        
        # 몇줄의 연산 코드를 생성할 것인지 정하기
        total_code_line = random.randrange(0, self.__MAX_CODE_LINE + 1)
        
        # 루프 코드 생성
        for i in range(loop_count):
            loop_code, lines = self.__gen_loop_codes(value_type_dict)
            code.append(loop_code)
            total_code_line -= lines
            if (total_code_line <= 0):
                total_code_line = 0
                break
            
        # 일반 연산코드 생성
        for i in range(total_code_line):
            code.append(self.__gen_code_one_line(value_type_dict))
        
        # code 배치 변경
        code = random.sample(code, len(code))
        
        # code에 변수 추가하기
        value_code_list += code
        code = value_code_list
        
        return '\n'.join(code)
            
    def __set_value_type(self) -> tuple[str:int]:
        """변수의 타입을 설정하는 함수

        Returns:
            tuple [str:int] : (type, max_range)
            - type (str) : 변수의 타입
            - max_range : 변수가 가질 수 있는 최대 크기
        """
        # 변수 타입 정하기
        type_prefix = 'uint{size}_t'
        type = type_prefix.format(size=random.choice(['8', '16', '32', '64']))
        max_range = 0
        if (type == 'uint8_t'):
            max_range = 0xff
        elif (type == 'uint16_t'):
            max_range = 0xffff
        elif (type == 'uint32_t'):
            max_range = 0xffffffff
        elif (type == 'uint64_t'):
            max_range = 0xffffffffffffffff
        
        return type, max_range
    
    def gen_code(self):
        template_data = self.__get_template()
        
        value_name_prefix = 'v_'
        if (self.use_template_flag):        
            # result 변수 return_type 설정하기
            return_type, max_range = self.__set_value_type()    
            ## result 변수 return type 설정하기
            template_data = template_data.replace('{{return_type}}', return_type)
            ## reusult 변수 초기값 설정하기
            template_data = template_data.replace('{{init_0}}', hex(random.randrange(0, max_range + 1)))
            # 코드 생성하기
            template_data = template_data.replace('{{code}}', self.__create_code())
        else:
            # reusult 변수 초기값 설정하기
            template_data = template_data.replace('{{init_0}}', hex(random.randrange(0, 0xffffffff + 1)))
        
            # 변수 개수 파악하기
            value_count = template_data.count(value_name_prefix)
        
            # 변수 타입 정하기
            type_prefix = 'uint{size}_t'
            for i in range(0, value_count):
                type = type_prefix.format(size=random.choice(['8', '16', '32', '64']))
                max_range = 0
                if (type == 'uint8_t'):
                    max_range = 0xff + 1
                elif (type == 'uint16_t'):
                    max_range = 0xffff + 1
                elif (type == 'uint32_t'):
                    max_range = 0xffffffff + 1
                elif (type == 'uint64_t'):
                    max_range = 0xffffffffffffffff + 1

                template_data = template_data.replace(f'{{{{{value_name_prefix}{i}}}}}' ,f'{type} {value_name_prefix}{i} = {hex(random.randrange(0, max_range))}')

            # 루프 개수 파악하기
            loop_name_prefix = 'loop_count_'
            loop_count = template_data.count(loop_name_prefix)

            # 루프 횟수 정하기
            for i in range(loop_count):
                template_data = template_data.replace(f'{{{{{loop_name_prefix}{i}}}}}', hex(random.randrange(self.__MIN_LOOP_COUNT, self.__MAX_LOOP_COUNT)))
        
        return template_data

    def save_result_code(self, code_data:str, src_path:str='./',src_name:str='result.c'):
        with open(os.path.join(src_path, src_name), 'w') as fp:
            fp.write(code_data)
    
    def compile_and_run_result_code(self, src_path:str='./',src_name:str='result.c', output_name:str='result') -> int:
        """완성된 코드를 컴파일하고 실행하여 답을 얻어내는 함수

        Args:
            src_path (str, optional): _description_. Defaults to './'.
            src_name (str, optional): _description_. Defaults to 'result.c'.
            output_name (str, optional): _description_. Defaults to 'result'.

        Returns:
            int: answer
        """
        cmd = ['gcc', '-O0',os.path.join(src_path, src_name), f'-o {output_name}']
        if self.arch == 'x86':
            cmd.append('-m32')
        res = os.popen(' '.join(cmd)).read()
        # print("res:", res)
        
        cmd = ['./result']
        answer = os.popen(' '.join(cmd)).read()
        if ('Floating point exception' in answer):
            raise ValueError('Floating point exception')
        answer = int(answer, 16)
        # print("answer:", answer)
        return answer

    def save_answer(self, answer:int, src_path:str='./',src_name:str='answer.txt'):
        with open(os.path.join(src_path, src_name), 'w') as fp:
            fp.write(hex(answer)+'\n')

    def run(self):
        src_code = self.gen_code()
        self.save_result_code(src_code)
        answer = self.compile_and_run_result_code()
        self.save_answer(answer)
        return answer

if __name__ == '__main__':
    gc = Gencode(level=1)
    src_code = gc.gen_code()
    gc.save_result_code(src_code)
    answer = gc.compile_and_run_result_code()
    # print("answer:", answer)
