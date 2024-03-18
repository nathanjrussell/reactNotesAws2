import json
import boto3
client = boto3.client('dynamodb')

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

def isValueValidMenuOption(submenuList, value):
    for entry in submenuList:
        if entry['value'] == value:
            return True
    return False

def getMenuItems(menu_name):
    GetItem = client.get_item(
        TableName='reactNoteSubjectMenus',
        Key={
            'menu_name': {
                'S': menu_name
            }
        }
    )

    # Extract the item from the response
    
    return remove_types(GetItem['Item']['submenu'])
    
def getNextMenu(previous_menu_list, menu_name):
    if (menu_name is None):
        return getMenuItems(previous_menu_list[0]['value'])
    if (isValueValidMenuOption(previous_menu_list, menu_name)):
        return getMenuItems(menu_name)
    return getMenuItems(previous_menu_list[0]['value'])


def lambda_handler(event, context):
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