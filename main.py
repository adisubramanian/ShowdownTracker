import requests, os, csv, sys, re

# Get List of matches played
matches = open("matches.txt", "r").readlines()
matches = [i.rstrip() + ".log" for i in matches]

#playerName = input("What was your username: ")
playerName = "ck49"

wins = []
mons = []
monsBrought = []
allMons = set([])

matchData = csv.writer(open("ShowdownDataByMatch.csv", "w", newline=''))
monData = csv.writer(open("ShowdownDataByPokemon.csv", "w", newline=''))


DataByMatch = ["matchID", "Win", "OpponentsTeam1", "OpponentsTeam2", "OpponentsTeam3", "OpponentsTeam4", "OpponentsTeam5", "OpponentsTeam6", "OpponentBrought1", "OpponentBrought2","OpponentBrought3","OpponentBrought4"]
matchData.writerow(DataByMatch)
DataByMon = ["Pokemon", "matches", "YourWinPct", "matchesBrought", "PctBrought", "YourWinPctBrought"]
monData.writerow(DataByMon)




for match in matches:
	matchID = match.split("-")[1].split(".log")[0]
	#read match
	page = str(requests.get(match).content)
	lines = page.split("\\n")
	pregame, game = page.split("|start")


	#Are you player 1, player 2, or neither?
	if "player|p1|"+playerName+"|" in pregame:
		player = 1
		Notplayer = 2
	elif "player|p2|"+playerName+"|":
		player = 2
		Notplayer = 1
	else:
		print("player not found, skipping match")

	

	#determine winner
	if "win|"+playerName in page:
		wins.append(1)
	else:
		wins.append(0)

	opponentMons = []

	for line in pregame.split("\\n"):
		if "poke|p" + str(int(Notplayer)) in line:
			p = line.split("poke|p" + str(Notplayer) + "|")[1].split(",")[0]
			if "-" in p:
				if "Porygon" not in p and "o-o" not in p:
					p = p.split("-")[0]
			opponentMons.append(p)
			allMons.add(opponentMons[-1])
#	print(opponentMons)
	mons.append(opponentMons)

	opponentBrought = []
	patternA = "p" + str(Notplayer)+"a: "
	patternB = "p" + str(Notplayer)+"b: "
	for pokemon in opponentMons:
		if patternA + pokemon in game:
			opponentBrought.append(pokemon)
		elif patternB + pokemon in game:
			opponentBrought.append(pokemon)

#	print(opponentBrought)
	monsBrought.append(opponentBrought)

	row1 = [matchID, wins[-1]]
	while len(opponentMons) < 6:
		opponentMons.append("unknown")
	row1.extend(opponentMons)
	while(len(opponentBrought) < 4):
		opponentBrought.append("unknown")
	row1.extend(opponentBrought)
	matchData.writerow(row1)
#	print(row1)

#print(DataByMon)
for mon in allMons:
	matches = 0
	monWins = 0
	brought = 0
	winsWhenBrought = 0
	for i in range(len(wins)):
		if mon in mons[i]:
			matches = matches + 1
			monWins = monWins + wins[i]
			if mon in monsBrought[i]:
				brought = brought + 1
				winsWhenBrought = winsWhenBrought + wins[i]

	row2 = [mon, matches, monWins/matches, brought, brought/matches]
	if brought == 0:
		row2.append("NA")
	else:
		row2.append(winsWhenBrought/brought)
	monData.writerow(row2)
#	print(row2)
#print(wins)