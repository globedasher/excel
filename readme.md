### excel.py used to run a query against every DB in the host cluster

1. `git clone https://github.com/globedasher/excel`
1. Install a virtual environment (on linux install `virtualenv`) 
1. Run `virtualenv <env>` in the repo root

   NOTE: I use `env` for my `<env>` environment folder name as it makes things smooth when working with Python. Not using a virtual environment can cause conflicts between modules installed and OS used modules.

1. Run `source <env>/bin/activate` to activate the virtual environment.
1. Run `pip install -r requirements.txt` to install module dependencies.
1. Run `python py_migrate.py` and proide information at the prompts.
