import os
import data_accessor as da

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TABLE_NAME = os.getenv('TABLE_NAME')
REGION_NAME = os.getenv('REGION_NAME')

bot = commands.Bot(command_prefix='!')
data_accessor = da.DataAccessor(TABLE_NAME, REGION_NAME)

"""
insert docs here xd
arg1 = class code
arg2 = class number
"""
@bot.command(name='drive', help='Provides google drive link of desired class')
async def drive_cmd_handler(ctx, arg1, arg2):
    #TODO need to regex arg2 is a 3 digit number
    response = "If you see this msg, something went very wrong..."
    value = arg1.upper() + ' ' + arg2
    try:
        record = data_accessor.get_item(key='class_name', value=value)
        response = record['Item']['link']
    # This exception is triggered bc 'Item' does not exist in record
    except Exception as e:
        response = f"Error requested course google drive not found\nContact @joeyjiem"
    '''
    except DynamoDB.Client.exceptions.ProvisionedThroughputExceededException:
        response = "ProvisionedThroughputExceededException contact Joey Jiemjitpolchai"

    except DynamoDB.Client.exceptions.ResourceNotFoundException:
        response = "ResourceNotFoundException contact Joey Jiemjitpolchai"

    except DynamoDB.Client.exceptions.RequestLimitExceeded:
        response = "RequestLimitExceeded contact Joey Jiemjitpolchai"

    except DynamoDB.Client.exceptions.InternalServerError:
        response = "InternalServerError contact Joey Jiemjitpolchai"
    '''
    await ctx.send(response)

bot.run(TOKEN)