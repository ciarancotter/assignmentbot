#Assignment Bot
#Imports
import os
import json
import time
import base64
import discord
import requests
import pandas as pd
from datetime import datetime, date
from discord.ext import commands

#Variables
coreModules = {
    'XXXXX': XXXXX,
    'XXXXX' : XXXXX,
    'XXXXX' : XXXXX,
    'XXXXX' : XXXXX
}

def fetchAssignments(assigner):
    query = ("""query courseInfo($assignmentID: ID = %s) {
  assignment(id: $assignmentID) {
    name
    dueAt
  }
  }"""%(assigner))
    return query

def getAssignments(module):
    assignments = []
    query = ("""query courseInfo($courseId: ID = %s) {
        course(id: $courseId) {
            assignmentsConnection {
            edges {
                node {
                id
                }
            }
            }
        }
        }"""%(coreModules[module]))
    url = 'https://ucc.instructure.com/api/graphql'
    r = requests.post(url, json = {'query': query}, headers = {'Authorization': 'Bearer *insert access token here*'})
    
    #Data processing
    jsonData = json.loads(r.text)['data']['course']['assignmentsConnection']['edges']
    for i in jsonData:
        nodeVal = i['node']
        idVal = nodeVal['id']
        decodedBytes = base64.b64decode(idVal)
        decodedStr = str(decodedBytes, "utf-8")
        cleanedStr = decodedStr.replace('Assignment-', "")
        assignments.append(cleanedStr)
    return assignments

def formatTime(thisTime):

    if thisTime == 'N/A':
        return 'N/A'
    
    else:
        playTime = thisTime.split('T')
        y1 = playTime[0].split("-")
        reformatted = str(y1[2]) + "/" + str(y1[1]) + "/" + str(y1[0])
        return reformatted

client = commands.Bot(command_prefix = 'b!')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('Now this is actually based.'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('No command found.')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange(),
        title = "Based Assignment Bot Help"
    )

    embed.add_field(name = 'Commands', value = 'due <module> [XXXXX, XXXXX, XXXXX, XXXXX]', inline = False)

    await ctx.send(embed=embed)

@client.command()
async def due(ctx, myModule : str):
    
    assignments = getAssignments(myModule)
    returnStr = ""
    today = date.today().strftime("%d/%m/%Y")

    for assignment in assignments:
        
        #Get the data
        query = fetchAssignments(assignment)
        url = 'https://ucc.instructure.com/api/graphql'
        r = requests.post(url, json = {'query': query}, headers = {'Authorization': 'Bearer *insert access token here**'})
        jsonData = json.loads(r.text)['data']['assignment']
        jsonData = dict(jsonData)

        if jsonData['dueAt'] == None:
            jsonData['dueAt'] = 'N/A'

        dueDate = formatTime(jsonData['dueAt'])
        if dueDate != 'N/A':
            dueTime = datetime.strptime(dueDate, '%d/%m/%Y')
            todayTime = datetime.strptime(today, '%d/%m/%Y')
            daysLeft = (dueTime - todayTime).days

            if dueTime >= todayTime:
                daysLeft = (dueTime - todayTime).days
                res = "**" + jsonData['name'] + "**" + " | " + "Due Date: " + dueDate + " | " + "Days Left: " + str(daysLeft) + "\n" 
                returnStr += res

                
    if len(returnStr) == 0:
        returnStr = 'There are no assignments due for ' + str(myModule) +"."

    await ctx.send(returnStr)

client.run('XXXXX')
