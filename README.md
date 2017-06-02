# NASA NPD Requirements Analysis Db

## About

This project is for developing a database to allow us to calculate the
Levenshtein distance metric between various NPD/NPR requirements so we
may use a quantitative means to determine which of these stated 
requirements are similar to other requirements in the same and other 
NPD/NPRs.

Contact: brian.a.thomas@nasa.gov


## Loading/Installation

This project is designed and tested against Python 3. You will also need
to have postgresql 9.x installed on your target machine. 

An installation script is provided in this distribution and resides
in the bin directory. There are any number of ways to set up your
python environment, my preferred one (described below) is using
[virtualenv](https://pypi.python.org/pypi/virtualenv).

```bash
# clone this repository to your local machine
git clone https://github.com/brianthomas/ocio-finance-db.git

# switch to the local repository dir
cd npd-req-analysis-db

# install virtualenv environment for python3
virtualenv -p <python_3_exe> ./env

# activate your environment
source env/bin/activate.sh

# install requirements
pip install -r requirements.txt

#add aggregate dictionary code to python path 
export PYTHONPATH=`pwd`

# create the database
createdb npdreq 

# initialize the schema
psql -d npdreq -U postgres -f schema/db.psql

# load the excel spreadsheet data into the postgresql db. 
python bin/loader.py -d 'postgresql://postgres@localhost:5432/npdreq' -f data/*.xlsm

# run the analysis (a stored procedure)
psql -d npdreq -U postgres -f schema/run_analysis.psql

```

