import json

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps({
            'message': 'Hello from AWS Lambda!',
            'status': 'success',
            'service': 'autou-email-classifier'
        })
    }

# Alias for WSGI compatibility
app = lambda_handler