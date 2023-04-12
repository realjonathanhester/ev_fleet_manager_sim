import unittest

from sim.fleet_manager_simulator import FleetManagerSimulator
from sim.fleet_managers.charge_when_empty_fleet_manager import ChargeWhenEmptyFleetManager
from sim.fleet_managers.charge_when_idle_fleet_manager import ChargeWhenIdleFleetManager
from sim.models.simulation_input import SimulationInput
from tests.fixtures import vehicleFixtures


class TestFleetManagerSimulator(unittest.TestCase):
    def test_charge_when_idle_with_lunch_break(self):
        """Input has an hour with no jobs. ChargeWhenIdle will charge during this time and complete all jobs"""
        sim_input = SimulationInput(
            [vehicleFixtures.vehicle_100_kwh_50_percent],
            vehicleFixtures.vehicle_jobs_with_idle,
            vehicleFixtures.energy_prices_3_hours_constant,
        )
        sim = FleetManagerSimulator.create_sim(sim_input, ChargeWhenIdleFleetManager())
        result = sim.simulate()
        self.assertEqual(result.number_charging_hours, 1)
        self.assertEqual(result.jobs_completed, 2)
        self.assertEqual(result.jobs_skipped, 0)
        self.assertEqual(result.amount_earned_dollars, 100)

    def test_charge_when_empty_with_lunch_break(self):
        """Input has an hour with no jobs. ChargeWhenEmpty won't take advantage and won't complete last job"""
        sim_input = SimulationInput(
            [vehicleFixtures.vehicle_100_kwh_50_percent],
            vehicleFixtures.vehicle_jobs_with_idle,
            vehicleFixtures.energy_prices_3_hours_constant,
        )
        sim = FleetManagerSimulator.create_sim(sim_input, ChargeWhenEmptyFleetManager())
        result = sim.simulate()
        self.assertEqual(result.number_charging_hours, 0)
        self.assertEqual(result.jobs_completed, 1)
        self.assertEqual(result.jobs_skipped, 1)
        self.assertEqual(result.amount_earned_dollars, 50)

    def test_charge_when_empty_with_lunch_break(self):
        sim_input = SimulationInput(
            [vehicleFixtures.vehicle_100_kwh_50_percent],
            vehicleFixtures.vehicle_jobs_with_idle,
            vehicleFixtures.energy_prices_3_hours_constant,
        )
        sim = FleetManagerSimulator.create_sim(sim_input, ChargeWhenIdleFleetManager())
        result = sim.simulate()
        self.assertEqual(result.number_charging_hours, 1)

    def test_charge_when_empty_constant_work(self):
        sim_input = SimulationInput(
            [vehicleFixtures.vehicle_100_kwh_50_percent],
            vehicleFixtures.vehicle_jobs_constant,
            vehicleFixtures.energy_prices_24_hours_constant,
        )
        sim = FleetManagerSimulator.create_sim(sim_input, ChargeWhenEmptyFleetManager())
        result = sim.simulate()
        self.assertEqual(result.number_charging_hours, 2)
        self.assertEqual(result.amount_earned_dollars, 1100)
        self.assertEqual(result.jobs_completed, 22)
        self.assertEqual(result.kwh_consumed, 400)
        self.assertEqual(result.kwh_cost_cents, 4500)

    def test_charge_when_idle_constant_work(self):
        sim_input = SimulationInput(
            [vehicleFixtures.vehicle_100_kwh_50_percent],
            vehicleFixtures.vehicle_jobs_constant,
            vehicleFixtures.energy_prices_24_hours_constant,
        )
        sim = FleetManagerSimulator.create_sim(sim_input, ChargeWhenIdleFleetManager())
        result = sim.simulate()
        self.assertEqual(result.number_charging_hours, 0)
        # since vehicle never has scheduled downtime, it completes jobs until runs it out of charge
        # and never charges
        self.assertEqual(result.jobs_skipped, 20)
        self.assertEqual(result.jobs_completed, 4)
        self.assertEqual(result.amount_earned_dollars, 200)
        self.assertEqual(result.kwh_consumed, 40)
        self.assertEqual(result.kwh_cost_cents, 0)


if __name__ == '__main__':
    unittest.main()
