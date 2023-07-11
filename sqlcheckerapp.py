"""
Automatic SQL Queries Checker (Backend for Web App)
Date: 20/10/2022
Author: A.Guardiola
"""

import mysql.connector
from flask import Flask, render_template, request
# import json Not needed
from random import shuffle

MULTILINE_QUERY = True

# Flask app setup ##############################################################
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Backend functions #############################################################
def getExerciceQueries(exercise):
    queriesokFile = open(f"queries/{exercise}.txt", "r", encoding="UTF-8")
    queriesok = queriesokFile.read().splitlines()
    queriesokFile.close()
    return queriesok

def parseSQL(exercise):
    queriesFile = open(f"queries/{exercise}.sql", "r", encoding="UTF-8")
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
    queriesFile.close()
    return queries

def checkQuery(database, exercise, number, query):
    # DB connection setup
    db = mysql.connector.connect(user='root', password='claumestra',
                                 host='127.0.0.1', database=database,
                                 charset='utf8')
    cursor = db.cursor()
    # Get correct query from file
    queryok = parseSQL(exercise)[number-1]
    # Get result of correct query from database
    cursor.execute(queryok)
    dataok = cursor.fetchall()
    # FIX PROVISIONAL
    # Need to add table prefix to avoid disambiguation
    headerDescrption = cursor.description
    headerok = []
    for row in headerDescrption:
        if row[0] not in headerok:
            headerok.append(row[0])
        else:
            headerok.append(row[0]+"2")
    # print(header)
    resultok = []
    for row in dataok:
        resultok.append(dict(zip(headerok, row)))
    # Get result of proposed query from database
    result = []
    try:
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        # FIX PROVISIONAL
        # Need to add table prefix to avoid disambiguation
        headerDescrption = cursor.description
        header = []
        for row in headerDescrption:
            if row[0] not in header:
                header.append(row[0])
            else:
                header.append(row[0]+"2")
        # print(header)
        for row in data:
            result.append(dict(zip(header, row)))
        # Compare and decide test result
        if data == dataok:
            datakeys = ['test', 'dataok', 'data', 'headersok', 'headers']
            data = dict(
                zip(datakeys, ['1', resultok, result, headerok, header]))
            return data
        else:
            datakeys = ['test', 'dataok', 'data', 'headersok', 'headers']
            data = dict(
                zip(datakeys, ['0', resultok, result, headerok, header]))
            return data
    except:
        header = []
        datakeys = ['test', 'dataok', 'data', 'headersok', 'headers']
        data = dict(zip(datakeys, ['0', resultok, result, headerok, header]))
        return data
    finally:
        db.close()

def registerScore(name,score):
    # DB connection setup
    db = mysql.connector.connect(user='root', password='claumestra',
                                 host='127.0.0.1', database='sqlchecker',
                                 charset='utf8')
    cursor = db.cursor()
    query = f"insert into scores(name,score) values('{name}',{score});"
    print(query)
    cursor.execute(query)
    db.commit()
    db.close()
    return 

# Routes #########################################################################
@app.route("/formSubmitted", methods=['POST'])
def formSubmitted():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        print(name,score)
        registerScore(name,score)
        return render_template("formSubmitted.html")

@app.route("/AC5", methods=['POST', 'GET'])
def showQueriesAC5():
    if request.method == 'POST':
        query = request.json
        test = checkQuery('universidad', 'AC5', int(query['no']), query['query'])
        return test
    queries = getExerciceQueries('AC5')
    queriesSet = list(zip(queries,range(1,len(queries)+1)))
    shuffle(queriesSet) 
    return render_template("sqlchecker.html", queries=queriesSet)

@app.route("/AC4", methods=['POST', 'GET'])
def showQueriesAC4():
    if request.method == 'POST':
        query = request.json
        test = checkQuery('jardineria', 'AC4', int(query['no']), query['query'])
        return test
    queries = getExerciceQueries('AC4')
    queriesSet = list(zip(queries,range(1,len(queries)+1)))
    return render_template("sqlchecker.html", queries=queriesSet)

@app.route("/AC3", methods=['POST', 'GET'])
def showQueriesAC3():
    if request.method == 'POST':
        query = request.json
        test = checkQuery('empleados', 'AC3', int(query['no']), query['query'])
        return test
    queries = getExerciceQueries('AC3')
    queriesSet = list(zip(queries,range(1,len(queries)+1)))
    return render_template("sqlchecker.html", queries=queriesSet)
@app.route("/AC2", methods=['POST', 'GET'])
def showQueriesAC2():
    if request.method == 'POST':
        query = request.json
        test = checkQuery('tienda', 'AC2', int(query['no']), query['query'])
        return test
    queries = getExerciceQueries('AC2')
    queriesSet = list(zip(queries,range(1,len(queries)+1)))
    return render_template("sqlchecker.html", queries=queriesSet)

@app.route("/AC1", methods=['POST', 'GET'])
def showQueriesAC1():
    if request.method == 'POST':
        query = request.json
        test = checkQuery('tienda', 'AC1', int(query['no']), query['query'])
        return test
    queries = getExerciceQueries('AC1')
    queriesSet = list(zip(queries,range(1,len(queries)+1)))
    return render_template("sqlchecker.html", queries=queriesSet)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")


# Main program squence ######################################################
app.run()
