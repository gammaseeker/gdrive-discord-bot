import boto3

s3 = boto3.resource('s3')

class DataAccessor:
    def __init__(self, table_name, region_name):
        # Creating the DynaoDB Client
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)

        # Creating the DynamoDB Table Resource
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = dynamodb.Table(table_name)
        self.table_name = table_name

    def get_item(self, key, value):
        try:
            record = self.table.get_item(
                TableName=self.table_name,
                Key={
                    key: value
                }
            )
        except DynamoDB.Client.exceptions.ProvisionedThroughputExceededException:
            raise DynamoDB.Client.exceptions.ProvisionedThroughputExceededException

        except DynamoDB.Client.exceptions.ResourceNotFoundException:
            raise DynamoDB.Client.exceptions.ResourceNotFoundException

        except DynamoDB.Client.exceptions.RequestLimitExceeded:
            raise DynamoDB.Client.exceptions.RequestLimitExceeded

        except DynamoDB.Client.exceptions.InternalServerError:
            raise DynamoDB.Client.exceptions.InternalServerError

        return record