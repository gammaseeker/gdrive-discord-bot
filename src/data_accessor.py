"""Data accessor for dynamoDB

"""

import boto3

s3 = boto3.resource('s3')

class DataAccessor:
    """Class to setup client to connect to dynamoDB"""

    def __init__(self, table_name, region_name):
        # Creating the DynaoDB Client
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)

        # Creating the DynamoDB Table Resource
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)
        self.table_name = table_name

    def get_item(self, key, value):
        try:
            record = self.table.get_item(
                TableName=self.table_name,
                Key={
                    key: value
                }
            )
        except Exception:
            raise Exception
        return record
    
    def update_item(self, key, value, new_link):
        record = self.table.get_item(
            TableName=self.table_name,
            Key={
                key: value
            }
        )
        if 'Item' in record:
            # Record exists, update record
            try:
                response = self.table.update_item(
                    TableName=self.table_name,
                    Key={
                        key: value
                    },
                    UpdateExpression="set link=:l",
                    ExpressionAttributeValues={
                        ':l': new_link
                    },
                    ReturnValues="UPDATED_NEW"
                )
            except Exception:
                raise Exception
        else:
            # Record doesn't exist yet, insert new record
            try:
                response = self.table.put_item(
                    TableName=self.table_name,
                    Item={
                        "class_name": value, 
                        "link": new_link  
                    }
                )
            except Exception:
                raise Exception
        return response