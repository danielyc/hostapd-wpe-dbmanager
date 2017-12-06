#!/usr/bin/python3.5

import csv, time, os

def cleandict(dictionary):
	cmpdict = {}
	for x in dictionary:
		if not x in cmpdict:
			cmpdict[x] = dictionary[x]
	return cmpdict


def cmpdict(original, newdict):
	new = {}
	for x in newdict:
		if not x in original:
			new[x] = newdict[x]
	return new


def writedict(dictionary, append=False, filename='db.csv'):
	clndict = cleandict(dictionary)
	if append:
		with open(filename, 'a') as f:
			wr = csv.writer(f)
			for x, y in clndict.items():
				wr.writerow([x, y])
	else:
		with open(filename, 'w') as f:
			wr = csv.writer(f)
			for x, y in clndict.items():
				wr.writerow([x, y])


def readdict():
    mydict = {}
    with open('db.csv', 'r') as f:
        rd = csv.reader(f)
        for row in rd:
            try:
                mydict[row[0]] = row[1]
            except IndexError:
                continue

    return mydict


def readlog():
    with open('hostapd-wpe.log', 'r') as f:
        y = {}
        for x in f.readlines():
            if 'jtr' in x:
                q = x[15:-1].split(':')
                y[q[0]] = q[1]
    return y


def calcperc():
	total = 0
	cracked = 0
	perc = 0	
	mydb = readdict()
	for x in mydb:
		if not '$NETNTLM$' in mydb[x]:
			cracked += 1
		total += 1
	perc = str(round((cracked / total) * 100, 0))[:2]
	return str(total), perc
	

def importpw():
	os.system('clear')
	db = readdict()
	print()
	print('#######################')
	print()
	print('    Enter filename     ')
	print()
	print('#######################')
	print()
	filename = input('> ')
	
	if not os.path.isfile(filename):	
		print('[*] file not found')
		menu()
	f = open(filename, 'r')	
	unpw = {}
	for x in f.readlines():
		#hcat
		if '::::' in x:
			try:
				unpw[x.split(':')[0]] = x.split(':')[6][:-1]
			except IndexError:
				continue
		#john
		else:
			try:
				unpw[x.split(':')[0]] = x.split(':')[1][:-1]
			except IndexError:
				continue
	f.close()
	new = {}
	tot = 0
	for x in unpw:
		if x in db:
			db[x] = unpw[x]
			tot += 1
		else:
			new[x] = unpw[x]
			tot += 1
	writedict(db)
	writedict(new, True)
	print('[*] %s passwords updated in database' % (str(tot)))


def export():
	os.system('clear')
	db = readdict()
	exprt = {}
	print()
	print('#######################')
	print()
	print('   Enter exportname    ')
	print()
	print('#######################')
	print()
	filename = input('> ')
	os.system('clear')
	print()
	print('#######################')
	print()
	print('   [J]ohn or [H]ashcat     ')
	print()
	print('#######################')
	print()
	extype = input('> ')
	if 'JOHN' in extype.upper() or 'J' in extype.upper():
		extype = 'john'
	elif 'HASHCAT' in extype.upper() or 'H' in extype.upper():
		extype = 'hcat'
	else:
		print('[*] invalid input')
		time.sleep(1)
		menu()
	for x, y in db.items():
		if '$NETNTLM$' in y and len(y) > 70:
			exprt[x] = y
	
	with open(filename, 'w') as f:
		for x, y in exprt.items():
			if extype == 'john':
				name = x + ':' + y + '\n'
			elif extype == 'hcat':
				name = x + '::::' + y.split('$')[3] + ':' + y.split('$')[2] + '\n'			
			f.write(name)


def searchuser():
	os.system('clear')
	db = readdict()
	print()
	print('#######################')
	print()
	print('    Enter username     ')
	print()
	print('#######################')
	print()
	inp = input('> ')
	if inp in db:
		if '$NETNTLM$' in db[inp] and len(db[inp]) > 70:
			print('[*] user found')
			print('[*] password not found')
		else:
			print('username: ' + inp)
			print('password: ' + db[inp])
		print()
		input('press enter to continue')
	else:
		print('[*] user not found')
		time.sleep(2)
		main()


def deluser():
	os.system('clear')
	db = readdict()
	print()
	print('#######################')
	print()
	print('    Enter username     ')
	print()
	print('#######################')
	print()
	user = input('> ')
	if user in db:
		print('username: ' + user)
		print('password: ' + db[user])
		print()
		print('are you sure?')
		print()
		print('[Y]es / [N]o ')
		inp = input('> ')
		if 'Y' in inp.upper() or 'YES' in inp.upper():
			del db[user]
			writedict(db)
	else:
		print('[*] user not found')
		time.sleep(2)


def deldb():
	os.system('clear')
	print()
	print('#######################')
	print()
	print('   ARE YOU SURE????    ')
	print()
	print('#######################')
	print()
	print('[Y]es / [N]o')
	print()
	inp = input('> ')
	if 'YES' in inp.upper() or 'Y' in inp.upper():
		os.remove('db.csv')
	else:
		main()


def menu():
	os.system('clear')
	print()
	print('########################')
	print()
	print('          MENU          ')
	print()
	print('########################')
	print()
	print(calcperc()[0] + ' entries' )
	print(calcperc()[1] + '% of passwords cracked ')
	print()
	print('1. import pw to db      ')
	print('2. search user	       ')
	print('3. export uncracked     ')
	print('4. delete user	       ')
	print()
	print('19. DELETE DICT         ')
	print('99. exit		       ')
	print()
	inp = input('> ')
	if inp == '1':
		importpw()
		menu()
	elif inp == '2':
		searchuser()
		menu()
	elif inp == '3':
		export()
		menu()
	elif inp == '4':
		deluser()
		menu()
	elif inp == '19':
		deldb()
		menu()
	elif inp == '99':
		exit()	
	else:
		menu()


def main():
	mydict = {}
	if os.path.isfile('db.csv'):
		print('[*] database found')
	else:
		writedict({})
		print('[*] no database found, new one created')

	if os.path.isfile('hostapd-wpe.log'):
		mydict = readlog()
		print('[*] log file found and read')
	else:
		print('[*] no log file found')

	dbdict = readdict()

	if len(dbdict) == 0:
		writedict(mydict)
		print('[*] log file written to database')
	else:
		new = cmpdict(dbdict, mydict)
		if len(new) > 0:
			print('[*] new items found and written to database')
			writedict(new, True)
		else:
			print('[*] no new items found')

	menu()


if __name__ == '__main__':
	main()
