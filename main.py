# Press the green button in the gutter to run the script.
import sys

from sim.fleet_manager_simulator import FleetManagerSimulator
from sim.fleet_managers.charge_when_empty_fleet_manager import ChargeWhenEmptyFleetManager
from sim.fleet_managers.charge_when_idle_fleet_manager import ChargeWhenIdleFleetManager
from sim.models.simulation_input import SimulationInput

if __name__ == '__main__':
    args = sys.argv
    sim_input = SimulationInput.from_csvs(
        args[1],
        args[2],
        args[3],
    )
    fleet_manager = None
    if args[4] == 'ChargeWhenIdleFleetManager':
        fleet_manager = ChargeWhenIdleFleetManager()
    elif args[3] == 'ChargeWhenEmptyFleetManager':
        fleet_manager = ChargeWhenEmptyFleetManager()
    sim = FleetManagerSimulator.create_sim(sim_input, fleet_manager)
    result = sim.simulate()
    # TODO: implement result.write_csv and output results to specified csv file
    print(result)
