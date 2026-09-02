import optuna

class Optimization:
    def __init__(self, objective):
        self.objective = objective


    def optuna_run(self, n_trials):

        study = optuna.create_study()
        study.optimize(self.objective, n_trials=n_trials)

        return study
