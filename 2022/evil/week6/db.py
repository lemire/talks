
with open("secret.txt", "r") as file:
    secret = file.read().strip()

import boto3
dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIAWTSKHA76FSSB2Z7S", aws_secret_access_key=secret, region_name="ca-central-1" )
tables = list(dynamodb.tables.all())
print("tables=",tables)

evil = dynamodb.Table("evil_locations")
print(evil)

response = evil.scan()
print(response)

lat = 45.54187056861444
long = -73.48202822340973

import uuid
myuuid = uuid.uuid4()


print(response)
response = evil.put_item(
    Item={
        'locationid': str(myuuid),
        'latitude': str(lat),
        'longitude': str(long),
    }
)
# botocore.exceptions.ClientError: An error occurred (ValidationException) when calling the PutItem operation: One or more parameter values were invalid: Missing the key locationid in the item
response = evil.scan()
print(response["Items"])