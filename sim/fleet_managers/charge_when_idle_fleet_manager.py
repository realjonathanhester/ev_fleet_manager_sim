from sim.fleet_managers.fleet_manager import FleetManager
from sim.models.active_vehicle import ActiveVehicle
from sim.models.simulation_input import VehicleJob


class ChargeWhenIdleFleetManager(FleetManager):
    """
    A naive fleet manager that will charge the vehicle when its opportunity cost is 0
    (or has no job for this time unit). It does not care about the price of energy
    """
    def assign_charge_instructions(self, hour, vehicle: ActiveVehicle, vehicle_job: VehicleJob, energy_cost_per_kwh):
        if vehicle_job is None or vehicle_job.earning_opportunity_dollars <= 0:
            return max(0, vehicle.vehicle_specs.capacity_kwh - vehicle.current_charge_kwh)
        return 0
