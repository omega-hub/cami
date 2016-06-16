print "Player.py file Reached"
import Fighter
class Saucer(Fighter.Fighter):

    def __init__(self):
        print "Saucer Spawned"

    def onCreate(self,x,y):
        Fighter.Fighter.create(self,x,y)
        self.health = 100
        return False

    def onDeath(self):
        return False