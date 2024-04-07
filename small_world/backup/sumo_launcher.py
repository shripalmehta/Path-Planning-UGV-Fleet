import traci

sumoCmd = ["sumo-gui", "-c", "small_world/worlds/small_world_net/sumo.sumocfg"]
traci.start(sumoCmd)
