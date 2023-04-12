from sim.models.active_vehicle import ActiveVehicle
from sim.models.simulation_input import VehicleJob


class FleetManager:
    def assign_charge_instructions(self, hour, vehicle: ActiveVehicle, vehicle_job: VehicleJob, energy_cost_per_kwh):
        raise NotImplementedError()
