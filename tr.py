import traci
import traci.constants as tc
import time

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

# def switch_vehicles_to_route(vehicle_ids, new_route):
#     for vehicle_id in vehicle_ids:
#         switch_route(vehicle_id, new_route)

def main():
    sumo_binary = "sumo-gui"  # Replace with the path to your SUMO binary
    sumo_cmd = [sumo_binary, "-c", "jaipur.sumo.cfg", "--start"]
    traci.start(sumo_cmd)
    start_time = time.time()
    highest = 0
    try:
        departure_times = {}
        with open("simulation_output.txt", "w") as output_file:
            while traci.simulation.getMinExpectedNumber() > 0:
            #     # Monitor traffic conditions on Route 1
            #     traffic_condition_on_route_1 = check_traffic_on_route(ROUTE_1_EDGES)
            #     traffic_condition_on_route_2 = check_traffic_on_route(ROUTE_2_EDGES)

                
            #     # Write simulation output to text file
            #     output_file.write(f"Time: {traci.simulation.getTime()}s\n")
            #     output_file.write(f"Traffic condition on Route 1: {traffic_condition_on_route_1}\n")
            #     output_file.write(f"Traffic condition on Route 2: {traffic_condition_on_route_2}\n\n")
                traci.simulationStep()

                 # Iterate over all vehicles in the simulation
                for vehicle_id in traci.vehicle.getIDList():
                    # Get departure time for each vehicle
                    if vehicle_id not in departure_times:
                        departure_times[vehicle_id] = traci.simulation.getTime()

            # Calculate and print traveling time for each vehicle
            for vehicle_id, departure_time in departure_times.items():
                total_travel_time = traci.simulation.getTime() - departure_time
                output_file.write(f"Vehicle {vehicle_id} total traveling time: {total_travel_time}s\n")
                if(total_travel_time>highest):
                    highest = total_travel_time

            end_time = time.time()
            total_execution_time = end_time - start_time
            output_file.write(f"Total execution time: {total_execution_time} seconds\n")

            output_file.write(f"Total simulation time: {highest} seconds\n")
    finally:
        traci.close()

if __name__ == "__main__":
    main()
