# example from Udemy course learn web scraping with python from scratch, coded by me.
from bs4 import BeautifulSoup
import requests
import pandas as pd
import statistics
import csv

#/sort/points/year/2019/seasontype/2
url = 'http://www.espn.com/nhl/statistics/player/_/stat/points'
defenseURL = 'http://www.espn.com/nhl/statistics/player/_/stat/defensive'
icetimeURL = 'http://www.espn.com/nhl/statistics/player/_/stat/timeonice'
faceoffsURL = 'http://www.espn.com/nhl/statistics/player/_/stat/faceoffs'
majorPimsURL = 'http://www.espn.com/nhl/statistics/player/_/stat/major-penalties'
minorPimsURL = 'http://www.espn.com/nhl/statistics/player/_/stat/minor-penalties'
goaliesURL = 'http://www.espn.com/nhl/statistics/player/_/stat/goaltending'
players = {}
playerNames = []
positions = []
teams = []
gps = []
goals = []
assists = []
points = []
plusMinus = []
pims = []
gwgs = []
otgs = []
ppgs = []
ppas = []
pkgs = []
pkas = []
shots = []
hits = []
blockedShots = []

goalies = []
goaliesGPs = []
goalieTeams = []
wins = []
gaas = []
gas = []
shotsAgainst = []
saves = []
svPercentage = []
shutouts = []

defensePlayers = {}
icetimePlayers = {}
faceoffPlayers = {}
majorPenaltyPlayers = {}
minorPenaltyPlayers = {}

def parseScoringPage(url):
    print('Parsing Scoring Page...')
    while True:
        breakFlag = False
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 17:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            playerNames.append(playerData[0])
            positions.append(playerData[1])
            teams.append(row[2].text)
            gps.append(row[3].text)
            goals.append(row[4].text)
            assists.append(row[5].text)
            points.append(row[6].text)
            plusMinus.append(row[7].text)
            pims.append(row[8].text)
            shots.append((row[10].text))
            gwgs.append(row[12].text)
            ppgs.append(row[13].text)
            ppas.append(row[14].text)
            pkgs.append(row[15].text)
            pkas.append(row[16].text)
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            #prevID = link.find('div', {'class': 'jcarousel-prev'})
            #if end is not None:
            #    breakFlag = True
            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    url = 'https:' + str(next)
        if breakFlag is True:
            break

