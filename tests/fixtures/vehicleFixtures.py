from sim.models.simulation_input import EnergyPrice
from sim.models.simulation_input import VehicleSpecs
from sim.models.simulation_input import VehicleJob


vehicle_100_kwh_50_percent = VehicleSpecs(1, 50, 100, 100)

vehicle_jobs_with_idle = [
    VehicleJob(
        vehicle_id=vehicle_100_kwh_50_percent.vehicle_id,
        hour=0,
        earning_opportunity_dollars=50,
        kwh_required=40
    ),
    # idle for hour 1
    VehicleJob(
        vehicle_id=vehicle_100_kwh_50_percent.vehicle_id,
        hour=2,
        earning_opportunity_dollars=50,
        kwh_required=40
    ),
]

energy_prices_3_hours_constant = [EnergyPrice(hour, 25) for hour in range(3)]

vehicle_jobs_constant = [
    VehicleJob(
        vehicle_id=vehicle_100_kwh_50_percent.vehicle_id,
        hour=hour,
        earning_opportunity_dollars=50,
        kwh_required=10
    ) for hour in range(24)
]
energy_prices_24_hours_constant = [EnergyPrice(hour, 25) for hour in range(24)]