import json
import boto3
client = boto3.client('dynamodb')

# Remove the DynamoDB types and return the data as a list of dictionaries
def remove_types(d):
    if isinstance(d, dict):
        if 'S' in d:
            return d['S']
        elif 'L' in d:
            return [remove_types(x) for x in d['L']]
        elif 'M' in d:
            return {k: remove_types(v) for k, v in d['M'].items()}
        else:
            return {k: remove_types(v) for k, v in d.items()}
    else:
        return d

# Check if the value is contained in the upper level menu
def isValueValidMenuOption(submenuList, value):
    for entry in submenuList:
        if entry['value'] == value:
            return True
    return False

# Get the menu items for the given menu name
def getMenuItems(menu_name):
    GetItem = client.get_item(
        TableName='reactNoteSubjectMenus',
        Key={
            'menu_name': {
                'S': menu_name
            }
        }
    )
    return remove_types(GetItem['Item']['submenu'])
    
# Get the next menu items for the given menu name
def getNextMenu(previous_menu_list, menu_name):
    if (menu_name is None):
        return getMenuItems(previous_menu_list[0]['value'])
    if (isValueValidMenuOption(previous_menu_list, menu_name)):
        return getMenuItems(menu_name)
    return getMenuItems(previous_menu_list[0]['value'])


def lambda_handler(event, context):
    # queryStringParameters is not part of event dict if there are no query parameters
    queryStringParameters = event.get('queryStringParameters',None)
    if queryStringParameters is None:
        general = 'general'
        subject = None
        category = None
        subcategory = None
        topic = None
    else:
        #only the first one needs a default value
        general = event['queryStringParameters'].get('general','general')
        subject = event['queryStringParameters'].get('subject',None)
        category = event['queryStringParameters'].get('category',None)
        subcategory = event['queryStringParameters'].get('subcategory',None)
        topic = event['queryStringParameters'].get('topic',None)
    
    data = {}

    data['general'] = getMenuItems(general)
    data['subject'] = getNextMenu(data['general'],subject)
    data['category'] = getNextMenu(data['subject'],category)
    data['subcategory'] = getNextMenu(data['category'],subcategory)

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(data)
    }

    return response