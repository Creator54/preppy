#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "with python3Packages; [ beautifulsoup4 requests ]"

import requests,sys,datetime,re
from bs4 import BeautifulSoup

URL = "https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/"
functions = [ "start","syllabus", "day", "help", "mark" ]
prepday=1

def syllabus():
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
                                print("\t\t",a.text.replace("YT","YT_VID",1),': ',a['href'])
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
    sys.stdout = open("syllabus.txt", "w")
    syllabus()
    sys.stdout = open("day_syllabus.txt","w")
    print("Challenge started on : ",datetime.datetime.now().strftime("%c"),"\n")
    day()
    sys.stdout = sys.__stdout__
    print(open("day_syllabus.txt").read())

def day(num=1,usefile="syllabus.txt"):
    start = False
    start_day = "Day " + str(num)
    end_day = "Day " + str(eval("int(num)+1"))
    with open(usefile, "r") as syllabusfile:
        for line in syllabusfile:
            if not end_day in line:
                if start_day in line:
                    start = True
                if start:
                    print(line,end='')
            else:
                break

def mark():
    with open("day_syllabus.txt","r") as syllabusfile:
        for line in syllabusfile:
            if line.startswith("[ Day"):
                prepday = int(re.search(r'\d+', line).group())

    try:
        print(open("progress.txt").read()) #using "r" works but gives <_io.TextIOWrapper name='progress.txt' mode='r' encoding='UTF-8'> too
    except:
        open("progress.txt","w")
        print(open("progress.txt").read())

    marklines = int(input("\nNo. of tasks done: "))
    sys.stdout = open("progress.txt","w")
    with open("day_syllabus.txt","r") as syllabusfile:
        for num, line in enumerate(syllabusfile):
            if line !="\n" and num >2 and marklines!=0:
                if len(line) == len(line.encode()): #last checking if line already has the check/unicode char
                    if "[" in line:
                        print("\t✅",line.replace("\t", "", 1),end="")
                    else:
                        print("\t\t ✅",line.replace("\t", "",3),end="")
                    marklines -=1
            else:
                print(line,end="")

def help():
    print("args this script accepts: ")
    print(functions)

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] in functions:
        if len(sys.argv) == 2:
            globals()[sys.argv[1]]()
        else:
            globals()[sys.argv[1]](sys.argv[2])
    else:
        help()
