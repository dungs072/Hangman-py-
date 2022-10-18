import random
class Quizz:
    def __init__(self,title:str) -> None:
        self.answers = []
        self.selected_answers = []
        self.title = title
        
    def add_answer(self,answer:str):
        self.answers.append(answer)
    
    def get_answer(self)->str:  
        choice = '-1'
        while(choice in self.selected_answers and len(self.answers)!=len(self.selected_answers)):
            choice = random.choice(self.answers)
        if choice!='-1':
            self.selected_answers.append(choice)
        return choice
    