from sys import argv
from .setup.injector import Injector

if __name__ == '__main__':

    if len(argv) < 2:

        raise ValueError("You need to provide at least a path to a configuration file")

    config_filename = argv[1]
    builder = Injector(config_filename)
    tabu_search = builder.create_tabu_search()
    tabu_search.tabu_search()
