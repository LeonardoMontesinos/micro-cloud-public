import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from utils_response import ok, error

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTOS_TABLE'])

def get_tenant(event):
    qp = event.get('queryStringParameters') or {}
    return qp.get('tenantId')

def get_all_products(event, context):
    tenant_id = get_tenant(event)
    if not tenant_id:
        return error("Falta el parametro tenantId en la URL", 400)

    try:
        response = table.query(
            KeyConditionExpression=Key('tenant_id').eq(tenant_id)
        )
        return ok(response.get('Items', []))
    except Exception as e:
        return error(str(e), 500)

def get_products_by_category(event, context):
    tenant_id = get_tenant(event)
    if not tenant_id:
        return error("Falta el parametro tenantId", 400)
        
    categoria = event['pathParameters']['categoria']

    try:
        response = table.query(
            KeyConditionExpression=Key('tenant_id').eq(tenant_id),
            FilterExpression=Attr('categoria').eq(categoria)
        )
        return ok(response.get('Items', []))
    except Exception as e:
        return error(str(e), 500)

def get_product_by_id(event, context):
    tenant_id = get_tenant(event)
    if not tenant_id:
        return error("Falta el parametro tenantId", 400)

    product_id = event['pathParameters']['id']

    try:
        response = table.get_item(
            Key={'tenant_id': tenant_id, 'producto_id': product_id}
        )
        item = response.get('Item')
        
        if not item:
            return error("Producto no encontrado", 404)
            
        return ok(item)
    except Exception as e:
        return error(str(e), 500)
