from openrouteservice.optimization import Vehicle, Job

class FleetManager:
    def __init__(self, bot_count, start):
        self.id = id
        self.start = start
        self.bot_count = 0
        self.bots = self.create_bots(bot_count)

    skill_dig = 500
    [skill_dig, skill_roll]

    def create_bots(self, n):
        bots = []
        for i in range(n):
            bots.append(self.create_bot(id=i))
        return bots

    def create_bot(self, id):
        # TODO add bot features - capacity, skills, etc.
        b = Vehicle(id=id, 
                    start=list(reversed(self.start)),
                    capacity=[500]) # capacity = material in kg
        self.bot_count += 1
        return b

    def destroy_bot(self, id):
        for bot in self.bots:
            if bot.id == id:
                self.bots.remove(bot)
                self.bot_count -= 1
                # logger.INFO('bot with id =', id, 'removed')

    def get_bot_count(self):
        return self.bot_count

    pass