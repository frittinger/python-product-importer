import boto3
from productsimporter.parser import xmlparser

s3client = boto3.client(
    's3',
    region_name='us-east-1'
)

# These define the bucket and object to read
bucketname = 'net-schnegg-import'
file_to_read = 'simple.xml'

# Create a file object using the bucket and object key.
fileobj = s3client.get_object(
    Bucket=bucketname,
    Key=file_to_read
)
# open the file object and read it into the variable filedata.
filedata = fileobj['Body'].read()

#
# # Once decoded, you can treat the file as plain text if appropriate
# print(contents)
xmlparser.parse_xml(filedata)
