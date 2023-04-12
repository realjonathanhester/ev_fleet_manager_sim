from typing import Dict

from sim.fleet_managers.fleet_manager import FleetManager
from sim.models.active_vehicle import ActiveVehicle
from sim.models.simulation_input import SimulationInput, EnergyPrice
from sim.models.simulation_result import FleetSimulationResult


class FleetManagerSimulator:
    def __init__(self, sim_input: SimulationInput, fleet_manager: FleetManager, max_time_unit: int):
        self.sim_input = sim_input
        self.fleet_manager = fleet_manager
        # create an 'ActiveVehicle' for every vehicle in the fleet
        self.vehicles: Dict[str, ActiveVehicle] = {v.vehicle_id: ActiveVehicle(v) for v in sim_input.vehicle_specs}
        # create a map of { vehicle_id -> { hour -> VehicleJob} } so we can lookup a job with vehicle_id, hour
        self.vehicle_jobs = {v.vehicle_id: dict() for v in self.vehicles.values()}
        for job in sim_input.vehicle_jobs:
            self.vehicle_jobs[job.vehicle_id][job.hour] = job
        self.max_time_unit = max_time_unit
        self.energy_prices: Dict[int, EnergyPrice] = {p.hour: p.cents_per_hour for p in sim_input.energy_prices}

    @classmethod
    def create_sim(cls, sim_input: SimulationInput, fleet_manager: FleetManager):
        cls.validate_input(sim_input)
        max_time_unit = max(sim_input.energy_prices, key=lambda p: p.hour)
        return FleetManagerSimulator(sim_input, fleet_manager, max_time_unit.hour)

    @classmethod
    def validate_input(cls, sim_input: SimulationInput):
        enery_price_hours = list(map(lambda p: p.hour, sim_input.energy_prices))
        max_time_unit = max(enery_price_hours)
        # make sure that we have an entry in energy prices for every time unit
        for i in range(max_time_unit):
            if i not in enery_price_hours:
                print("error: energy prices is missing entry for time unit %i" % (i))
                assert i in enery_price_hours

    def simulate(self):
        for i in range(self.max_time_unit + 1):
            self.iterate_time_unit(i)
        return FleetSimulationResult.build_from_vehicle_activity(self.vehicles)

    def iterate_time_unit(self, hour):
        for (vehicle_id, vehicle) in self.vehicles.items():
            # find the job for this vehicle for this hour
            vehicle_job = self.vehicle_jobs.get(vehicle_id).get(hour)
            energy_price = self.energy_prices[hour]
            charge_amount = self.fleet_manager.assign_charge_instructions(hour, vehicle, vehicle_job, energy_price)
            if charge_amount > 0:
                vehicle.do_charge(hour, charge_amount, vehicle.vehicle_specs.charge_rate_kw, energy_price)
            elif vehicle_job is not None:
                vehicle.do_work(hour, vehicle_job)
