from Model import *

# def visualize_env(environment):
#     for agent_type in environment.agents.keys():
#         for agent in environment.agents[agent_type]:





if __name__ == '__main__':
    print("Simulation started...")
    env = Environment(num_agents=20, num_gates=1, max_x=50, max_y=50)

    # Visuzalization crap
    fig = plt.figure(figsize=(20,15))
    

    timesteps = 20
    for step in range(timesteps):
        env.timestep()


    print(str(env))




