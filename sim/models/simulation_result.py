from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from sim.models.active_vehicle import ActiveVehicle, VehicleActivity, VehicleChargeActivity, VehicleJobActivity, \
    VehicleSkipJobActivity


@dataclass
class FleetSimulationResult:
    """Output of simulation"""
    kwh_consumed: int = 0
    kwh_cost_cents: int = 0
    jobs_skipped: int = 0
    jobs_completed: int = 0
    number_charging_hours: int = 0
    amount_earned_dollars: int = 0
    amount_lost: int = 0
    vehicle_activity_logs: Dict[str, List[VehicleActivity]] = None

    @classmethod
    def build_from_vehicle_activity(cls, active_vehicles: Dict[int, ActiveVehicle]):
        result = FleetSimulationResult()
        result.vehicle_activity_logs = {}
        for vehicle_id, vehicle in active_vehicles.items():
            result.vehicle_activity_logs[vehicle_id] = vehicle.activities
            for activity in vehicle.activities:
                if isinstance(activity, VehicleChargeActivity):
                    result.kwh_consumed += activity.amount_charged_kwh
                    result.kwh_cost_cents += activity.charge_cost_total_cents
                    result.number_charging_hours += 1
                if isinstance(activity, VehicleSkipJobActivity):
                    result.jobs_skipped += 1
                if isinstance(activity, VehicleJobActivity):
                    result.jobs_completed += 1
                    result.kwh_consumed += activity.kwh_consumed
                    result.amount_earned_dollars += activity.amount_earned

        return result

    def write_csv(self):
        pass
