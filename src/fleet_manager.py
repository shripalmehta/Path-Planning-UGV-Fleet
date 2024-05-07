from openrouteservice.optimization import Vehicle, Job

class FleetManager:
    def __init__(self, bot_count, start):
        self.id = id
        self.start = start
        self.bot_capacity = 1000
        self.bot_count = 0
        self.bots = self.create_bots(bot_count)

    def create_bots(self, n):
        bots = []
        for i in range(n):
            bots.append(self.create_bot(id=i))
        return bots

    def create_bot(self, id):
        # TODO add bot features - capacity, skills, etc.
        b = Vehicle(id=id, 
                    start=list(reversed(self.start)),
                    end=list(reversed(self.start)),
                    capacity=[self.bot_capacity]) # payload capacity = material in kg
        self.bot_count += 1
        return b

    def destroy_bot(self, id):
        for bot in self.bots:
            if bot.id == id:
                self.bots.remove(bot)
                self.bot_count -= 1
                
    def get_bot_count(self):
        return self.bot_count

    pass
