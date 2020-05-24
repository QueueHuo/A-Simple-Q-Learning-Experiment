from playground import Playground
import pickle
import random
import time
import os
import platform
playground = Playground()
actions = Playground.get_actions()


LEARNING_RATE = 0.2
# How many episodes u wanna train
TARGET_EPISODES = 50
# How long the progress bar u'd like to see
NUMBER_OF_BARS_IN_UI = 20
GAMMA = 0.2
Q = {}
reward_history = []
# Set to False if u wanna train; set to true if u wanna watch an animation-like demonstration lively
ENABLE_RENDER = True

progress_indicator = 0

def save_Q():
    global Q
    with open('Q_Learning_Data.pkl', 'wb') as fw:
        pickle.dump(Q, fw)
        fw.flush()
        fw.close()

def load_Q():
    global Q
    try:
        with open('Q_Learning_Data.pkl', 'rb') as fr:
            Q = pickle.load(fr)
            fr.close()
    except FileNotFoundError as fnfe:
        Q = {}
        save_Q()
load_Q()





def get_maximum_reward(actions_under_state):
    
    if actions_under_state == None:
        return 0
    optimal_action_v = None
    for k, v in actions_under_state.items():
        if optimal_action_v == None or optimal_action_v < v:
            optimal_action_v = v
    return optimal_action_v

action_initialized_values = {}
for i in range(len(actions)):
    action_initialized_values.update({
       i : 0
    })

if not ENABLE_RENDER:
    print("="*NUMBER_OF_BARS_IN_UI)
# Q-Learning
current_episode = 0
avg_reward = []
while current_episode < TARGET_EPISODES:
    current_episode += 1
    progress_indicator += 1
    if(not ENABLE_RENDER and float(progress_indicator) / TARGET_EPISODES > (1.00/NUMBER_OF_BARS_IN_UI)):
        print('■',end='', flush=True)
        save_Q()
        progress_indicator = 0
        avg_reward.append(sum(reward_history)/len(reward_history))
        
    state = playground.get_serialized_state()
    is_terminal_state = False
    total_reward = 0

    while not is_terminal_state:
        
        optimal_action = random.randint(0,len(actions)-1)

        if Q.get(state, None) != None:
            # choose optimal action
            optimal_action_v = None
            all_z = True
            for k, v in Q.get(state, None).items():
                if v != 0:
                    all_z = False
                if optimal_action_v == None or optimal_action_v < v:
                    optimal_action_v = v
                    optimal_action = k
            if all_z:
                optimal_action = random.randint(0,len(actions)-1)
        else:
            Q.update({state: action_initialized_values})

        # act and experience
        new_state, reward, is_terminal_state = playground.step(actions[optimal_action])
        # update Q Table
        Q[state][optimal_action] = Q[state][optimal_action] + \
            LEARNING_RATE * (reward + GAMMA * get_maximum_reward(Q.get(new_state)) - Q[state][optimal_action])
        state = new_state
        total_reward += reward
        if ENABLE_RENDER:
            time.sleep(0.1)
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
            playground.render_battle()

    reward_history.append(total_reward)
    
    playground.reset_playground()

    if ENABLE_RENDER:
        print('GAME OVER; Total rewards = %s'%total_reward)
        time.sleep(2)






# import matplotlib.pyplot as plt

# plt.plot(reward_history)

# plt.show()
    
# plt.plot(avg_reward)
# plt.xlabel("Group No.")
# plt.ylabel('Score')
# plt.show()