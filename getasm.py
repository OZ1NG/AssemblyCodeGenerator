import os

class Getasm():
    __GRAMMER_TYPE_LIST = ['intel', 'at']
    
    def __init__(self, func_name:str, file_path:str, asm_grammer:str = 'intel'):
        self.func_name = func_name
        self.file_path = file_path
        if (asm_grammer not in self.__GRAMMER_TYPE_LIST):
            raise ValueError (f"{asm_grammer} is not variable type. Only {self.__GRAMMER_TYPE_LIST}")    
        self.asm_grammer = asm_grammer
        
    def getasm(self) -> str:
        cmd = ['objdump', '-d', f'-M {self.asm_grammer}', self.file_path, f"| awk -v RS= '/<{self.func_name}>:/'"]
        res = os.popen(' '.join(cmd)).read()
        return res
        
if __name__ == '__main__':
    # res = Getasm('calc_func', './result', asm_grammer='at').getasm()
    res = Getasm('calc_func', './result').getasm()
    print(res)
