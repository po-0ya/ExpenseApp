#import needed modules
from tabulate import tabulate
from Api import api
from os import name,system
from sys import argv
import sys

# os type for clear CLI
_osname = name
if _osname == 'nt':
    clear = 'cls'
elif _osname == 'posix':
    clear = 'clear'

#filename, arguments and length of arguments
_filename = argv[0]
args = argv
length = len(args)

def usage() -> None:
    'show the usage of the software'
    system(clear)
    print(f'''
This is an application for recording expenses
Usage:
    Initialize:
        Initial switches : -i --init
        {_filename} -i
    Add record:
        Add switches : -a --add
        {_filename} -a <amount> <category> [<description>]
    View records:
        View switches : -v --view
        {_filename} -v
        {_filename} -v -s <sort-type[asc,desc]>
        {_filename} -v --sort <sort-type[asc,desc]>
        {_filename} -v <category>
        {_filename} -v <category> <sort[T,F]>
        {_filename} -v <category> <sort[T,F]> <sort-type[asc,desc]>
    Help menu:
        Help switches : -h --help
        {_filename} -h
''')

def main():
    #conditions

    #if there is no argument exit and show usage
    if length < 2:
        try:
            usage()
            sys.exit()
        except SystemExit:
            print('Exiting the software...')

    else:
        #if the argument is i or init build db
        if args[1] in ['i','--init'] and length == 2:
            api.init()

        #if argument is a or add, insert next informations to db
        elif args[1] in ['-a','--add'] and length == 4:
            try:
                amount = float(args[2])
                api.add(amount,args[3])
            except ValueError as err:
                print('The amount type should be a NUMBER not string.')
            
            #we passed here because we handled it in our api in the sql class
            #but we should change it soon as possible because this type of exceptions should be handle in api file
            except:
                pass

        #if argument is a or add, insert next informations to db but this one is with description
        elif args[1] in ['-a','--add'] and length == 5:
            try:
                amount = float(args[2])
                api.add(amount,args[3],args[4])
            except ValueError as err:
                print('The amount type should be a NUMBER not string.')
            
            #we passed here because we handled it in our api in the sql class
            #but we should change it soon as possible because this type of exceptions should be handle in api file
            except:
                pass
        
        #if argument is v or view show the all records
        elif args[1] in ['-v','--view'] and length == 2:
            try:
                total, records = api.show()
                print('Total Expenses: %.2f'%(total))
                print(tabulate(records))
            except:
                pass

        elif args[1] in ['-v','--view'] and length == 4 and args[2].lower() in ['-s','--sort'] and args[3].lower() in ['asc','desc']:
            try:
                # breakpoint()
                sort = True
                total, records = api.show(None,sort,args[3].upper())
                print('Total Expenses: %.2f'%(total))
                print(tabulate(records))
            except:
                pass
        
        #if argument is v or view and category is given show all records according to that category
        elif args[1] in ['-v','--view'] and length == 3:
            try:
                total, records = api.show(args[2])
                print('Total Expenses: %.2f'%(total))
                print(tabulate(records))
            except:
                pass

        elif args[1] in ['-v','--view'] and length == 4:
            try:
                if args[3].upper() in ['T','TRUE']:
                    sort = True
                elif args[3].upper() in ['F','FALSE']:
                    sort = False
                else:
                    print('Type of the sort argument should be bool(T-F).')
                total, records = api.show(category=args[2],sort=sort)
                print('Total Expenses: %.2f'%(total))
                print(tabulate(records))
            except:
                pass

        elif args[1] in ['-v','--view'] and length == 5:
            try:
                if args[3].upper() in ['T','TRUE']:
                    sort = True
                elif args[3].upper() in ['F','FALSE']:
                    sort = False
                else:
                    print('Type of the sort argument should be bool(T-F).')
                if args[4].upper() == 'DESC':
                    sorttype = 'DESC'
                else:
                    sorttype = 'ASC'
                total, records = api.show(args[2],sort,sorttype)
                print('Total Expenses: %.2f'%(total))
                print(tabulate(records))
            except:
                pass

        #if second argument is not in the list show help menu again
        elif args[1] in ['-h','--help'] and length == 2:
            usage()

#run
if __name__ == '__main__':
    main()