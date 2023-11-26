#  Written by Vladislav Glinkin
#  mongo.py provides functions for working with MongoDB

import json
import pymongo
from pymongo import errors, database
import os


client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_database = pymongo.database.Database(client=client, name="spectacles_database")
collection = pymongo.collection.Collection(database=mongo_database, name="spectacles", create=False)


def json_into_mongodb():
    print('Connecting to MongoDB...')
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        list_of_databases = client.list_database_names()
        if list_of_databases.count('spectacles_database') == 0:
            mongo_database.create_collection(name='spectacles')
        for spectacle in os.listdir('spectacles'):
            file = open(f'spectacles/{spectacle}', mode='r')
            collection.insert_one(json.load(file))
            file.close()
        print('Writing JSON into database completed')
        print(f'Number of documents in the collection: {collection.count_documents({})}')


def show_all_spectacles():
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        for document in collection.find():
            print(document)


def search_by_spectacle_name(spectacle_name):
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        for document in collection.find({'spectacle_name': spectacle_name}):
            print(document)


def search_by_director(director):
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        for document in collection.find({'actors': director}):
            print(document)


def search_by_actor(actor):
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        for document in collection.find({'actors': actor}):
            print(document)


def spectacles_without_dates():
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        for document in collection.find({'dates': None}):
            print(document)


def spectacles_without_information():
    try:
        client.server_info()
    except pymongo.errors.ConnectionFailure:
        print('Connection impossible')
    else:
        for document in collection.find({'director': None, 'actors': None, 'dates': None}):
            print(document)
