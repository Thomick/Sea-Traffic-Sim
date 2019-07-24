from Boats import *
from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from SimDisplay import *
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
import random
from collections import deque
from SimDisplay import *
import numpy as np
import time


class DQNBoat(Boat):
    def __init__(self, param, initState, targets):
        super().__init__(param, initState, targets)
        self.agent = None
        self.state = None
        self.last_action_id = 0
        self.done = False

    def update(self):
        other_boat = None
        for b in self.boatList:
            if not b is self:
                other_boat = b
                break
        self.state = get_state(self, other_boat)
        super().update()
        if not self.done:
            reward = 0
            if self.isColliding:
                self.done = True
                reward = -1
            elif self.target_reached:
                self.done = True
                reward = 1
            new_state = get_state(self, other_boat)
            self.agent.remember(self.state, self.last_action_id,
                                reward, new_state, self.done)

    def set_agent(self, agent):
        self.agent = agent

    def do_action(self):
        action_values = self.agent.get_action_values(self.state)
        self.last_action_id = self.agent.act(action_values)
        self.action_from_id(self.last_action_id)

    def action_from_id(self, action_id):
        if action_id == 0:
            self.cape = 0
        elif action_id == 1:
            self.cape = 1
        elif action_id == 2:
            self.cape = -1
        elif action_id == 3:
            self.change_gear(increase=True)
        elif action_id == 4:
            self.change_gear(increase=False)


class DQNAgent():
    def __init__(self, model=None, from_file=False):
        self.memory = deque(maxlen=3000)
        self.nb_actions = 5  # Correspond to actions form id function
        self.nb_input = 9  # correspond to get state function
        self.gamma = 0.995    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.98
        self.learning_rate = 0.01
        if model == None:
            self.model = Sequential()
            self.model.add(
                Dense(32, activation='relu', input_dim=self.nb_input))
            self.model.add(Dense(32, activation='relu'))
            self.model.add(Dense(32, activation='relu'))
            self.model.add(Dense(self.nb_actions, activation='linear'))
            self.model.compile(
                loss='mse', optimizer=Adam(lr=self.learning_rate))
        else:
            self.model = model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        batch = random.sample(self.memory, batch_size)
        states = []
        targets_f = []
        for state, action, reward, next_state, done in batch:
            states.append(state[0])
            target = reward
            if not done:
                target = reward + self.gamma * \
                    np.amax(self.model.predict(next_state)[0])
            targets_f.append(self.model.predict(state)[0])
            targets_f[-1][action] = target
        states = np.array(states)
        targets_f = np.array(targets_f)
        self.model.fit(states, targets_f, epochs=1, verbose=0)

    def act(self, action_values):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.nb_actions)
        return np.argmax(action_values)
    
    def dec_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_action_values(self, state):
        action_values = self.model.predict(state)
        return action_values
    
    def save(self,file):
        self.model.save(file)
        
    def load(self,file):
        self.model = load_model(file)


def get_state(boat, other_boat):
        # State minimalist a etoffer pour une generalisation
    rot_angle = angle_between(boat.target, np.array([1, 0]))
    cor_other_pos = other_boat.pos - boat.pos
    rot_other_pos = [cor_other_pos[0] * np.cos(rot_angle) - cor_other_pos[1] * np.sin(
        rot_angle), cor_other_pos[0] * np.sin(rot_angle) + cor_other_pos[1] * np.cos(rot_angle)]
    rot_other_speed = [other_boat.speed[0] * np.cos(rot_angle) - other_boat.speed[1] * np.sin(
        rot_angle), other_boat.speed[0] * np.sin(rot_angle) + other_boat.speed[1] * np.cos(rot_angle)]
    rot_speed = [boat.speed[0] * np.cos(rot_angle) - boat.speed[1] * np.sin(
        rot_angle), boat.speed[0] * np.sin(rot_angle) + boat.speed[1] * np.cos(rot_angle)]
    cur_state = []
    cur_state.append(distance(boat.pos, boat.target))
    cur_state.append(angle_between(boat.pos - boat.target, boat.dir))
    cur_state.append(rot_speed[0])
    cur_state.append(rot_speed[1])
    cur_state.append(rot_other_pos[0])
    cur_state.append(rot_other_pos[1])
    cur_state.append(rot_other_speed[0])
    cur_state.append(rot_other_speed[1])
    cur_state.append(distance(boat.pos, other_boat.pos))
    return np.array(cur_state).reshape((1, 9))


