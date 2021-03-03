from Boats import Boat
from BoatConstructor import buildBoat
from Utils import distance, angle_between
from SimDisplay import SimDisplay
from keras.models import Sequential, load_model
from keras.layers import Dense
import random
from collections import deque
import numpy as np
import time
import os

#Classe des bateaux dont les actions sont dictées par le un agent DQN
class DQNBoat(Boat):
    def __init__(self, param, initState, targets):
        super().__init__(param, initState, targets)
        self.agent = None
        self.state = None
        self.last_action_id = 0
        self.done = False
        self.init_dist = distance(self.pos, self.target)
        #self.partial_rewards = [init_dist/2,init_dist/4,init_dist/8, init_dist/16]
        self.partial_rewards = [200]
        self.reward_level = 1
        self.total_reward = 0

    def update(self):
        other_boat = None
        for b in self.boatList:
            if not b is self:
                other_boat = b
                break
        self.state = get_state(self, other_boat)
        super().update()
        if not self.done:
            reward = -0.001
            if len(self.partial_rewards) > 0 and distance(self.pos, self.target) < self.partial_rewards[0]:
                self.partial_rewards.pop(0)
                reward += self.reward_level
                #self.reward_level += 1
            if self.isColliding:
                self.done = True
                reward -= 5
            elif self.target_reached:
                self.done = True
                reward += 5
            new_state = get_state(self, other_boat)
            self.agent.remember(self.state, self.last_action_id,
                                reward, new_state, self.done)
            self.total_reward += reward

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


#Implementation du DQN
class DQNAgent():
    def __init__(self, model=None, from_file=False):
        self.memory = deque(maxlen=10000)
        self.nb_actions = 5  # Correspond to actions form id function
        self.nb_input = 9  # correspond to get state function
        self.gamma = 0.996    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.003
        self.update_delay = 2000
        self.model = self.create_model()
        self.target_model = self.create_model()
        self.replay_count = 0

    def create_model(self):
        model = Sequential()
        model.add(
            Dense(32, activation='relu', input_dim=self.nb_input))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.nb_actions, activation='linear'))
        model.compile(loss='mse', optimizer='rmsprop')
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        self.replay_count += 1
        batch = random.sample(self.memory, batch_size)
        states = []
        rewards = []
        next_states = []
        actions = []
        dones = []
        for state, action, reward, next_state, done in batch:
            states.append(state[0])
            rewards.append(reward)
            next_states.append(next_state[0])
            actions.append(action)
            dones.append(done)
        states = np.array(states)
        next_states = np.array(next_states)
        expected_vals = np.amax(self.target_model.predict(next_states), axis=1)
        targets_f = self.target_model.predict(states)
        for i in range(len(states)):
            target = reward
            if not dones[i]:
                target = reward + self.gamma * expected_vals[i]
            targets_f[i][actions[i]] = target
        self.model.fit(states, targets_f, epochs=1, verbose=0)

        if self.replay_count > self.update_delay:
            self.update_target()
            self.replay_count = 0

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

    def save(self, file):
        self.model.save(file)

    def load(self, file):
        self.model = load_model(file)

    def update_target(self):
        self.target_model.set_weights(self.model.get_weights())


#Compilation des données connues par l'agent vers un vecteur d'entrée du réseau de neuronnes
def get_state(boat, other_boat):
    # State minimalist a etoffer pour une generalisation
    rot_angle = angle_between(np.array([1, 0]), boat.target)
    cor_other_pos = other_boat.pos - boat.pos
    rot_other_pos = [cor_other_pos[0] * np.cos(rot_angle) + cor_other_pos[1] * np.sin(
        rot_angle), -cor_other_pos[0] * np.sin(rot_angle) + cor_other_pos[1] * np.cos(rot_angle)]
    rot_other_speed = [other_boat.speed[0] * np.cos(rot_angle) + other_boat.speed[1] * np.sin(
        rot_angle), -other_boat.speed[0] * np.sin(rot_angle) + other_boat.speed[1] * np.cos(rot_angle)]
    rot_speed = [boat.speed[0] * np.cos(rot_angle) + boat.speed[1] * np.sin(
        rot_angle), -boat.speed[0] * np.sin(rot_angle) + boat.speed[1] * np.cos(rot_angle)]
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


#Initialisation d'un environnement de simulation pour l'entrainement
def init_scene(agent):
    boats = []
    boats.append(buildBoat(os.path.join(os.path.dirname(__file__), "BoatConfig", "dqnboat_training.txt"),
                           {'pos': (100, 200), 'angle': -90}, targets=[(800, 200)], name="Titanic"))
    boats.append(buildBoat(os.path.join(os.path.dirname(__file__), "BoatConfig", "dqnboat_training.txt"),
                           {'pos': (800, 200), 'angle': 90}, targets=[(100, 200)], name="CDG"))
    for b in boats:
        b.boatList = boats
        b.set_agent(agent)
    return boats


if __name__ == "__main__":
    agent = DQNAgent()
    # agent.load("save/dqnboat175n.h5")
    batch_size = 64
    nb_episode = 5000
    display = False

    t0 = time.time()
    for e in range(0, nb_episode):
        print(f"##### Episode {e} #####")
        t1 = time.time()
        boats = init_scene(agent)
        for t in range(2000):
            done = 0
            for b in boats:
                b.update()
                if b.done:
                    done += 1
            if done == len(boats):
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
            if (t + 1) % 500 == 0:
                print(f"Iter : {t+1}")
        print("Total Rewards :")
        for b in boats:
            print(f"{b.name} : {b.total_reward}")
        print("Episode: {}/{}, Nb Step: {}, Epsilon: {:.2}"
              .format(e, nb_episode, t, agent.epsilon))
        t2 = time.time()
        print(f"Episode time : {t2-t1} sec")
        print(f"Total time : {t2-t0} sec")
        if e % 10 == 0:
            if display:
                #eps = agent.epsilon
                #agent.epsilon = 0
                boats = init_scene(agent)
                scale_factor = 1
                screen_size = [900, 600]
                boatFile = os.path.join(os.path.dirname(
                    __file__), "Images", "boat2.png")
                disp = SimDisplay(screen_size, boatFile)
                disp.initDisplay(boats, scale_factor, [(800, 200), (100, 200)])
                disp.runSim(framerate=1000, nb_step=2000, pause_on_start=False)
                #agent.epsilon = eps
            agent.save(os.path.join(os.path.dirname(
                __file__), "save", f"dqnboat{e}n.h5"))
        agent.dec_epsilon()
