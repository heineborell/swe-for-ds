# Dependency management

## Use a requirements file

Setup `requirements.txt` with any requirements that
are explicitly imported and not part of the standard
python library.

Can install using `pip` via

```bash
pip install -r requirements.txt
```

## Use conda

Assuming you have `conda` intalled, you can use
`conda activate` to start your defualt conda environment.

To build a new environment:

```bash
conda create -n erdos python=3.10 scikit-learn jupyter
conda activate erdos
```

You can then `conda install` or `pip install` just to 
this specific environment.

To save the environment:

```bash
conda env export | grep "^prefix: " > environment.yaml
```

It can then be installed via

```bash
conda env create -f environment.yaml
```

To see all environments:

```bash
conda env list
```

and to deactivate run

```bash
conda deactivate
```

### Installing into jupyter

Run the following to make a kernel available iwthin jupyter notebooks that matches your conda environment

```bash
conda activate erdos
conda install jupyter
python -m ipykernel install --user --name erods
jupyter notebook
```


## Use pyenv and virtual environments


### pyenv for python version

Install `pyenv` and then see what verions are available

```bash
pyenv versions
```

To see what is installed

```bash
pyenv install --list
```

and then install with

```bash
pyenv install 3.10.6
```

Set the global version with

```bash
pyenv global 3.10.6
```

and set a local (folder and sub-folder specific) version with

```bash
pyenv local 3.9.7
```

### Use venv for dependencies

Create a virtual environment in a `.venv/` directory in your current directory and activate it with

```bash
python -m venv .venv
source .venv/bin/activate
```

Then pip install as before, can use `requirements.txt`. Deactivate with

```bash
deactivate
```

#### Installing into jupyter

Same as above but with the virtual environment activated instead of the conda environment.


## Other requirements

Make sure to write down in the `README.md` what needs to happen to create
the development environment. In particular, some python packages, such as `psycopg2` require other
things to be installed, e.g., postgres. Make sure to make a note of these.
