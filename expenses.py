#import needed modules
from tabulate import tabulate
from Api import api
from os import name,system,listdir,path,mkdir
from sys import argv
import sys
from argparse import ArgumentParser,Namespace
import os

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

sort_group.add_argument(
    '-s','--sort',help='Sort the output in ascending or descending order -s [asc/desc]',
    action='store',
    choices=['asc','desc'],
    nargs=1,
    )

delete_group.add_argument('-r','--remove',help='Remove a record from database by ID -r [id]',action='store',nargs=1,type=int)

#parse arguments that i define for parser
args = parser.parse_args()

#clear commandline
def clearScreen() -> None:
    ostype = name
    if ostype == 'nt':
        clear = 'cls'
    elif ostype == 'posix':
        clear = 'clear'
    system(clear)

def main():
    
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

        #remove the record if it's in database by ID
        if args.remove:
            api.delete(args.remove[0])
            print(f'ID:{args.remove[0]} successfully removed.')
            
    except Exception as err:
        print(err)
    
#run
if __name__ == '__main__':
    main()