
class Player():
    def __init__(self,coin) -> None:
        self.coin = coin
        
    def get_coin(self):
        return self.coin
    
    def add_coin(self, amount:int):
        self.coin+=amount