"""gdrive bot source code

This bot is designed to fetch the google drive link for a course according to
arguments passed in by the user.
"""

import os
import re
import data_accessor as da

from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
from const import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TABLE_NAME = os.getenv('TABLE_NAME')
REGION_NAME = os.getenv('REGION_NAME')

bot = commands.Bot(command_prefix='!')
data_accessor = da.DataAccessor(TABLE_NAME, REGION_NAME)

def validate_drive_args(arg_ctr, args):
    if len(args) != arg_ctr:
        return ARG_CTR_ERROR

    if not args[0].isalpha():
        return ARG_ALPHA_ERROR

    if not re.search("\d{3}", args[1]):
        return ARG_CODE_ERROR

    return None

"""Handler function for the !drive command. 

This command accepts two args
arg1 = class code
arg2 = class number

Example usage: !drive CSE 320
"""
@bot.command(name='drive', help='Provides google drive link of desired class')
async def drive_cmd_handler(ctx, *args):
    response = DEFAULT_RESPONSE    
    invalid = validate_drive_args(2, args)
    if not invalid:
        # args[0] and args[1] are both valid format
        course = args[0].upper() + ' ' + args[1]
        try:
            record = data_accessor.get_item(key='class_name', value=course)
            response = record['Item']['link']
        # This exception is triggered bc 'Item' does not exist in record
        except Exception as e:
            response = f"Sorry looks like the google drive for {course} doesn't exist \nContact @joeyjiem if you think this is a mistake"
    else:
        response = invalid
    await ctx.send(response)

"""Handler function for the !update command. 

This command accepts two args
arg1 = class code
arg2 = class number
arg3 = google drive link

Example usage: !update CSE 320 google.com
"""
@bot.command(name='update', help='Updates google drive link of specified class')
async def update_cmd_handler(ctx, *args):
    response = DEFAULT_RESPONSE
    invalid = validate_drive_args(3, args)
    if not invalid:
        course = args[0].upper() + ' ' + args[1]

        try:
            data_accessor.update_item(key='class_name', value=course, new_link=args[2])
            response = f"{course} google drive link updated successfully to {args[2]}"
        # This exception is triggered bc 'Item' does not exist in record
        except Exception as e:
            response = f"Error could not update link for {course}\nContact @joeyjiem"

    else:
        response = invalid

    await ctx.send(response)

@bot.command(name='kill', help='Shuts down bot')
@has_permissions(administrator=True)
async def _kill_cmd_handler(ctx):
    await ctx.send('Bot shutting down')
    await bot.close()

@_kill_cmd_handler.error
async def kill_cmd_handler_error(ctx, error):
    if isinstance(error, MissingPermissions):
        response = f"Sorry {ctx.message.author}, you do not have permissions to do that."
        await ctx.send(response)

bot.run(TOKEN)