"""
Automatic SQL Queries Checker
Date: 20/10/2022
Author: A.Guardiola
"""

import mysql.connector
import colorama

# TBD: move to script arguments
EJERCICIO = "AC5"
DATABASE = "jardineria"
NUM_CONSULTAS = 22
ALUMNO = "Ignacio Albiol"
MULTILINE_QUERY = True
# ACi

def executeQuery(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def parseSQL(file):
    queriesFile = open(file,"r")
    if MULTILINE_QUERY:
        queries = []
        query = " "
        while True:
            newLine = queriesFile.readline()
            if not newLine:
                break
            if ";" not in newLine:
                query = query + newLine
            else:
                query = query + newLine
                queries.append(query.replace("\n"," "))
                query = ""
    else:
        queries = queriesFile.read().splitlines()
    return queries

# Read and parse SQL files
queriesok = parseSQL(f"queries/{EJERCICIO}.sql")
queries = parseSQL("queries/alumne.sql")

# Database connection
db = mysql.connector.connect(user='root', password='claumestra',
                            host='127.0.0.1', database=DATABASE)
cursor = db.cursor()

#  Set up output file
sortida = open("queries/correccio.txt",'a',encoding="UTF-8")
print(f"Correcció {ALUMNO}", file=sortida)

# Check queries
testsok = 0
testCount = NUM_CONSULTAS
for line,query in enumerate(queries):
    result_ok = executeQuery(queriesok[line])
    try:
        result = executeQuery(query)

        if result == result_ok:
            print(colorama.Fore.GREEN + f"Query #{line + 1} is OK")
            print(f"Query #{line + 1} is OK", file=sortida)
            testsok += 1
        else:
            print(colorama.Fore.RED + f"Query #{line + 1} is KO")
            print(f"Query #{line + 1} is KO", file=sortida)
    except:
        print(colorama.Fore.RED + f"Query #{line + 1} is KO")
        print(f"Query #{line + 1} is KO", file=sortida)

#  Finish and close output file
print(colorama.Style.RESET_ALL)
print(f"Tests OK: {testsok}")
print(f"Tests OK: {testsok}", file=sortida)
print(f"Nota: {round(testsok/testCount*10,2)}", file=sortida)

db.close()