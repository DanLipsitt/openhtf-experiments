# OpenHTF experiments

## Running

To create an activate a virtualenv with the required dependencies:

``` shell
pip install pipenv
pipenv install
pipenv shell
```

## Comparing OpenHTF versions

Tox lets you run a script in multiple environments, described in
[tox.ini](./tox.ini) and specified with the `-e` flag.

``` shell
tox  -e py27-htf_snapshot --run-command "python {toxinidir}/script.py"
tox  -e py27-htf_v110     --run-command "python {toxinidir}/script.py"
```

Or run in all environments sequentially:
``` shell
tox --run-command "python {toxinidir}/script.py"
```
