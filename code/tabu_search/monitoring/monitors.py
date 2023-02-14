import os
import json
import random
import subprocess
from time import time
from .base import Monitor

class TimeMonitor(Monitor):

    def __init__(self, time_tracker: str):

        self.time_tracker: dict[str, str] = self._parse_target_tracker(time_tracker)

    def start(self) -> None:

        self.start_time: float = time()

    def stop(self) -> None:

        elapsed: float = time() - self.start_time
        self.__save_elapsed_time(elapsed)

    def __save_elapsed_time(self, elapsed: float) -> None:

        self.create_tracker(self.time_tracker["group"], self.time_tracker["tracker"], "time")
        self.trackers[self.time_tracker["group"]][self.time_tracker["tracker"]].append(elapsed)

class EnergyMonitor(Monitor):

    def __init__(self, user: str, device: str, energy_tracker: str, power_tracker: str = None):

        self.user = user
        self.device = device
        self.energy_tracker: dict[str, str] = self._parse_target_tracker(energy_tracker)
        self.power_tracker: dict[str, str] = self._parse_target_tracker(power_tracker)
        self.experiment_id: str = hex(random.getrandbits(64))[2:]
        self.environ = os.environ.copy()

    def start(self) -> None:

        vampire_start: str = r"vampire {command} -u {user} -e {experiment}".format(command = "start",
                                                                                            user = self.user,
                                                                                            experiment = self.experiment_id)
        subprocess.run(["bash", "-c", vampire_start], stdout = subprocess.PIPE, env = self.environ)

    def stop(self) -> None:

        vampire_stop: str = r"vampire {command} -u {user} -e {experiment}".format(command = "stop",
                                                                                            user = self.user,
                                                                                            experiment = self.experiment_id)
        subprocess.run(["bash", "-c", vampire_stop], stdout = subprocess.PIPE, env = self.environ)

        self.__save_consumed_energy()
        self.__save_instantaneous_power()

    def __save_consumed_energy(self) -> None:

        vampire_energy: str = r"vampire {command} -u {user} -e {experiment} -d {devices}".format(command = "energy",
                                                                                                 user = self.user,
                                                                                                 experiment = self.experiment_id,
                                                                                                 devices = self.device)
        completed = subprocess.run(["bash", "-c", vampire_energy], stdout = subprocess.PIPE, env = self.environ)
        result: str = completed.stdout.decode("UTF-8")
        consumed_energy = json.loads(result)[self.device]

        self.create_tracker(self.energy_tracker["group"], self.energy_tracker["tracker"], "energy")
        entry: dict = {"acc_energy": consumed_energy, "experiment_id": self.experiment_id}
        self.trackers[self.energy_tracker["group"]][self.energy_tracker["tracker"]].append(entry)

    def __save_instantaneous_power(self) -> None:

        vampire_get: str = r"vampire {command} -u {user} -e {experiment} -d {devices}".format(command = "get",
                                                                                              user = self.user,
                                                                                              experiment = self.experiment_id,
                                                                                              devices = self.device)
        completed = subprocess.run(["bash", "-c", vampire_get], stdout = subprocess.PIPE, env = self.environ)
        result: str = completed.stdout.decode("UTF-8").split("\n")
        rows = [i.split(",") for i in result][:-1]
        col_names = rows[0]

        self.create_tracker(self.power_tracker["group"], self.power_tracker["tracker"], "power")

        for measure in rows[1:]:

            entry = dict(zip(col_names, measure))
            self.trackers[self.power_tracker["group"]][self.power_tracker["tracker"]].append(entry)
