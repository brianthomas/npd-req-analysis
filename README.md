# NASA NPD Requirements Analysis Project 

## About

This project is for developing code to allow us to calculate a variety
of metrics between various NPD/NPR requirements so we may use a 
quantitative means to determine which of these stated 
requirements are similar to other requirements in the same and other 
NPD/NPRs.

Currently only Damerau-Levenshtein (DL) and normalized DL is implemented.

Contact: brian.a.thomas@nasa.gov


## Loading/Installation

This project is designed and tested against Python 3.

An installation script is provided in this distribution and resides
in the bin directory. There are any number of ways to set up your
python environment, my preferred one (described below) is using
[virtualenv](https://pypi.python.org/pypi/virtualenv).

```bash
# clone this repository to your local machine
git clone https://github.com/brianthomas/npd-req-analysis.git

# switch to the local repository dir
cd npd-req-analysis

# install virtualenv environment for python3
virtualenv -p <python_3_exe> ./env

# activate your environment
source env/bin/activate.sh

# install requirements
pip install -r requirements.txt

#add aggregate dictionary code to python path 
export PYTHONPATH=`pwd`

# run the NDL algorithm on the excel spreadsheet data
# note that the spreadsheet was handbuilt by policy folks
python bin/find_dl_distance.py -f data/*.xlsm

```

