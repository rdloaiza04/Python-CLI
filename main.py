import click
import requests
from datetime import datetime
from songs import Songs
import re


# API URL'S
urlMon = "https://de-challenge.ltvco.com/v1/songs/monthly"
urlDay = "http://de-challenge.ltvco.com/v1/songs/daily"
api_key = 'ec093dd5-bbe3-4d8e-bdac-314b40afb796'

# Input Validation
def turnSeconds(time):
    print(time)
    listNum = re.findall(r'\d+', time)
    lengthList = len(listNum)
    if (lengthList == 3):
        hoursToSeconds = int(listNum[0]) * 3600
        minutesToSeconds = int(listNum[1]) * 60
        newSeconds = (int(listNum[2])+hoursToSeconds+minutesToSeconds)
        return newSeconds
    elif (lengthList == 2):
        minutesToSeconds = int(listNum[0]) * 60
        newSeconds = (int(listNum[1])+minutesToSeconds)
        return newSeconds

    elif (lengthList == 1):
        newSeconds = (int(listNum[0]))
        return newSeconds

    else:
        return 0

'''
Checks for the inputed data in the month parameter
ctx and params are requiered for the functionality of the callback
I: ctx (context), params(parameters), value(inputed value)
O: None
'''
def monthRegex(ctx, params, value):
    regex = r'(\d{4})-(\d{2})'
    if re.match(regex, value):
        return value
    else:
        raise click.BadParameter(
            'The format of the month for searching is: YYYY-MM')

'''
Checks for the inputed data in the day parameter
ctx and params are requiered for the functionality of the callback
I: ctx (context), params(parameters), value(inputed value)
O: None
'''
def dayRegex(ctx, params, value):
    regex = r'(\d{4})-(\d{2})-(\d{2})'
    if re.match(regex, value):
        return value
    else:
        raise click.BadParameter(
            'The format of the month for searching is: YYYY-MM-DD')

####CRUD####
'''
Insert or update the data in the database, with the data received from the API
I: data(json)
O: None
'''
def insertDB(data):
    # The function .isoformat(sep=' ', timespec='milliseconds') parse the received timestamp from released_at and last_played_at into ISO8601, with milliseconds
    global_rank = 0
    last_played_at = "0000-00-00T00:00:00.00"
    times_played = 0
    try:
        if(data["stats"]):
            global_rank = data['stats']['global_rank']
            last_played_at = datetime.fromtimestamp((data['stats']['last_played_at']//10**9)).isoformat(sep=' ', timespec='milliseconds')
            times_played = data['stats']['times_played']

    except:
        #print(data['name'], ": No stats here")
        pass

    year, month, day = (data['released_at']).split("-")
    year = int(year)
    month = int(month)
    day = int(day)
    released_at = datetime(year, month, day).isoformat(sep=' ', timespec='milliseconds')
    newTime = turnSeconds(data['duration'])
    print(newTime)
    song = Songs(data['artist'], newTime, data['name'], released_at, 
    data['song_id'], global_rank, last_played_at, times_played)

    if song.checkExistence():
        song.updateData()

    else:
        song.insertData()

'''
Deletes a song from the database using its song_id
I: song_id
O: None
'''
def deleteDB(song_id):
    Songs.deleteData(song_id)

#########################################

'''
Creates a click group, for multiple commands implementation from the terminal
Makes the CLI
'''
@click.group()
def cli():
    pass

'''
Command that receive the month and call the API with the inputed data
I: month (YYYY-MM)
O: None
'''
@click.command()
@click.argument('month', type=str, callback=monthRegex)
def monthly(month):
    params = {
        'released_at': month,
        'api_key': api_key
    }
    response = requests.get(urlMon, headers=None, params=params)
    data = response.json()
    try:
        if data["error"]:
            print(data["error"])
    except:
        for item in data:
            insertDB(item)

'''
Command that receive the day and call the API with the inputed data
I: day (YYYY-MM-DD)
O: None
'''
@click.command()
@click.argument('day', type=str, callback=dayRegex)
def daily(day):
    params = {
        'released_at': day,
        'api_key': api_key
    }
    response = requests.get(urlDay, headers=None, params=params)
    data = response.json()
    try: 
        if data["error"]:
            print(data["error"])
    except:
        for item in data:
            insertDB(item)

'''
Command that receive the song_id and deletes it from the database
I: delete (song_id)
O: None
'''
@click.command()
@click.option('--delete', '-d', type=str, help='Command to delete a song, receives the song_id')
def changeDB(delete):
    if delete:
        deleteDB(delete)
    else:
        print("Please use \n\n--help \n\nto see the available commands")

##############################################
#Creates the group of commands from the CLI
##############################################
cli.add_command(monthly)
cli.add_command(daily)
cli.add_command(changeDB)


if __name__ == "__main__":
    cli()
