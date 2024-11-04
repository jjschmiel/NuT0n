from tf_agents.specs import array_spec
from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
import numpy as np
import main as main
import random
class Nut0nEnv(py_environment.PyEnvironment):
    _episode_ended = False
    episodes = 0

    def __init__(self):
        super().__init__() 
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(2,), dtype=np.int32, minimum=0, maximum=2, name='action')
        
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.int32, minimum=0, name='observation')
        
        
        print("**********started game***************")

        
        
    def move_ev(self, m):
        print("**********in move_ev***************")
        if m == 0:
            self.main.active_game_controls(self.main.player)
        elif m == 1:
            self.main.active_game_controls(self.main.player)
        else:
            self.main.active_game_controls(self.main.player)

    def observation_spec(self):
        print("**********in observation_spec***************")
        return self._observation_spec
    
    def action_spec(self):
        print("**********in action_spec***************")
        return self._action_spec
    
    def _reset(self):
        print("**********in _reset***************")
        self._state = 0
        self._episode_ended = False
        self.main = main
        return ts.restart(np.array([self._state], dtype=np.int32))
    

    def _step(self, action):
        print("**********in _step***************")
        print("action begining: " + str(action))
        print("state begining: " + str(self._state))
        if self._episode_ended:
            #print("episode ended")
            return ts.StepType.LAST
        
        self.main.main(True, self)

        # Update state based on actions
        self._state += action1 + action2

        print("action end: " + str(action))
        print("state end: " + str(self._state))

        if self._state >= 10:
            self._episode_ended = True
            return ts.termination(np.array([self._state], dtype=np.int32), reward=1)
        else:
            return ts.transition(np.array([self._state], dtype=np.int32), reward=0.1)

if __name__ == "__main__":
    env = Nut0nEnv()

    time_step_spec = env.time_step_spec()

    print("discount: " + str(time_step_spec.discount))
    print("step_type: " + str(time_step_spec.step_type))
    print("reward: " + str(time_step_spec.reward))
    print("observation: " + str(time_step_spec.observation))

    while True:
        print("**********in while loop***************")
        random_action = random.randint(0, 2)
        time_step = env.step(random_action)