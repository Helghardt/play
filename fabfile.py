from etc.fabric_tasks import *


def test():
    # run('echo Hello, World!')
    print(env.project_name)


def loaddata():
    manage('loaddata '
           'input_types.json ')
