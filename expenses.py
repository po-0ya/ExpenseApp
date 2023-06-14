#import needed modules
from tabulate import tabulate
from Api import api
from os import name,system,listdir,path,mkdir
from sys import argv
import sys
from argparse import ArgumentParser,Namespace
import os
from Src.clear_screen import clearScreen
from Src.json_load import readJson
from Errors.ArgErrors import *

#define the parser for software
parser = ArgumentParser(prog='expenses',
description='An app that can manage your daily expenses.',
epilog='Coded by Cr0\n[https://github.com/po-0ya]')

#classification of arguments
#TODO check if can handle conflicts
show_group = parser.add_argument_group('Show Record')
input_group = parser.add_argument_group('Add Record')
sort_group = parser.add_argument_group('Sort Option')
delete_group = parser.add_argument_group('Remove Record')

#acceptable arguments 
show_group.add_argument('-v','--view',help='Show the records filter by category -v [category]',action='store')
show_group.add_argument('-va','--viewall',help='Show all the records',action='store_true')

input_group.add_argument('-a','--add',help='Add a new record -a [amount] [category]',action='store',nargs=2)
input_group.add_argument(
    '-m','--message',
    help='Add a message to your record incase if you wanna describe some information about that record -m [message]',
    action='store',nargs='?',default=None)
input_group.add_argument(
    '-j','--json-file',
    help='Store records from a json file so you can save multiple records at once',
    action='store',
    nargs=1)

sort_group.add_argument(
    '-s','--sort',help='Sort the output in ascending or descending order -s [asc/desc]',
    action='store',
    choices=['asc','desc'],
    nargs=1,
    )

delete_group.add_argument('-r','--remove',help='Remove a record from database by ID -r [id]',action='store',nargs=1,type=int)

#parse arguments that i define for parser
args = parser.parse_args()

def main():
    #check conflict inputs
    #TODO it can improve at some ways
    try:
        if (args.remove and (args.add or args.json_file or args.message)):
            raise RemoveCantUseWithAdd()
        if (args.remove and (args.view or args.viewall)):
            raise RemoveCantUseWithView()
        if (args.add and (args.view or args.viewall)):
            raise AddCantUseWithView()
        if (args.add and args.json_file):
            raise AddCantUseWithJson()
    except RemoveCantUseWithAdd:
        print('Cant use -r switch with another switch\nif you wanna remove record use -r single')
        exit()
    except RemoveCantUseWithView:
        print('Cant use -r switch with -v or -va please use them seperatly')
        exit()
    except AddCantUseWithView:
        print('Cant use -a switch with -v or -va please use them seperatly')
        exit()
    except AddCantUseWithJson:
        print('Please use one of this switches\nif you wanna add a single record use -a\nif you wanna add multi records use -j')
        exit()

    #check if the db directory is here or create it
    dbdir = [directory for directory in listdir() if path.isdir(directory)]
    if 'db' not in dbdir:
        mkdir('db')

    #check if there is database file or not to create fresh one
    if 'data.db' not in listdir(r'db/'):
        clearScreen()
        print('Database Created')
        api.init() 

    try:

        #remove the record if it's in database by ID
        if args.remove:
            api.delete(args.remove[0])
            print(f'ID:{args.remove[0]} successfully removed.')

        #add record by json file
        if args.json_file:
            data = readJson(args.json_file[0])
            for item in data:
                if len(item) not in [2,3]:
                    print('Length of items in json file should be at least 2 or 3 (amount,category,[message])')
                    exit()

                if len(item) == 2:
                    api.add(item['amount'],item['category'])
                elif len(item) == 3:
                    api.add(item['amount'],item['category'],item['message'])
            print('Records stored')

        #check if user want to add record with message
        if args.add != None and args.message != None:
            print('Record stored')
            api.add(args.add[0],args.add[1],args.message)
        #else if user want to add record but no without any description
        elif args.add and not args.message:
            print('Record stored')
            api.add(args.add[0],args.add[1])
        
        #it's just columns for header in tabulate
        cols = ['ID','Amount','Category','Description','Date']

        #check if user want to see records filtered by a category and sort them
        if args.view and args.sort != None:
            if 'asc' in args.sort:
                total, records = api.show(args.view,sort=True)
            else:
                total, records =api.show(args.view,sort=True,stype='DESC')
            print(f'Total expenses : {total:.2f}')
            print(tabulate(records,tablefmt='pretty',headers=cols))

        #check if user want to see records filtered by a category
        elif args.view:
            total, records = api.show(args.view)
            print(f'Total expenses : {total:.2f}')
            print(tabulate(records,tablefmt='pretty',headers=cols))

        #check if user want to see all records stored in database with sort format
        if args.viewall and args.sort != None:
            if 'asc' in args.sort:
                total , records = api.show(sort=True)
            else:
                total, records = api.show(sort=True,stype='DESC')
            print(f'Total expenses : {total:.2f}')
            print(tabulate(records,tablefmt='pretty',headers=cols))

        #check if user want to see all records stored in database
        elif args.viewall:
            total , records = api.show()
            print(f'Total expenses : {total:.2f}')
            print(tabulate(records,tablefmt='pretty',headers=cols))

    except Exception as err:
        print(err)
    
#run
if __name__ == '__main__':
    main()