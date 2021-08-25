###
# Código usado para subir função para Lambda
# Autoria de Carlos Dip
###

###
# Code used to upload a function to Lambda
# Made by Carlos Dip
###

import boto3
from botocore.config import Config
from zipfile import ZipFile

# Cria cliente boto3
# Creates boto3 Client
my_config = Config(retries={'max_attempts': 0}, read_timeout=840, connect_timeout=600, region_name="us-east-2")
client = boto3.client('lambda', config=my_config)

# Zipa código da função
# Zip function code
with ZipFile("lambda_function.zip", "w") as zipper:
    zipper.write("lambda_function.py")

# Sobe zip para Lambda
# Upload
with open("lambda_function.zip", "rb") as newFunc:
    client.update_function_code(FunctionName='arn:aws:lambda:us-east-2:461597312227:function:example', ZipFile=newFunc.read())

print("Done")