def create_memory(agent):
    done = 0
    boats = []
    boats.append(buildBoat("BoatConfig/testboat.txt",
                           {'pos': (100, 200), 'angle': -90}, targets=[(800, 200)], name="Titanic"))
    boats.append(buildBoat("BoatConfig/testboat.txt",
                           {'pos': (800, 200), 'angle': 90}, targets=[(200, 200)], name="CDG"))
    for b in boats:
        b.boatList = boats
    d1 = False
    d2 = False
    for time in range(2000):
        r1 = 0
        r2 = 0
        prev_state = get_state(boats[0], boats[1])
        boats[0].update()
        new_state = get_state(boats[0], boats[1])
        if boats[0].target_reached:
            if d1 == False:
                d1 = True
                r1 = 1
        if (r1 == 0 and not d1) or (r1 == 1 and d1):
            action = int(boats[0].cape)
            if action == -1:
                action = 2
            agent.remember(prev_state, action, r1, new_state, d1)

        prev_state = get_state(boats[1], boats[0])
        boats[1].update()
        new_state = get_state(boats[1], boats[0])
        if boats[1].target_reached:
            if d2 == False:
                d2 = True
                r2 = 1
        if (r2 == 0 and not d2) or (r2 == 1 and d2):
            action = int(boats[1].cape)
            if action == -1:
                action = 2
            agent.remember(prev_state, action, r2, new_state, d2)
        if done == len(boats):
            break


def init_scene(agent):
    boats = []
    boats.append(buildBoat("BoatConfig/dqnboat_training.txt",
                           {'pos': (100, 200), 'angle': -90}, targets=[(800, 200)], name="Titanic"))
    boats.append(buildBoat("BoatConfig/dqnboat_training.txt",
                           {'pos': (800, 200), 'angle': 90}, targets=[(100, 200)], name="CDG"))
    for b in boats:
        b.boatList = boats
        b.set_agent(agent)
    return boats


if __name__ == "__main__":
    agent = DQNAgent()
    agent.load("save/dqnboat.h5")
    batch_size = 32
    nb_episode = 500
    display = True

    create_memory(agent)
    for i in range(1000):
        agent.replay(128)
        print(i)

    t1 = time.time()
    for e in range(nb_episode):
        print(f"##### Episode {e} #####")
        done = 0
        boats = init_scene(agent)
        for t in range(2000):
            for b in boats:
                b.update
            if done == len(boats):
                
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
            if (t + 1) % 500 == 0:
                print(f"Iter : {t+1}")
        agent.save("save/dqnboat.h5")
        agent.dec_epsilon()
        print("Episode: {}/{}, Score: {}, epsilon: {:.2}"
                      .format(e, nb_episode, t, agent.epsilon))
        print(f"Total time : {time.time()-t1} sec")
        if e % 5 == 0:
            if display:
                eps = agent.epsilon
                agent.epsilon = 0
                boats = init_scene(agent)
                scale_factor = 1
                screen_size = [900, 600]
                boatFile = "Images/boat2.png"
                disp = SimDisplay(screen_size, boatFile)
                disp.initDisplay(boats, scale_factor, [(800, 200), (100, 200)])
                disp.runSim(framerate=100, nb_step=2000, pause_on_start = False)
                agent.epsilon = eps
            agent.save("./save/dqnboat.h5")
