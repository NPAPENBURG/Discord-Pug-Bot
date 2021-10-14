class Player:

    def __init__(self, name, elo, win, loss, discord_id, currentmatch):
        self.elo = elo
        self.name = name
        self.win = win
        self.loss = loss
        self.discord_id = discord_id
        self.currentmatch = currentmatch

