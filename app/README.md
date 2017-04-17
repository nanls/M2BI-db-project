# 

This is a database for the analysis of polyproline helix structure. 

## Setup

0. Get files

		$git clone https://github.com/Athenais/M2BI-db-project.git
		$cd M2BI-db-project/app

1. Install virtualenv

		$sudo pip3 install virtualenv

2. Create virtual environment

		$virtualenv -p /usr/bin/python3 venv

3. Activate virtualenv

		$source venv/bin/activate

4. Install requirements

		$pip install -r requirements.txt
		

5. Setup the tools

		$chmod u+x setup-tools.sh
		$ ./setup-tools.sh

6. Initialize database de novo : 
/!\ this will delete previous database

		$rm data.db
		$python setup-db.py

6'. Or initialize database using pdb in data dir :
		
		$python fetch-pdbs-from-PICSES-list.py -l tools/cullpdb_pc90_res1.8_R0.25_d120106_chains8017
		$python fill-db-using-data-dir.py



7. Quit virtualenv

		$deactivate


## Usage

1. Update project repository

		$git pull

2. Activate virtualenv

		$source venv/bin/activate

3. Update requirements

		$pip install -r requirements.txt

# if not already created
# 4. Creation of the database
	
#		$python setup-db.py

5. Run Python webserver

		$python __init__.py

6. Open web browser at <http://127.0.0.1:5000/>

7. Test it

8. Kill web app

		$ctrl-c

9. Quit virtualenv

		$deactivate
