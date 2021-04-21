import os
import re
import data_accessor as da

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TABLE_NAME = os.getenv('TABLE_NAME')
REGION_NAME = os.getenv('REGION_NAME')

bot = commands.Bot(command_prefix='!')
data_accessor = da.DataAccessor(TABLE_NAME, REGION_NAME)

def validate_drive_args(args):
    if len(args) != 2:
        return "Error. Please format your input correctly: !drive [CLASS] [CODE]\nExample usage: !drive CSE 320"

    if not args[0].isalpha():
        return "Error. Class should be only composed of letters"

    if not re.search("\d{3}", args[1]):
        return "Error. Class code should be a three digit number"

    return None

"""
insert docs here xd
arg1 = class code
arg2 = class number
"""
@bot.command(name='drive', help='Provides google drive link of desired class')
async def drive_cmd_handler(ctx, *args):
    response = "If you see this msg, something went very wrong..."
    invalid = validate_drive_args(args)
    if not invalid:
        # args[0] and args[1] are both valid format
        value = args[0].upper() + ' ' + args[1]
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
    else:
        response = invalid
    await ctx.send(response)

bot.run(TOKEN)