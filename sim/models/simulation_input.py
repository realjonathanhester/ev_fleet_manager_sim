import csv
from dataclasses import dataclass


@dataclass
class EnergyPrice:
    hour: int
    cents_per_hour: int

    @classmethod
    def load_from_csv(cls, csv_file_name):
        prices = []
        with open(csv_file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                prices.append(
                    EnergyPrice(
                        int(row['hour']),
                        int(row['cents_per_kwh']),
                    )
                )
        return prices

@dataclass
class VehicleSpecs:
    vehicle_id: int
    initial_charge_kwh: int
    capacity_kwh: int
    charge_rate_kw: int

    @classmethod
    def load_from_csv(cls, csv_file_name):
        vehicles = []
        with open(csv_file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vehicles.append(
                    VehicleSpecs(
                        int(row['vehicle_id']),
                        int(row['initial_charge_kwh']),
                        int(row['capacity_kwh']),
                        int(row['charge_rate_kw']),
                    )
                )
        return vehicles


@dataclass
class VehicleJob:
    vehicle_id: int
    hour: int
    earning_opportunity_dollars: int
    kwh_required: int

    @classmethod
    def load_from_csv(cls, csv_file_name):
        vehicle_jobs = []
        with open(csv_file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vehicle_jobs.append(
                    VehicleJob(
                        int(row['vehicle_id']),
                        int(row['hour']),
                        int(row['earning_opportunity']),
                        int(row['kwh_required']),
                    )
                )
        return vehicle_jobs


@dataclass
class SimulationInput:
    vehicle_specs: list[VehicleSpecs]
    vehicle_jobs: list[VehicleJob]
    energy_prices: list[EnergyPrice]

    @classmethod
    def from_csvs(cls, vehicle_csv, vehicle_jobs_csv, energy_prices_csv):
        return SimulationInput(
            VehicleSpecs.load_from_csv(vehicle_csv),
            VehicleJob.load_from_csv(vehicle_jobs_csv),
            EnergyPrice.load_from_csv(energy_prices_csv),
        )
