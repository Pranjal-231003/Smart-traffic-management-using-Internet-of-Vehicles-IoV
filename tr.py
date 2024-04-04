import os
import sys
import optparse
import traci
import time

def get_shortest_route(veh_id, traffic):
    source = traci.vehicle.getRoadID(veh_id)
    destination = traci.vehicle.getRoute(veh_id)[-1]
    return traci.simulation.findRoute(source, destination)

def reroute_vehicle(veh_id, traffic):
    new_route = get_shortest_route(veh_id, traffic)
    print(new_route)
    traci.vehicle.setRoute(veh_id, new_route.edges)  # Set the new route for the vehicle


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


def run():
    step = 0
    traffic = {}
    start_time = time.time()
    highest = 0
    try:
        departure_times = {}
        with open("simulation_output.txt", "w") as output_file:
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                for vehicle_id in traci.vehicle.getIDList():
                    # Get departure time for each vehicle
                    if vehicle_id not in departure_times:
                        departure_times[vehicle_id] = traci.simulation.getTime()

                if step % 200 == 0:
                    for veh_id in traci.vehicle.getIDList():
                        sum_traffic = 0
                        edges = traci.vehicle.getRoute(veh_id)
                        for edge in edges:
                            traffic[edge] = len(traci.edge.getLastStepVehicleIDs(edge))
                            sum_traffic += traffic[edge]
                        if sum_traffic > 3:
                            reroute_vehicle(veh_id, traffic)
                step += 1
            for vehicle_id, departure_time in departure_times.items():
                total_travel_time = traci.simulation.getTime() - departure_time
                output_file.write(f"Vehicle {vehicle_id} total traveling time: {total_travel_time}s\n")
                if (total_travel_time > highest):
                    highest = total_travel_time

            end_time = time.time()
            total_execution_time = end_time - start_time
            output_file.write(f"Total execution time: {total_execution_time} seconds\n")

            output_file.write(f"Total simulation time: {highest} seconds\n")

    finally:
        traci.close()

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--nogui", action="store_true", default=False, help="Run the commandline version of SUMO")
    options, args = parser.parse_args()

    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("Please declare environment variable 'SUMO_HOME'")

    sumo_binary = "sumo-gui" if not options.nogui else "sumo"
    sumo_cmd = [sumo_binary, "-c", "jaipur.sumocfg"]
    traci.start(sumo_cmd)

    run()
