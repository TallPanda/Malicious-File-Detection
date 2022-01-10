Malicious File Detection
College project to create a Malicious File Detection tool utilising the Virus Total API and the NIST NSRL Database


Setup
pip install the requirements from requirements.txt
# pip install -r requirements.txt

Inside the config/mysql/secure/ folder copy the default.login.json to a login.json file and fill in your details for your mysql server with a benign file database
# We used the NIST NSRL database for ours
A mysqlsetup.sql is provided if you are using the nsrl database. It is presumed that you are using the unique database but in its nameing constraints however any NSRLFile.txt file can be used
You will be required to change [["location of your NSRLFile.txt"]] to the location of your NSRLFile.txt inside the mysqlsetup.sql to use it