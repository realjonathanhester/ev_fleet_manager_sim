from sim.fleet_managers.fleet_manager import FleetManager
from sim.models.active_vehicle import ActiveVehicle
from sim.models.simulation_input import VehicleJob


class ChargeWhenEmptyFleetManager(FleetManager):
    def assign_charge_instructions(self, hour, active_vehicle: ActiveVehicle, vehicle_job: VehicleJob, energy_cost_per_kwh):
        # if there's no job, don't charge. we only charge when we can't do a job
        if vehicle_job is None:
            return 0
        # if there's enough charge to do job, do it. otherwise, charge
        if active_vehicle.current_charge_kwh > vehicle_job.kwh_required:
            return 0
        available_charge_capacity_kwh = active_vehicle.vehicle_specs.capacity_kwh - active_vehicle.current_charge_kwh
        return min(available_charge_capacity_kwh, active_vehicle.vehicle_specs.charge_rate_kw * 1.0)

