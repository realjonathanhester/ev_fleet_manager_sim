from dataclasses import dataclass


@dataclass
class EnergyPrice:
    hour: int
    cents_per_hour: int


@dataclass
class VehicleSpecs:
    vehicle_id: int
    initial_charge_kwh: int
    capacity_kwh: int
    charge_rate_kw: int

    @classmethod
    def load_from_csv(cls, csv_file_name):
        pass


@dataclass
class VehicleJob:
    vehicle_id: int
    hour: int
    earning_opportunity_dollars: int
    kwh_required: int

    @classmethod
    def loadFromCsv(cls, csv_file_name):
        pass


@dataclass
class SimulationInput:
    vehicle_specs: list[VehicleSpecs]
    vehicle_jobs: list[VehicleJob]
    energy_prices: list[EnergyPrice]
