# %% [markdown]
# # What this script does? 
# 
# ### About the project 
# 
#  Salesforce is greate at managing customer data, but it is not that good for the data team. good that salesforce offers effencient APIs that can access and control the objects in a salesforce organizaiotn. In this project, I will connect to salesforce imaginary organization namly "Sa-mA Properties".  
# 
#  ### Salesforce Org
# I created salesforce developer account and created some object for this project. I imported the data in the included CSV files to salesforce. 
# 
# ### Goal 
# Connect salesforce organizaiont and fetch the data object into python data frames and do some data analysis. 
# 
# ### Data 
# All the data in this project is created by me using excel random funciton and some entities names from the internet.
# 
# ### Output 
# The script shall generate. 
# - first, to create a csv file contain all the objects (created by salesforce developer).
# - second, to take one of the objects as example and export it as csv file. 

# %% [markdown]
# ## Setup
# 
# simple-salesforce is a library can work fairly good with salesforce. if first time removing the # in line 1 installs the simple-salesforce library
# 
# ### The Salesforce Credentials
# the salesforce accesss credentials are saved in a json file in the same project directory named "login.json".

# %%
# %pip install simple-salesforce
# %pip install pandas

from simple_salesforce import Salesforce, SFType, SalesforceLogin
import json
import pandas as pd
import csv

# %% [markdown]
# ## Connect to Salesfroce
# create salesfoce connection 

# %%
# Log to salesforce
loginInfo = json.load(open('login.json'))
Username = loginInfo['username']
password = loginInfo['password']
security_token = loginInfo['security_token']
domin = 'login'

session_id, instance = SalesforceLogin(
    username=Username, password=password, security_token=security_token, domain=domin)

sf = Salesforce(instance=instance, session_id=session_id)
sf

# %% [markdown]
# ## Print connection details
# the connection detils fetches the salesforce organization details

# %%
# print sessoin details
for element in dir(sf):
    if not element.startswith('_'):
        if isinstance(getattr(sf, element), str):
            print('Property Name:{0}; Value: {1}'.format(
                element, getattr(sf, element)))

# %% [markdown]
# ## Print domin 

# %%
# print domain name
print(instance)

# %% [markdown]
# ## Print and Export the object to CSV
# Sales force creates automatlically tons of tables for serving meta data for the data sets. luckily they rename each object (table) name by addig "__c" and also the user fields (columns) by adding the same trailing letters "__c". relying on this I will print each object and within it each fields ends with "__c"
# the data of this code block should be the object by the developer in salesforce.

# %%
# Get the list of objects (tables) in the Salesforce database
objects = sf.describe()['sobjects']

# Create variable to store the output file name
output_file = 'salesforce_tables_and_fields.csv'

# Open the CSV file in write mode
with open(output_file, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write the header row
    csvwriter.writerow(['Table Name', 'Field Name'])

    # Iterate over the objects
    for obj in objects:
        table_name = obj['name']

        # Check if the table name is a custom object (ends with '__c')
        if table_name.endswith('__c'):
            # Get fields for the current table
            fields = sf.__getattr__(table_name).describe()

            # Write the table name to the CSV file
            csvwriter.writerow([table_name, ''])

            # Print the table name
            print(f"Table Name: {table_name}")

            # Write field names to the CSV file and print them
            for field in fields['fields']:
                field_name = field['name']
                if field_name.endswith('__c'):
                    csvwriter.writerow(['', field_name])
                    print(f" \tField Name: {field_name}")

# print a confirmation message
print(
    f"Table names and fields for custom objects have been written to {output_file}.")

# %% [markdown]
# ## Fetching a Specific object (table) data
# one of the object in my data is off_days which is a list of the off holdays such as week-ends, holidays, etc. 

# %%
# Get the offdays table and fields
soql = 'SELECT off_date__c, off_details__c FROM off_days__c'
output_tasks = sf.query(query=soql)

# Extract records and fields
records = output_tasks['records']

# Create a list of dictionaries for each record
data = [{'off_date': record['off_date__c'],
         'off_details': record['off_details__c']}
        for record in records]

# Create a DataFrame
df_offdays = pd.DataFrame(data)
df_offdays

# Export to CSV
df_offdays.to_csv('tbl_offdays.csv', index=False)

# %% [markdown]
# ## Terminate the Salesfrce connection season

# %%
# end session
session_id = None
instance = None

# %% [markdown]
# * The script has run successfully and the list of tables in the salesforce database the table off days are saved in the same directory as csv fiels. 


