import traci
import traci.constants as tc

ROUTE_1_EDGES = ["170204662#0", "170204662#1", "170204662#2", "170204662#3", "449397140", "532234592#3", "532234592#4", "532234592#5", "170204653#0", "-28851030#3", "-28851030#2", "-28851030#1", "-28851030#0"]
ROUTE_2_EDGES = ["170204662#0", "170204662#1", "170204662#2"]

def check_traffic_on_route(route_edges):
    total_speed = 0
    vehicle_count = 0

    for edge in route_edges:
        vehicle_list = traci.edge.getLastStepVehicleIDs(edge)
        for vehicle_id in vehicle_list:
            
            total_speed += traci.vehicle.getSpeed(vehicle_id)
            vehicle_count += 1

    average_speed = total_speed / max(1, vehicle_count)  # To avoid division by zero

    # You can define your own threshold for traffic conditions
    traffic_threshold = 10  # Adjust this value based on your simulation

    return average_speed < traffic_threshold

def switch_vehicles_to_route(vehicle_ids, new_route):
    for vehicle_id in vehicle_ids:
        switch_route(vehicle_id, new_route)

def main():
    sumo_binary = "sumo"  # Replace with the path to your SUMO binary
    sumo_cmd = [sumo_binary, "-c", "jaipur.sumo.cfg", "--start"]

    traci.start(sumo_cmd)

    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            # Monitor traffic conditions on Route 1
            traffic_condition_on_route_1 = check_traffic_on_route(ROUTE_1_EDGES)
            traffic_condition_on_route_2 = check_traffic_on_route(ROUTE_2_EDGES)

            if traffic_condition_on_route_1:
                # Switch vehicles to Route 2
                switch_vehicles_to_route(traci.vehicle.getIDList(), "route3")

            if traffic_condition_on_route_2:
                # Switch vehicles to Route 1
                switch_vehicles_to_route(traci.vehicle.getIDList(), "route1")

            traci.simulationStep()

    finally:
        traci.close()

if __name__ == "__main__":
    main()
