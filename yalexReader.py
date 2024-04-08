from reader import reader
from Simulator import *
from preAFD import import_module
from typing import *


class YalexReader:
    def __init__(self, file_path:str):
        self.content:str = reader(file_path)

    def analizeFile(self):

        def decAnalyzer(message:str):
            dec:List[str] = message.split('=',1)
            if len(dec) != 2:
                raise Exception(f'Error in variable declaration `{message}`')
            name:str = dec[0].replace('let','',1).strip()
            expression:str = dec[1].strip()
            
        
        def tokAnalyzer(message:str):
            pass
        
        def RLAnalyzer(message:str):
            pass
        
        machine = import_module('machine.plk', {
            'comments': ['\(\*[^()]+\*\)'],
            'declarations': ['let +[a-z]+ *= *\n*([^ \n\t]|\'[^\']\'|"[^"]+")+'],
            'tokens': ['(\| +)?([^ \n\t]|\'[^\']\'|"[^"]+")+( +\{ *return +[A-Z]+ *\})?'],
            'RL': ['rule +[a-z]+ *=']
            })
        
        analysis = exclusiveSim(machine, self.content)
        
        inRules = True
        
        for message, token in analysis:
            if token == 'comments':
                continue
            elif token == 'declarations':
                inRules = False
                decAnalyzer(message)
            elif token == 'tokens':
                if not inRules:
                    raise Exception('Rules not declarated in first place.')
                tokAnalyzer(message)
            elif token == 'RL':
                inRules = True
                RLAnalyzer(message)
        
             