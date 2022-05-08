
with open("secret.txt", "r") as file:
    secret = file.read().strip()

import boto3
dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIAWTSKHA76FSSB2Z7S", aws_secret_access_key=secret, region_name="ca-central-1" )
#print(dynamodb.list_tables()["TableNames"])
tables = list(dynamodb.tables.all())
print("tables=",tables)

evil = dynamodb.Table("evil_locations")
print(evil)

response = evil.scan()
print(response)
#import json
#response = json.loads(evil.scan())
#print(response)
#data = response['Items']

#while 'LastEvaluatedKey' in response:
#    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
#    data.extend(response['Items'])
lat = 45.54187056861444
long = -73.48202822340973
#import struct

# define double_to_hex (or float_to_hex)
#def double_to_hex(f):
#    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])
#print(double_to_hex(lat))
#print(double_to_hex(long))

#key = double_to_hex(lat)+double_to_hex(long)
import uuid

myuuid = uuid.uuid4()
from decimal import Decimal

#response = evil.put_item(
#    Item={
#        'latitude': str(lat),
#        'longitude': str(long),
#    }
#)
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