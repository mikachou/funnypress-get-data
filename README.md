# Funny Press : get data

## Overview

Funny Press project purpose is to detect funny articles titles.
These script help to acquire data to feed machine-learning models.

The scripts in `get_full_articles/` directory downloads full articles and put them in CSV stored in `exports/` directory.
The scripts in `get_titles/` directory downloads only and put them in CSV stored in `exports/` directory.

## Requirements

The following install procedure requires `pyenv` and its plugin `pyenv-virtualenv`. Check eventually their repo to see how to install them

* pyenv : https://github.com/pyenv/pyenv
* pyenv-virtualenv : https://github.com/pyenv/pyenv-virtualenv

## Install

1. clone the repository

```
$ git clone https://github.com/mikachou/house-prices
```

Then enter the folder
```
$ cd house-prices
```

2. install right python version with pyenv :
```
$ pyenv local
```

You may check that you have install the right python version

```
$ python -V
Python 3.12.6
```

In case right python version is not intall, type the following command
```
$ pyenv install
```

Create a virtualenv for this project

```
$ pyenv virtualenv funnypress-get-data
```

Enter in the just created virtualenv

```
$ pyenv activate funnypress-get-data
```

3. install required packages
```
$ pip install -r requirements.txt
```


## Usage

Once in Virtualenv execute python scripts to extract texts from the sources, e.g :
`python get_full_articles/gorafisation.py`
to get full articles

or
`python get_titles/gorafisation.py`
to get only titles