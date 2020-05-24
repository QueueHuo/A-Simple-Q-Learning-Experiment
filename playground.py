import random
import copy
import hashlib
class Playground:
    def __init__(self):

        self.state = {}
        self.reset_playground()
    def get_serialized_state(self):
        # TODO:
        c = hashlib.sha512()
        c.update(bytes(str(self.state), encoding='ASCII'))
        return c.hexdigest()
    def step(self, action):
        """
        this will push the state from s -> s'
        takes action
        returns the actual reward and new state s'
        and whether it is the final stage
        """
        self.state['round'] += 1
        prev_state = copy.deepcopy(self.state)
        new_state = action.act(self.state)

        # TODO: enemy logic
        x = random.randint(1,10)
        if 1 <= x <= 3:
            # Enemy trys to move forward
            if(self.state['enemy']['pos'] - 1 > 0 and self.state['enemy']['pos'] - 1 != self.state['hero']['pos']):
                self.state['enemy']['pos'] -= 1
        elif 4 <= x <= 5:
            # Enemy trys to move backward
            if(self.state['enemy']['pos'] + 1 < self.state['map_len']):
                self.state['enemy']['pos'] += 1
        elif 6 <= x <= 8:
            # Enemy trys to attack
            if(self.state['enemy']['pos'] - 1 == self.state['hero']['pos']):
                self.state['hero']['hp'] -= 1
                if(self.state['hero']['hp'] < 0):
                    self.state['hero']['hp'] = 0
        elif x == 9:
            if(self.state['enemy']['pos'] - 1 == self.state['hero']['pos']):
                self.state['hero']['hp'] -= 2
                self.state['enemy']['hp'] -= 1
                if(self.state['hero']['hp'] < 0):
                    self.state['hero']['hp'] = 0
                if(self.state['enemy']['hp'] < 0):
                    self.state['enemy']['hp'] = 0

        reward = 0
        reward += (prev_state['enemy']['hp'] - self.state['enemy']['hp']) / (self.state['round'] / (self.state['max_rounds']/2)) + 5 if (self.state['enemy']['hp'] <= 0) else -0.01
        reward -= (prev_state['hero']['hp'] - self.state['hero']['hp']) + 3 if (self.state['hero']['hp'] <= 0) else 0
        # print("ENEMY HP %s -> %s"%(prev_state['enemy']['hp'], self.state['enemy']['hp']))

        is_terminal_state = (self.state['hero']['hp'] <= 0) or (self.state['enemy']['hp'] <= 0) or self.state['round'] > new_state['max_rounds']
        self.state = new_state
        return self.get_serialized_state(), reward, is_terminal_state
        
    def reset_playground(self):
        """
        Resets the playground for the next episode
        """
        self.state['round'] = 0
        self.state = {
            'map_len': 22, # from 1 to , both inclusive
            'hero': {
                'pos': 3,
                'hp': 10,
                'full_hp': 10,
            },
            'enemy': {
                'pos': 13,
                'hp': 10,
                'full_hp': 10,
            },
            'max_rounds': 500,
            'round': 0,
        }

    @staticmethod
    def get_actions():
        return [
            MoveForwardAction,
            AttackAction,
            MoveBackwardAction,
            DeepAttackAction
        ]
        pass
    
    def _render_both_hp(self):
        output = ''
        hero_block_to_render = int((float(self.state['hero']['hp']) / self.state['hero']['full_hp']) * 10)
        enemy_block_to_render = int((float(self.state['enemy']['hp']) / self.state['enemy']['full_hp']) * 10)
        output += '■' * hero_block_to_render + ' ' * (10 - hero_block_to_render)
        output += '  ' # two spaces between
        output += ' ' * (10 - enemy_block_to_render) + '■' * enemy_block_to_render
        return output

    def _render_both_position(self):
        output = ''
        for _ in range(1,23):
            if _ == self.state['hero']['pos']:
                output += '&'
            elif _ == self.state['enemy']['pos']:
                output += 'X'
            else:
                output += ' '
        return output

    def render_battle(self):
        print('+'+'-'*22+'+')
        print('|', self._render_both_hp(), '|', sep = '')
        print('|' + ' '*22 + '|')
        print('|' + ' '*22 + '|')
        print('|',self._render_both_position(),'|', sep = '')
        print('+'+'-'*22+'+')
        print('Round: %s'%self.state['round'])

class MoveForwardAction:
    @staticmethod 
    def act(state):
        new_state = state
        if state['hero']['pos'] + 1 <= state['map_len'] and state['hero']['pos'] + 1 != state['enemy']['pos']:
            state['hero']['pos'] += 1
        # elif state['hero']['pos'] + 1 == state['enemy']['pos']:
        #     state['enemy']['hp'] -= 1
        #     if(state['enemy']['hp'] < 0):
        #         state['enemy']['hp'] = 0
        return new_state

class MoveBackwardAction:
    @staticmethod 
    def act(state):
        new_state = state
        if state['hero']['pos'] - 1 > 0:
            state['hero']['pos'] -= 1
        return new_state

class AttackAction:
    @staticmethod 
    def act(state):
        new_state = state
        if state['enemy']['pos'] - state['hero']['pos'] < 2:
            state['enemy']['hp'] -= 1
            if(state['enemy']['hp'] < 0):
                state['enemy']['hp'] = 0
        else:
            MoveForwardAction.act(state)
        return new_state

class DeepAttackAction:
    @staticmethod 
    def act(state):
        new_state = state
        if state['enemy']['pos'] - state['hero']['pos'] < 2:
            state['enemy']['hp'] -= 2
            if(state['enemy']['hp'] < 0):
                state['enemy']['hp'] = 0
            state['hero']['hp'] -= 1
            if(state['hero']['hp'] < 0):
                state['hero']['hp'] = 0
        return new_state

# class IdleAction:
#     @staticmethod 
#     def act(state):
#         new_state = state
#         return new_state

if __name__ == '__main__':
    import os
    import time
    import random
    playground = Playground()
    playground.render_battle()
    actions = Playground.get_actions()
    while True:
        s, r, t = playground.step(actions[random.randint(0,3)])
        os.system('cls')
        if t:
            print("GAME OVER")
            time.sleep(1)
            playground.reset_playground()
        else:
            playground.render_battle()

        time.sleep(0.5)