def parseDefensivePage(defenseURL):
    print('Parsing Defense Page...')
    while True:
        breakFlag = False
        response = requests.get(defenseURL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 12:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            defensePlayers[playerData[0]] = {'position': playerData[1], 'team': row[2].text, 'gamesPlayed': row[3].text, 'hits': row[10].text, 'blockedShots': row[11].text}
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    defenseURL = 'https:' + str(next)
        if breakFlag is True:
            break


def parseIcetimePage(icetimeURL):
    print('Parsing Ice-time Page...')
    while True:
        breakFlag = False
        response = requests.get(icetimeURL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 12:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            icetimePlayers[playerData[0]] = {'position': playerData[1], 'team': row[2].text, 'gamesPlayed': row[3].text, 'toig': row[8].text, 'shifts': row[9].text, 'production': row[11].text}
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    icetimeURL = 'https:' + str(next)
        if breakFlag is True:
            break


def parseFaceoffsPage(faceoffsURL):
    print('Parsing Faceoffs Page...')
    while True:
        breakFlag = False
        response = requests.get(faceoffsURL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 13:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            faceoffPlayers[playerData[0]] = {'position': playerData[1], 'team': row[2].text, 'gamesPlayed': row[3].text,'faceoffs': row[9].text, 'faceoffsWon': row[10].text}
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    faceoffsURL = 'https:' + str(next)
        if breakFlag is True:
            break


def parseMajorPenaltiesPage(majorPimsURL):
    print('Parsing Major Penalty Page...')
    while True:
        breakFlag = False
        response = requests.get(majorPimsURL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 14:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            majorPenaltyPlayers[playerData[0]] = {'position': playerData[1], 'team': row[2].text, 'gamesPlayed': round(int(row[3].text) / float(row[4].text)), 'majorPenalties': row[5].text, 'misconduct': row[6].text, 'gameMisconduct': row[7].text,
                                             'boarding': row[8].text, 'unsportsmanlikeConduct': row[9].text, 'fights': row[10].text, 'instigator': row[11].text}
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    majorPimsURL = 'https:' + str(next)
        if breakFlag is True:
            break


def parseMinorPenaltiesPage(minorPimsURL):
    print('Parsing Minor Penalty Page...')
    while True:
        breakFlag = False
        response = requests.get(minorPimsURL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 15:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            minorPenaltyPlayers[playerData[0]] = {'position': playerData[1], 'team': row[2].text, 'gamesPlayed': 'N/A', 'minorPenalties': row[4].text, 'hooking': row[5].text, 'tripping': row[6].text,
                                                  'roughing': row[7].text, 'holding': row[8].text, 'interference': row[9].text, 'slashing': row[10].text,
                                                  'highSticking': row[11].text, 'crossCheck': row[12].text, 'holdingStick': row[13].text, 'goalieInterference': row[14].text}
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    minorPimsURL = 'https:' + str(next)
        if breakFlag is True:
            break


def parseGoaliePage(goaliesURL):
    print('Parsing Goalie Page...')
    while True:
        breakFlag = False
        response = requests.get(goaliesURL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tablehead'})
        cellData = []
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 16:
                if cells[0].text != 'RK':
                    cellData.append(cells)
        for row in cellData:
            playerData = row[1].text
            playerData = playerData.split(', ')
            goalies.append(playerData[0])
            goalieTeams.append(row[2].text)
            goaliesGPs.append(row[3].text)
            wins.append(row[4].text)
            gaas.append(row[7].text)
            gas.append(row[8].text)
            shotsAgainst.append(row[9].text)
            saves.append(row[10].text)
            svPercentage.append(row[11].text)
            shutouts.append(row[12].text)
        links = soup.find_all('a', {'rel': 'nofollow'})
        divs = soup.find_all('div')
        for div in divs:
            divStr = str(div)
            if 'jcarousel-next-disabled' in divStr:
                breakFlag = True
        for link in links:
            if breakFlag is True:
                break
            identifier = link.find('div', {'class': 'jcarousel-next'})

            if identifier is not None:
                if link.get('href'):
                    next = link.get('href')
                    goaliesURL = 'https:' + str(next)
        if breakFlag is True:
            break


playerStats = []


def createPlayers():
    print('Creating Player Objects...')
    i = 0
    for player in playerNames:
        playerStats2 = {
            'name': player,
            'team': teams[i],
            'gamesPlayed': gps[i],
            'position': positions[i],
            'goals': goals[i],
            'assists': assists[i],
            'points': points[i],
            'plusMinus': plusMinus[i],
            'PIMS': pims[i],
            'shots': shots[i],
            'GWGS': gwgs[i],
            'PPGS': ppgs[i],
            'PPAS': ppas[i],
            'PKGS': pkgs[i],
            'PKAS': pkas[i],
            'hits': 'N/A',
            'blockedShots': 'N/A',
            'toig': 'N/A',
            'shifts': 'N/A',
            'production': 'N/A',
            'faceoffs': 'N/A',
            'faceoffsWon': 'N/A',
            'majorPenalties': 'N/A',
            'misconduct': 'N/A',
            'gameMisconduct': 'N/A',
            'boarding': 'N/A',
            'unsportsmanlikeConduct': 'N/A',
            'fights': 'N/A',
            'instigator': 'N/A',
            'minorPenalties': 'N/A',
            'hooking': 'N/A',
            'tripping': 'N/A',
            'roughing': 'N/A',
            'holding': 'N/A',
            'interference': 'N/A',
            'slashing': 'N/A',
            'highSticking': 'N/A',
            'crossCheck': 'N/A',
            'holdingStick': 'N/A',
            'goalieInterference': 'N/A'
        }
        i += 1
        playerStats.append(playerStats2)

goalieStats = {}
def createGoalie():
    print('Creating Goalie Objects...')
    i = 0
    for goalie in goalies:
        goalieStats[goalie] = {
            'Team': goalieTeams[i],
            'GamesPlayed': goaliesGPs[i],
            'goalsAgainstAverage': gaas[i],
            'goalsAllowed': gas[i],
            'shotsAgainst': shotsAgainst[i],
            'saves': saves[i],
            'savePercentage': svPercentage[i],
            'shutouts': shutouts[i]
                              }


def addDefenseStatsToPlayer():
    print('Adding Defense Stats to Players...')
    for dp in defensePlayers.keys():
        players = [p['name'] for p in playerStats]
        if dp not in  players and defensePlayers[dp]['position'] != 'G ':
            playerStats2 = {}
            playerStats2['name'] = dp
            playerStats2['position'] = defensePlayers[dp]['position']
            playerStats2['team'] = defensePlayers[dp]['team']
            playerStats2['gamesPlayed'] = defensePlayers[dp]['gamesPlayed']
            playerStats2['hits'] = defensePlayers[dp]['hits']
            playerStats2['blockedShots'] = defensePlayers[dp]['blockedShots']
            playerStats2['goals'] = 'N/A'
            playerStats2['assists'] = 'N/A'
            playerStats2['points'] = 'N/A'
            playerStats2['plusMinus'] = 'N/A'
            playerStats2['PIMS'] = 'N/A'
            playerStats2['shots'] = 'N/A'
            playerStats2['GWGS'] = 'N/A'
            playerStats2['PPGS'] = 'N/A'
            playerStats2['PPAS'] = 'N/A'
            playerStats2['PKGS'] = 'N/A'
            playerStats2['PKAS'] = 'N/A'
            playerStats2['toig'] = 'N/A'
            playerStats2['shifts'] = 'N/A'
            playerStats2['production'] = 'N/A'
            playerStats2['faceoffs'] = 'N/A'
            playerStats2['faceoffsWon'] = 'N/A'
            playerStats2['majorPenalties'] = 'N/A'
            playerStats2['misconduct'] = 'N/A'
            playerStats2['gameMisconduct'] = 'N/A'
            playerStats2['boarding'] = 'N/A'
            playerStats2['unsportsmanlikeConduct'] = 'N/A'
            playerStats2['fights'] = 'N/A'
            playerStats2['instigator'] = 'N/A'
            playerStats2['minorPenalties'] = 'N/A'
            playerStats2['hooking'] = 'N/A'
            playerStats2['tripping'] = 'N/A'
            playerStats2['roughing'] = 'N/A'
            playerStats2['holding'] = 'N/A'
            playerStats2['interference'] = 'N/A'
            playerStats2['slashing'] = 'N/A'
            playerStats2['highSticking'] = 'N/A'
            playerStats2['crossCheck'] = 'N/A'
            playerStats2['holdingStick'] = 'N/A'
            playerStats2['goalieInterference'] = 'N/A'
            playerStats.append(playerStats2)
        else:
            for p in playerStats:
                name = p['name']
                if dp == name:
                    p['hits'] = defensePlayers[dp]['hits']
                    p['blockedShots'] = defensePlayers[dp]['blockedShots']


def addIcetimeStatsToPlayer():
    print('Adding Icetime Stats to Players')
    for ip in icetimePlayers.keys():
        players = [p['name'] for p in playerStats]
        if ip not in players and icetimePlayers[ip]['position'] != 'G ':
            playerStats2 = {}
            playerStats2['name'] = ip
            playerStats2['position'] = icetimePlayers[ip]['position']
            playerStats2['team'] = icetimePlayers[ip]['team']
            playerStats2['gamesPlayed'] = icetimePlayers[ip]['gamesPlayed']
            playerStats2['toig'] = icetimePlayers[ip]['toig']
            playerStats2['shifts'] = icetimePlayers[ip]['shifts']
            playerStats2['production'] = icetimePlayers[ip]['production']
            playerStats2['hits'] = 'N/A'
            playerStats2['blockedShots'] = 'N/A'
            playerStats2['goals'] = 'N/A'
            playerStats2['assists'] = 'N/A'
            playerStats2['points'] = 'N/A'
            playerStats2['plusMinus'] = 'N/A'
            playerStats2['PIMS'] = 'N/A'
            playerStats2['shots'] = 'N/A'
            playerStats2['GWGS'] = 'N/A'
            playerStats2['PPGS'] = 'N/A'
            playerStats2['PPAS'] = 'N/A'
            playerStats2['PKGS'] = 'N/A'
            playerStats2['PKAS'] = 'N/A'
            playerStats2['faceoffs'] = 'N/A'
            playerStats2['faceoffsWon'] = 'N/A'
            playerStats2['majorPenalties'] = 'N/A'
            playerStats2['misconduct'] = 'N/A'
            playerStats2['gameMisconduct'] = 'N/A'
            playerStats2['boarding'] = 'N/A'
            playerStats2['unsportsmanlikeConduct'] = 'N/A'
            playerStats2['fights'] = 'N/A'
            playerStats2['instigator'] = 'N/A'
            playerStats2['minorPenalties'] = 'N/A'
            playerStats2['hooking'] = 'N/A'
            playerStats2['tripping'] = 'N/A'
            playerStats2['roughing'] = 'N/A'
            playerStats2['holding'] = 'N/A'
            playerStats2['interference'] = 'N/A'
            playerStats2['slashing'] = 'N/A'
            playerStats2['highSticking'] = 'N/A'
            playerStats2['crossCheck'] = 'N/A'
            playerStats2['holdingStick'] = 'N/A'
            playerStats2['goalieInterference'] = 'N/A'
            playerStats.append(playerStats2)
        else:
            for p in playerStats:
                name = p['name']
                if ip == name:
                    p['toig'] = icetimePlayers[ip]['toig']
                    p['shifts'] = icetimePlayers[ip]['shifts']
                    p['production'] = icetimePlayers[ip]['production']



def addFaceoffStatsToPlayer():
    print('Adding Faceoff Stats to Players...')
    for fp in faceoffPlayers.keys():
        players = [p['name'] for p in playerStats]
        if fp not in players and faceoffPlayers[fp]['position'] != 'G ':
            playerStats2 = {}
            playerStats2['name'] = fp
            playerStats2['position'] = faceoffPlayers[fp]['position']
            playerStats2['team'] = faceoffPlayers[fp]['team']
            playerStats2['gamesPlayed'] = faceoffPlayers[fp]['gamesPlayed']
            playerStats2['faceoffs'] = faceoffPlayers[fp]['faceoffs']
            playerStats2['faceoffsWon'] = faceoffPlayers[fp]['faceoffsWon']
            playerStats2['hits'] = 'N/A'
            playerStats2['blockedShots'] = 'N/A'
            playerStats2['goals'] = 'N/A'
            playerStats2['assists'] = 'N/A'
            playerStats2['points'] = 'N/A'
            playerStats2['plusMinus'] = 'N/A'
            playerStats2['PIMS'] = 'N/A'
            playerStats2['shots'] = 'N/A'
            playerStats2['GWGS'] = 'N/A'
            playerStats2['PPGS'] = 'N/A'
            playerStats2['PPAS'] = 'N/A'
            playerStats2['PKGS'] = 'N/A'
            playerStats2['PKAS'] = 'N/A'
            playerStats2['toig'] = 'N/A'
            playerStats2['shifts'] = 'N/A'
            playerStats2['production'] = 'N/A'
            playerStats2['majorPenalties'] = 'N/A'
            playerStats2['misconduct'] = 'N/A'
            playerStats2['gameMisconduct'] = 'N/A'
            playerStats2['boarding'] = 'N/A'
            playerStats2['unsportsmanlikeConduct'] = 'N/A'
            playerStats2['fights'] = 'N/A'
            playerStats2['instigator'] = 'N/A'
            playerStats2['minorPenalties'] = 'N/A'
            playerStats2['hooking'] = 'N/A'
            playerStats2['tripping'] = 'N/A'
            playerStats2['roughing'] = 'N/A'
            playerStats2['holding'] = 'N/A'
            playerStats2['interference'] = 'N/A'
            playerStats2['slashing'] = 'N/A'
            playerStats2['highSticking'] = 'N/A'
            playerStats2['crossCheck'] = 'N/A'
            playerStats2['holdingStick'] = 'N/A'
            playerStats2['goalieInterference'] = 'N/A'
            playerStats.append(playerStats2)
        else:
            for p in playerStats:
                name = p['name']
                if fp == name:
                    p['faceoffs'] = faceoffPlayers[fp]['faceoffs']
                    p['faceoffsWon'] = faceoffPlayers[fp]['faceoffsWon']



def addMajorPenaltyStatsToPlayer():
    print('Adding Major Penalty Stats to Players...')
    for mjp in majorPenaltyPlayers.keys():
        players = [p['name'] for p in playerStats]
        if mjp not in players and majorPenaltyPlayers[mjp]['position'] != 'G ':
            playerStats2 = {}
            playerStats2['name'] = mjp
            playerStats2['position'] = majorPenaltyPlayers[mjp]['position']
            playerStats2['tams'] = majorPenaltyPlayers[mjp]['team']
            playerStats2['gamesPlayed'] = majorPenaltyPlayers[mjp]['gamesPlayed']
            playerStats2['majorPenalties'] = majorPenaltyPlayers[mjp]['majorPenalties']
            playerStats2['misconduct'] = majorPenaltyPlayers[mjp]['misconduct']
            playerStats2['gameMisconduct'] = majorPenaltyPlayers[mjp]['gameMisconduct']
            playerStats2['boarding'] = majorPenaltyPlayers[mjp]['boarding']
            playerStats2['unsportsmanlikeConduct'] = majorPenaltyPlayers[mjp]['unsportsmanlikeConduct']
            playerStats2['fights'] = majorPenaltyPlayers[mjp]['fights']
            playerStats2['instigator'] = majorPenaltyPlayers[mjp]['instigator']
            playerStats2['hits'] = 'N/A'
            playerStats2['blockedShots'] = 'N/A'
            playerStats2['goals'] = 'N/A'
            playerStats2['assists'] = 'N/A'
            playerStats2['points'] = 'N/A'
            playerStats2['plusMinus'] = 'N/A'
            playerStats2['PIMS'] = 'N/A'
            playerStats2['shots'] = 'N/A'
            playerStats2['GWGS'] = 'N/A'
            playerStats2['PPGS'] = 'N/A'
            playerStats2['PPAS'] = 'N/A'
            playerStats2['PKGS'] = 'N/A'
            playerStats2['PKAS'] = 'N/A'
            playerStats2['toig'] = 'N/A'
            playerStats2['shifts'] = 'N/A'
            playerStats2['production'] = 'N/A'
            playerStats2['faceoffs'] = 'N/A'
            playerStats2['faceoffsWon'] = 'N/A'
            playerStats2['minorPenalties'] = 'N/A'
            playerStats2['hooking'] = 'N/A'
            playerStats2['tripping'] = 'N/A'
            playerStats2['roughing'] = 'N/A'
            playerStats2['holding'] = 'N/A'
            playerStats2['interference'] = 'N/A'
            playerStats2['slashing'] = 'N/A'
            playerStats2['highSticking'] = 'N/A'
            playerStats2['crossCheck'] = 'N/A'
            playerStats2['holdingStick'] = 'N/A'
            playerStats2['goalieInterference'] = 'N/A'
        else:
            for p in playerStats:
                name = p['name']
                if mjp == name:
                    p['majorPenalties'] = majorPenaltyPlayers[mjp]['majorPenalties']
                    p['misconduct'] = majorPenaltyPlayers[mjp]['misconduct']
                    p['gameMisconduct'] = majorPenaltyPlayers[mjp]['gameMisconduct']
                    p['boarding'] = majorPenaltyPlayers[mjp]['boarding']
                    p['unsportsmanlikeConduct'] = majorPenaltyPlayers[mjp]['unsportsmanlikeConduct']
                    p['fights'] = majorPenaltyPlayers[mjp]['fights']
                    p['instigator'] = majorPenaltyPlayers[mjp]['instigator']


def addMinorPenaltyStatsToPlayer():
    print('Adding Minor Penalty Stats to Players')
    for mip in minorPenaltyPlayers.keys():
        players = [p['name'] for p in playerStats]
        if mip not in players and minorPenaltyPlayers[mip]['position'] != 'G ':
            playerStats2 = {}
            playerStats2['name'] = mip
            playerStats2['position'] = minorPenaltyPlayers[mip]['position']
            playerStats2['team'] = minorPenaltyPlayers[mip]['team']
            playerStats2['gamesPlayed'] = minorPenaltyPlayers[mip]['gamesPlayed']
            playerStats2['minorPenalties'] = minorPenaltyPlayers[mip]['minorPenalties']
            playerStats2['hooking'] = minorPenaltyPlayers[mip]['hooking']
            playerStats2['tripping'] = minorPenaltyPlayers[mip]['tripping']
            playerStats2['roughing'] = minorPenaltyPlayers[mip]['roughing']
            playerStats2['holding'] = minorPenaltyPlayers[mip]['holding']
            playerStats2['interference'] = minorPenaltyPlayers[mip]['interference']
            playerStats2['slashing'] = minorPenaltyPlayers[mip]['slashing']
            playerStats2['highSticking'] = minorPenaltyPlayers[mip]['highSticking']
            playerStats2['crossCheck'] = minorPenaltyPlayers[mip]['crossCheck']
            playerStats2['holdingStick'] = minorPenaltyPlayers[mip]['holdingStick']
            playerStats2['goalieInterference'] = minorPenaltyPlayers[mip]['goalieInterference']
            playerStats2['hits'] = 'N/A'
            playerStats2['blockedShots'] = 'N/A'
            playerStats2['goals'] = 'N/A'
            playerStats2['assists'] = 'N/A'
            playerStats2['points'] = 'N/A'
            playerStats2['plusMinus'] = 'N/A'
            playerStats2['PIMS'] = 'N/A'
            playerStats2['shots'] = 'N/A'
            playerStats2['GWGS'] = 'N/A'
            playerStats2['PPGS'] = 'N/A'
            playerStats2['PPAS'] = 'N/A'
            playerStats2['PKGS'] = 'N/A'
            playerStats2['PKAS'] = 'N/A'
            playerStats2['toig'] = 'N/A'
            playerStats2['shifts'] = 'N/A'
            playerStats2['production'] = 'N/A'
            playerStats2['faceoffs'] = 'N/A'
            playerStats2['faceoffsWon'] = 'N/A'
            playerStats2['majorPenalties'] = 'N/A'
            playerStats2['misconduct'] = 'N/A'
            playerStats2['gameMisconduct'] = 'N/A'
            playerStats2['boarding'] = 'N/A'
            playerStats2['unsportsmanlikeConduct'] = 'N/A'
            playerStats2['fights'] = 'N/A'
            playerStats2['instigator'] = 'N/A'
            playerStats.append(playerStats2)
        else:
            for p in playerStats:
                name = p['name']
                if mip == name:
                    p['minorPenalties'] = minorPenaltyPlayers[mip]['minorPenalties']
                    p['hooking'] = minorPenaltyPlayers[mip]['hooking']
                    p['tripping'] = minorPenaltyPlayers[mip]['tripping']
                    p['roughing'] = minorPenaltyPlayers[mip]['roughing']
                    p['holding'] = minorPenaltyPlayers[mip]['holding']
                    p['interference'] = minorPenaltyPlayers[mip]['interference']
                    p['slashing'] = minorPenaltyPlayers[mip]['slashing']
                    p['highSticking'] = minorPenaltyPlayers[mip]['highSticking']
                    p['crossCheck'] = minorPenaltyPlayers[mip]['crossCheck']
                    p['holdingStick'] = minorPenaltyPlayers[mip]['holdingStick']
                    p['goalieInterference'] = minorPenaltyPlayers[mip]['goalieInterference']


def writeToCsv(filename, dictObjects):
    with open(filename, 'w', newline='') as csvOut:
        csvWriter = csv.DictWriter(csvOut, playerStats[0].keys())
        csvWriter.writeheader()
        csvWriter.writerows(playerStats)


parseScoringPage(url)
parseDefensivePage(defenseURL)
parseIcetimePage(icetimeURL)
parseFaceoffsPage(faceoffsURL)
parseMajorPenaltiesPage(majorPimsURL)
parseMinorPenaltiesPage(minorPimsURL)
#parseGoaliePage(goaliesURL)
createPlayers()
addDefenseStatsToPlayer()
addIcetimeStatsToPlayer()
addFaceoffStatsToPlayer()
addMajorPenaltyStatsToPlayer()
addMinorPenaltyStatsToPlayer()
print(playerStats)
writeToCsv('NHL_Player_Stats.csv', playerStats)


