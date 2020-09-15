# RLStrategy for the simplified problem of only one boat

from Boats import Boat
from BoatConstructor import buildBoat
from Utils import angle_between, distance, unit_vector
from SimDisplay import SimDisplay
from keras.models import Sequential, load_model
from keras.layers import Dense
import random
from collections import deque
import numpy as np
import time
import os
from keras.optimizers import Adam
import matplotlib.pyplot as plt


class DQNBoat(Boat):
    def __init__(self, param, initState, targets):
        super().__init__(param, initState, targets)
        self.agent = None
        self.last_action_id = 0
        self.done = False
        self.init_dist = distance(self.pos, self.target)
        self.reward_level = 1
        self.state = self.get_state()
        self.total_reward = 0

    def update(self):
        reward = np.dot(unit_vector(self.dir), unit_vector(self.target-self.pos)) * \
            (self.init_dist-distance(self.pos, self.target))/(self.init_dist*2000)
        previous_state = self.state
        super().update()
        if not self.done:
            if self.isColliding:
                self.done = True
                reward -= 3
            elif self.target_reached:
                self.done = True
                reward += 2
            self.state = self.get_state()
            self.agent.remember(previous_state, self.last_action_id,
                                reward, self.state, self.done)
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
            self.cape = 0.1
        elif action_id == 2:
            self.cape = -0.1
        elif action_id == 3:
            self.change_gear(increase=True)
        elif action_id == 4:
            self.change_gear(increase=False)

    def get_state(self):
        # State minimalist a etoffer pour une generalisation
        rot_angle = angle_between(np.array([1, 0]), self.target)
        speed = [self.speed[0] * np.cos(rot_angle) + self.speed[1] * np.sin(
            rot_angle), -self.speed[0] * np.sin(rot_angle) + self.speed[1] * np.cos(rot_angle)]
        cur_state = []
        cur_state.append(distance(self.pos, self.target)/2000)
        cur_state.append(angle_between(self.pos - self.target, self.dir))
        cur_state.append(self.angular_speed)
        cur_state.append(speed[0])
        cur_state.append(speed[1])
        return np.array(cur_state).reshape((1, 5))


class DQNAgent():
    def __init__(self, model=None, from_file=False):
        self.memory = deque(maxlen=10000)
        self.nb_actions = 5  # Correspond to actions form id function
        self.nb_input = 5  # correspond to get state function
        self.gamma = 1    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.99
        self.learning_rate = 0.01
        self.update_delay = 500
        self.model = self.create_model()
        self.target_model = self.create_model()
        self.replay_count = 0

    def create_model(self):
        model = Sequential()
        model.add(
            Dense(32, activation='relu', input_dim=self.nb_input))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.nb_actions, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
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


def init_scene(agent):
    boats = []
    boats.append(buildBoat(os.path.join(os.path.dirname(__file__), "BoatConfig", "dqnboat_training.txt"),
                           {'pos': (100, 200), 'angle': -90}, targets=[(800, 200)], name="Titanic"))
    for b in boats:
        b.boatList = boats
        b.set_agent(agent)
    return boats


if __name__ == "__main__":
    agent = DQNAgent()
    agent.load(os.path.join(os.path.dirname(
        __file__), "save", f"dqnboat2740n.h5"))
    batch_size = 64
    nb_episode = 5000
    display = True

    t0 = time.time()
    for e in range(0, nb_episode):
        print(f"##### Episode {e} #####")
        t1 = time.time()
        boats = init_scene(agent)
        t = 0
        while t < 2000:
            t += 1
            done = True
            for b in boats:
                b.update()
                done = done and b.done
            if done:
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
        if e % 5 == 0:
            if display:
                eps = agent.epsilon
                agent.epsilon = 0.0
                boats = init_scene(agent)
                scale_factor = 1
                screen_size = [900, 600]
                boatFile = os.path.join(os.path.dirname(
                    __file__), "Images", "boat2.png")
                disp = SimDisplay(screen_size, boatFile)
                disp.initDisplay(boats, scale_factor, [(800, 200), (100, 200)])
                disp.runSim(framerate=1000, nb_step=2000, pause_on_start=False)
                agent.epsilon = eps
            agent.save(os.path.join(os.path.dirname(
                __file__), "save", f"dqnboat{e}n.h5"))
        agent.dec_epsilon()
