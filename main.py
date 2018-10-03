import urllib2
import sys
import os
##functions
def parseQmark(addr): ##removes sql
	i = 0
	out = ""
	try:
		while(addr[i] != "?"):
			out = out + addr[i]
			i = i + 1
	except:
		return addr
	return out

def openLink(address, local, current): ##returns list of addresses
	tryflag = 0
	out = []
	out2 = []
	try:
		url = urllib2.urlopen(address)
	except:
		return ""
	url = url.read()
	url = url.split("\"")
	for line in url:
		if tryflag == 1:
			out.append(line)
			tryflag = 0
		else:
			if line[-7:] == "a href=":
				tryflag = 1
			continue
	for addr in out:
		addr = parseQmark(addr)
		if addr[0:4] == "http":
			out2.append(addr)
			continue
		elif addr[0] == "/":
			out2.append(local + addr)
		else:
			if current[-1] == "/":
				out2.append(current + addr)
			else:
				out2.append(current + "/" + addr)
	return out2

def getRelative(addr): ##gets the server's address
	out = ""
	i  = 0
	if addr[0:7] == "http://":
		i = 7
	if addr[0:8] == "https://":
		i = 8
	try:
		while(addr[i] != "/"):
			out = out + addr[i]
			i = i + 1
	except:
		return addr
	return out

##main
try:
	f = open("config.txt","r")
	config = f.read()
	config = config.split("\n")
	f.close()
	ITERATIONS = int(config[0])
except:
	print("Config error")
	sys.exit(0)

current = raw_input("Web address: ")
if current[0:4] != "http":
	current = "http://" + current
queue = [current, ]
oldqueue = queue
completed = []
fyon = raw_input("Would you like to export to a file? y/n: ")
fyon = fyon.lower()
if fyon == "y" or fyon == "yes":
	fyon = 1
file = raw_input("Filename: ")
try:
	f = open(file, "w")
	f.close()
except:
	print("Unknown error.")

i = -1
cIT = 0
while(1):
	try:
		while(1):
			while(cIT == ITERATIONS):
				cont = raw_input("Continue? ")
				cont = cont.lower()
				if cont == "yes":
					cIT = -1
					break
				elif cont == "no":
					os._exit(0)
				else:
					continue
			cIT = cIT + 1
			i = i + 1
			addr = queue[i]
			current = addr
			relative = getRelative(addr)
			if addr in completed:
				continue
			if openLink(addr, relative, current) == "":
				continue
			queue = queue + openLink(addr, relative, current)
			oldqueue = queue
			print(addr)
			if fyon == 1:
				try:
					f = open(file, "r")
					fcon = f.read()
					f.close()
					f = open(file, "w")
					f.write(fcon + addr + "\n")
					f.close()
				except:
					f = open(file, "w")
					f.write(addr + "\n")
					f.close()
			completed.append(addr)
	except:
		queue = oldqueue[::-1]
