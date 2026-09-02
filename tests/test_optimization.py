from simulation_calibration.optimization import Optimization


def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return (x - 2) ** 2

optimization = Optimization(objective=objective)
study = optimization.optuna_run(n_trials=100)
best_params = study.best_params
found_x = best_params["x"]
print(f"Found x: {found_x}, (x - 2)^2: {(found_x - 2) ** 2}")