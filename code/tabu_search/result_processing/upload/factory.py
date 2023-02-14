from ..base import Syncer
from .syncers import GithubSyncer

class SyncerFactory:

    syncer_mapping = {"github": GithubSyncer}

    @classmethod
    def create_syncer(cls, type, parameters = {}) -> Syncer:

        return cls.syncer_mapping[type](**parameters)
