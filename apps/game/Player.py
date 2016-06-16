print "Player.py file Reached"
import Fighter
class Player(Fighter.Fighter):

    def __init__(self):
        print "Player Character initialized---------"

    def onCreate(self,x,y):
    	Fighter.Fighter.onCreate(self,x,y)
        self.health = 100
        return False

    def onDeath(self):
        return False