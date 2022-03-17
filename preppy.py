#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "with python3Packages; [ beautifulsoup4 requests ]"

import requests,sys
from bs4 import BeautifulSoup

URL = "https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/"

def data():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("details")

    for x in results:
        if x.find("table"):
            print("[",x.find("summary").text,"]")
            for y in x.find("table").find("tbody").findAll("tr"):
                for idz,z in enumerate(y.findAll("td")):
                    if idz==0:
                        for a in z.findAll("a",href=True):
                            print("\t[",a.text,"] (",a['href'],")\n")
                    else:
                        for a in z.findAll("a",href=True):
                            if a.text=="YT":
                                print("\t\t",a.text,'\t: ',a['href'])
                            else:
                                print("\t\t",a.text,': ',a['href'])
                print("\n")
        else:
            if x.find("summary").findAll("a"):
                for y in x.find("summary").findAll("a",href=True):
                    print("[",x.find("summary").text,"] (",a['href'],")\n",x.find("ol").text)
            else:
                print("[",x.find("summary").text,"]\n\n",x.find("p").text)

def start():
    print("Challenge started !\n")
    sys.stdout = open("data.txt", "w")
    data()
    sys.stdout = sys.__stdout__ #resets to default stdout
    day()

def day(num=1):
    start = False
    start_day = "Day " + str(num)
    end_day = "Day " + str(eval("int(num)+1")) + ":"
    datafile = open("data.txt", "r")
    for line in datafile:
        if not end_day in line:
            if start_day in line:
                start = True
            if start:
                print(line,end='')
        else:
            break
    datafile.close()

def mark():
    print("mark")

def help():
    print("help")

if __name__ == '__main__':
    functions = [ "start","data", "day", "help", "mark" ]
    if sys.argv[1] in functions:
        if len(sys.argv) == 2:
            globals()[sys.argv[1]]()
        else:
            globals()[sys.argv[1]](sys.argv[2])
    else:
        print("Invalid function !")
