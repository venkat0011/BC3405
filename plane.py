from mesa import Model, Agent
from mesa.space import MultiGrid
import queue_method
import methods
import numpy as np


def baggage_normal():
    """ Generates a positive integer number from normal distribution """
    value = round(np.random.normal(1, 1), 0)
    while value < 0:
        value = round(np.random.normal(1, 1), 0)
    return value


class PassengerAgent(Agent):
    """ An agent with a fixed seat assigned """
    def __init__(self, unique_id, model, seat_pos, group):
        super().__init__(unique_id, model)
        self.seat_pos = seat_pos
        self.group = group
        self.state = 'INACTIVE'
        self.shuffle_dist = 0
        if self.model.shuffle_enable:
            self.shuffle = True
        else:
            self.shuffle = False

        if self.model.common_bags == 'normal':
            self.baggage = baggage_normal()
        else:
            self.baggage = self.model.common_bags

    def step(self):
        if self.state == 'GOING' and self.model.get_patch((self.pos[0] + 1, self.pos[1])).state == 'FREE' and self.model.get_patch((self.pos[0] + 1, self.pos[1])).shuffle == 0:
            if self.model.get_patch((self.pos[0] + 1, self.pos[1])).back == 0 or self.model.get_patch((self.pos[0] + 1, self.pos[1])).allow_shuffle is True:
                self.model.get_patch((self.pos[0] + 1, self.pos[1])).allow_shuffle = False
                self.move(1, 0)
                if self.shuffle:
                    if self.pos[0] + 1 == self.seat_pos[0]:
                        self.state = 'SHUFFLE CHECK'
                if self.pos[0] == self.seat_pos[0]:
                    if self.baggage > 0:
                        self.state = 'BAGGAGE'
                    else:
                        self.state = 'SEATING'

        elif self.state == 'SHUFFLE':
            if self.pos[1] == 4 and self.model.get_patch((self.pos[0] + 1, self.pos[1])).state == 'FREE':
                if self.pos[0] == self.seat_pos[0]:
                    self.shuffle_dist = self.model.get_patch((self.pos[0], self.pos[1])).shuffle
                    self.model.get_patch((self.pos[0], self.pos[1])).shuffle -= 1
                self.move(1, 0)
                self.shuffle_dist -= 1
                if self.shuffle_dist == 0:
                    self.state = 'BACK'
                    if self.pos[0] - self.seat_pos[0] == 2:
                        self.model.schedule.safe_remove_priority(self)
                        self.model.schedule.add_priority(self)
            else:
                if self.pos[1] > 4 and self.model.get_patch((self.pos[0], self.pos[1] - 1)).state == 'FREE':
                    self.move(0, -1)
                elif self.pos[1] < 4 and self.model.get_patch((self.pos[0], self.pos[1] + 1)).state == 'FREE':
                    self.move(0, 1)

        elif self.state == 'BACK' and self.model.get_patch((self.pos[0] - 1, self.pos[1])).state == 'FREE' and self.model.get_patch((self.pos[0] - 1, self.pos[1])).allow_shuffle is False:
            self.move(-1, 0)
            if self.pos[0] == self.seat_pos[0]:
                self.state = 'SEATING'
                self.model.get_patch((self.pos[0], self.pos[1])).back -= 1
                if self.model.get_patch((self.pos[0], self.pos[1])).back == 0:
                    self.model.get_patch((self.pos[0], self.pos[1])).ongoing_shuffle = False

        elif self.state == 'BAGGAGE': # we need to update the capacity of the bin in the relevant col
            if self.baggage >= 1:
                # get the cabin allocated to this person first
                # we need to get the cabin based on his current position, the first instance of baggage is when he is at the column of his seat
                cabin = self.model.get_cabin(self.pos) # this will always return the avaialbale bin
                #the bin might not always be in the current location, so we need to check if it is in the same column
                if(cabin.col == self.pos[0]):

                    self.baggage-=1
                    cabin.capacity-=1
                else: # first we need to move to the cabin first then deposit
                    print("it is going to move")
                    if(cabin.col > self.pos[0]):
                        self.move(1,0)
                    else:
                        self.move(-1,0)

                    pass


                # check what is the position, which row does it belong to, 1,2,3 will belong to the cabin at the top
                # while 5,6,7 will belong to the btm cabin

            else:
                # need to move back to the seat position
                # need to check where is the seating postion and the current position
                if(self.seat_pos[0]!=self.pos[0]):
                    if(self.seat_pos[0]>self.pos[0]):
                        self.move(1,0)
                    else:
                        self.move(-1,0)
                else:
                    self.state = 'SEATING'

        elif self.state == 'SEATING':
            if self.seat_pos[1] in (1, 2, 3):
                self.move(0, -1)
            else:
                self.move(0, 1)
            if self.pos[1] == self.seat_pos[1]:
                self.state = 'FINISHED'
                self.model.schedule.safe_remove(self)
                self.model.schedule.safe_remove_priority(self)

        if self.state == 'SHUFFLE CHECK' and self.model.get_patch((self.pos[0] + 1, self.pos[1])).state == 'FREE' and self.model.get_patch((self.pos[0] + 1, self.pos[1])).ongoing_shuffle == False:
            try:
                shuffle_agents = []
                if self.seat_pos[1] in (1, 2):
                    for y in range(3, self.seat_pos[1], -1):
                        local_agent = self.model.get_passenger((self.seat_pos[0], y))
                        if local_agent is not None:
                            if local_agent.state != 'FINISHED':
                                raise Exception()
                            shuffle_agents.append(local_agent)
                elif self.seat_pos[1] in (6, 7):
                    for y in range(5, self.seat_pos[1]):
                        local_agent = self.model.get_passenger((self.seat_pos[0], y))
                        if local_agent is not None:
                            if local_agent.state != 'FINISHED':
                                raise Exception()
                            shuffle_agents.append(local_agent)
                shuffle_count = len(shuffle_agents)
                if shuffle_count != 0:
                    self.model.get_patch((self.seat_pos[0], 4)).shuffle = shuffle_count
                    self.model.get_patch((self.seat_pos[0], 4)).back = shuffle_count
                    self.model.get_patch((self.seat_pos[0], 4)).allow_shuffle = True
                    self.model.get_patch((self.pos[0] + 1, self.pos[1])).ongoing_shuffle = True
                    for local_agent in shuffle_agents:
                        local_agent.state = 'SHUFFLE'
                        self.model.schedule.safe_remove(local_agent)
                        self.model.schedule.add_priority(local_agent)
                self.state = 'GOING'
            except Exception:
                pass

    def move(self, m_x, m_y):
        self.model.get_patch((self.pos[0], self.pos[1])).state = 'FREE'
        self.model.grid.move_agent(self, (self.pos[0] + m_x, self.pos[1] + m_y))
        self.model.get_patch((self.pos[0], self.pos[1])).state = 'TAKEN'
    def store_luggage(self):
        # storing luggage and stopping queue
        pass

    def __str__(self):
        return "ID {}\t: {}".format(self.unique_id, self.seat_pos)


