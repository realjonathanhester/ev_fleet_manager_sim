import dataclasses
from dataclasses import dataclass

from sim.models.simulation_input import VehicleSpecs, VehicleJob


class VehicleActivity:
    pass


@dataclass
class VehicleChargeActivity(VehicleActivity):
    hour: int
    amount_charged_kwh: int
    cents_per_hour: int
    charge_cost_total_cents: int


@dataclass
class VehicleJobActivity(VehicleActivity):
    hour: int
    amount_earned: int
    kwh_consumed: int


@dataclass
class VehicleSkipJobActivity(VehicleActivity):
    earnings_missed: int


class ActiveVehicle:
    def __init__(self, vehicle_specs: VehicleSpecs):
        self.vehicle_id = vehicle_specs.vehicle_id
        self.vehicle_specs = vehicle_specs
        self.current_charge_kwh = vehicle_specs.initial_charge_kwh
        self.activities = list()

    def do_work(self, hour, vehicle_job: VehicleJob):
        if self.current_charge_kwh - vehicle_job.kwh_required <= 0:
            # not enough charge to do job so downtime
            self.activities.append(VehicleSkipJobActivity(vehicle_job.earning_opportunity_dollars))
            return
        self.current_charge_kwh = self.current_charge_kwh - vehicle_job.kwh_required
        self.activities.append(
            VehicleJobActivity(
                hour,
                vehicle_job.earning_opportunity_dollars,
                vehicle_job.kwh_required
            )
        )

    def do_charge(self, hour, charge_amount, charge_rate, kwh_cents_per_hour, vehicle_job_skipped: VehicleJob):
        if self.current_charge_kwh + charge_amount > self.vehicle_specs.capacity_kwh:
            raise Exception("trying to charge vehicle above capacity")
        # assuming time unit is hour. amount to charge is either the desired charge amount or max charge in hour
        charge_amount = min(charge_amount, charge_rate * 1.0)
        self.current_charge_kwh = self.current_charge_kwh + charge_amount
        self.activities.append(
            VehicleChargeActivity(
                hour,
                charge_amount,
                kwh_cents_per_hour,
                charge_amount * kwh_cents_per_hour
            )
        )
        if vehicle_job_skipped is not None:
            self.activities.append(VehicleSkipJobActivity(vehicle_job_skipped.earning_opportunity_dollars))
