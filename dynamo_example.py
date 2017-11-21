import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
table = dynamodb.create_table(
        TableName='users2',
        KeySchema=[
            {
                'AttributeName':'username',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName':'username',
                'AttributeType': 'S'
                }
        ],
        ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
        }
    )

table.meta.client.get_waiter('table_exists').wait(TableName='users')

print(table.item_count)