class PatchAgent(Agent):
    def __init__(self, unique_id, model, patch_type, state=None):
        super().__init__(unique_id, model)
        self.type = patch_type
        self.state = state
        self.shuffle = 0
        self.back = 0
        self.allow_shuffle = False
        self.ongoing_shuffle = False

    def step(self):
        pass
class CabinAgent(Agent):
    def __init__(self,unique_id,model,patch_type,col):
        super().__init__(unique_id, model) # path type wl
        self.capacity = 4
        self.col = col
        self.type = patch_type
        self.shuffle = 0
        self.back = 0
        self.allow_shuffle = False
        self.ongoing_shuffle = False

    def step(self):
        pass


class PlaneModel(Model):
    """ Replica of the Airbus A320 Layouut and the boarding simulation of such a plane """

    method_types = {
        'Random': methods.random,
        'Front-to-back': methods.front_to_back,
        'Front-to-back (4 groups)': methods.front_to_back_gr,
        'Back-to-front': methods.back_to_front,
        'Back-to-front (4 groups)': methods.back_to_front_gr,
        'Window-Middle-Aisle': methods.win_mid_ais
    }

    def __init__(self, method, shuffle_enable=True, common_bags='normal'):
        self.grid = MultiGrid(38, 9, False)
        self.running = True
        self.schedule = queue_method.QueueActivation(self)
        self.method = self.method_types[method]
        self.entry_free = True
        self.shuffle_enable = shuffle_enable
        self.common_bags = common_bags
        # Create agents and splitting them into separate boarding groups accordingly to a given method
        self.boarding_queue = []
        self.method(self)

        # Create patches representing corridor, seats and walls
        # this part need to change to accomdoate the emergency exits
        id = 97
        for row in ( 1, 2,3, 5, 6,7):
            for col in (0, 1, 2):
                patch = PatchAgent(id, self, 'WALL')
                self.grid.place_agent(patch, (col, row))
                id += 1
            for col in range(3, 35):
                if(col!=14 and col!=16):
                    patch = PatchAgent(id, self, 'SEAT')
                else:
                    patch = PatchAgent(id, self, 'WALL"')
                self.grid.place_agent(patch, (col, row))
                id += 1
            for col in (35,36,37):
                patch = PatchAgent(id, self, 'WALL')
                self.grid.place_agent(patch, (col, row))
                id += 1
        for col in range(38):
            patch = PatchAgent(id, self, 'CORRIDOR', 'FREE')
            if (col >=2 and col <= 35):
                cabin = CabinAgent("btm"+str(col),self,"CABIN",col)
                self.grid.place_agent(cabin,(col,0))
                cabin = CabinAgent("top" + str(col), self, "CABIN",col)
                self.grid.place_agent(cabin,(col,8))
            self.grid.place_agent(patch, (col, 4))
            id += 1

    def step(self): # this is the place where the agent first enters the plane
        self.schedule.step()

        if len(self.grid.get_cell_list_contents((0, 4))) == 1:
            self.get_patch((0, 4)).state = 'FREE'

        if self.get_patch((0, 4)).state == 'FREE' and len(self.boarding_queue) > 0:
            a = self.boarding_queue.pop()
            a.state = 'GOING'
            self.schedule.add(a)
            self.grid.place_agent(a, (0, 4))
            self.get_patch((0, 4)).state = 'TAKEN'

        if self.schedule.get_agent_count() == 0:
            self.running = False

    def get_patch(self, pos):
        agents = self.grid.get_cell_list_contents(pos)
        for agent in agents:
            if isinstance(agent, PatchAgent):
                return agent
        return None

    def get_passenger(self, pos):
        agents = self.grid.get_cell_list_contents(pos)
        for agent in agents:
            if isinstance(agent, PassengerAgent):
                return agent
        return None
    def get_cabin(self,pos):  # what should be the cabin at his location, return the one with
        # check the top and btm cabin at his location
        agent1 = self.grid.get_cell_list_contents((pos[0],0)) # the btm cabin
        agent2 = self.grid.get_cell_list_contents((pos[0], 8)) # the top cabin
        for agent in agent1:
            if ( isinstance(agent,CabinAgent) and agent.capacity >0):
                return agent
        for agent in agent2:
            if(isinstance(agent,CabinAgent) and agent.capacity>0 ):
                return agent
        # if after these 2 loops and it still cannot find, then we need to use the entire search space
        cabin = self.get_next_avail_cabin(pos)
        if(isinstance(cabin,CabinAgent) and cabin.capacity >0):
            return cabin
        return None


    def get_next_avail_cabin(self,pos): # this will require the current position
        #  this function is called when the cabin allocated to the passenger column is occupied and
        if (pos[0] >= 20):  # the search space to the right is lesser
            for i in range(pos[0] + 1, 36):
                top_cabin = self.get_cabin((i, 0))
                btm_cabin = self.get_cabin((i, 8))
                if (top_cabin.capacity > 0):
                    return top_cabin
                elif (btm_cabin.capacity > 0):
                    return btm_cabin
            # even after this it doesnt return means all the cabins to the right are occupied sp have to search the left side
            for i in range(2, pos[0]):
                top_cabin = self.get_cabin((i, 0))
                btm_cabin = self.get_cabin((i, 8))
                if (top_cabin.capacity > 0):
                    return top_cabin
                elif (btm_cabin.capacity > 0):
                    return btm_cabin

        else:  # the search space to the left is smaller
            for i in range(2, pos[0]):
                top_cabin = self.get_cabin((i, 0))
                btm_cabin = self.get_cabin((i, 8))
                if (top_cabin.capacity > 0):
                    return top_cabin
                elif (btm_cabin.capacity > 0):
                    return btm_cabin
            for i in range(pos[0] + 1, 36):
                top_cabin = self.get_cabin((i, 0))
                btm_cabin = self.get_cabin((i, 8))
                if (top_cabin.capacity > 0):
                    return top_cabin
                elif (btm_cabin.capacity > 0):
                    return btm_cabin

