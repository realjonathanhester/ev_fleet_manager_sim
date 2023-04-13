# Fleet Manager Simulator
A simulator that evaluates fleet management charging strategies.

Given a fleet of electric vehicles with earnings opportunities and electricity prices, the simulator uses
a charging strategy algorithm to determine when vehicles charge or do work. The result of the simulation 
includes metrics on how well the fleet performed, including earnings potential met and energy costs 
incurred. 

To run the tests

`python3 -m unittest tests/test_fleet_manager_simulator.py`

To run the script with csv inputs

`
jonathanhester@jonathans-MacBook-Air chargingSimulator % python3 main.py tests/data/vehicles.csv tests/data/vehicle_jobs.csv tests/data/energy_costs.csv ChargeWhenIdleFleetManager`

Input
- Fleet vehicle specifications [vehicle_id,initial_charge_kwh,capacity_kwh,charge_rate_kw]
- Vehicle earnings opportunities [vehicle_id,hour,earning_opportunity,kwh_required]
- Charging costs [hour,cents_per_kwh]

Output 
- SimulationResult 
  - kwh_consumed
  - kwh_cost_cents
  - jobs_skipped
  - jobs_completed
  - number_charging_hours 
  - amount_earned_dollars 
  - amount_lost 
  - vehicle_activity_logs

Imagine you operate a fleet of autonomous EVs doing work on a rideshare network. You need to make decisions on 
when the vehicles earn and when they undergo downtime for charging. This decision will be based on many factors
but two important ones are the cost of charging and the earnings opportunities available. Both of these will 
vary over time, often in complex but forecastable ways.

This is a simple tool that can evaluate implementations of these decision making strategies on specified
scenarios in a simple, deterministic environment. Scenarios could easily be generated from snapshots of
historical data. 