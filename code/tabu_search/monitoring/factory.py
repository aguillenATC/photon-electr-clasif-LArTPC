from .base import Monitor
from .monitors import TimeMonitor, EnergyMonitor

class MonitorFactory:

    monitor_mapping = {"time": TimeMonitor,
                        "energy": EnergyMonitor}

    @classmethod
    def create_monitor(cls, type, parameters = {}) -> Monitor:

        return cls.monitor_mapping[type](**parameters)
