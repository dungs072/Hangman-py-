from quizz import Quizz
import random

class Quizz_manager:
    def __init__(self) -> None:
        self.dict_word = {}
        self.used_title = []
        self.__load_file()
        
    def __load_file(self):
        file = open('quizzes_text.txt')
        for line in file:
            infor = line.lstrip('-').split(':')
            values = infor[1].strip().split(', ')
            temp_quizz = Quizz(infor[0])
            for value in values:
                temp_quizz.add_answer(value)
            self.dict_word[infor[0]] = temp_quizz  
        file.close()
               
    def get_quizz(self):
        title = random.choice(list(self.dict_word))
        if self.__is_full_quizz(): return (None,None)
        while not self.dict_word[title].has_not_used_answer():
            title = random.choice(list(self.dict_word))
        self.used_title.append(title)
        return (title,self.dict_word[title].get_answer())
    
    def __is_full_quizz(self):
        for key in self.dict_word:
            if self.dict_word[key].has_not_used_answer():
                return False
        return True