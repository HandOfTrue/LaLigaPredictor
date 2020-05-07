#!/usr/bin/env python3.6
# Marcos del Cueto
import re
import sys
import requests
import unidecode
import pandas as pd
from bs4 import BeautifulSoup

def get_id(medium_name):
    #print('I get inside the function')
    #player_sofifa = None
    medium_name= medium_name.strip()
    #print('try looking for',medium_name)
    url = base_url_sofifa_search + str(medium_name) + "&r=" + str(fifa_year) + "0010&set=true"
    #print('TEST search in sofifa url:',url)
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    for line in soup:
        #print(line)
        #country = re.findall(r"title=.+<a href=\"/players\?pn=",str(line))
        #country = re.findall(r"title=\".+?\"/>",str(country))
        #country = re.findall(r"\".+?\"",str(country))
        #country = re.findall(r"[a-zA-Z ]{2,}",str(country))
        #if country: 
            #country_player.append(country)
            #print('new country found:', country)
        #exact_name = re.findall(rf"<a class=\"tooltip=\".*{medium_name}\" href=\"/player/[0-9]+",str(line))
        exact_name = re.findall(rf"<a class=.+{medium_name}\" href=\"/player/[0-9]+",str(line))
        if exact_name: 
            #print('### TEST EXACT NAME', exact_name)
            id_by_exact_name = re.findall(r"[0-9]+",str(exact_name))
            #print('### TEST ID BY EXACT NAME', id_by_exact_name)
        player_id = re.findall(r"href=\"/player/[0-9]+",str(line))
        player_id = re.findall(r"[0-9]+",str(player_id))
        #print(player_id)
        if player_id:
            player_sofifa_id = player_id
            #print('Inside function, player ID:', player_sofifa_id)
            #print('I got an ID this time:', player_sofifa_id)
            if len(player_sofifa_id)>1:
                if id_by_exact_name[0] in player_sofifa_id:
                    player_sofifa_id = []
                    player_sofifa_id.append(id_by_exact_name[0])
                    print('### WARNING ### More than 1 ID found. Was able to solve it:',id_by_exact_name[0])
                    #print('Inside function, player ID (after curation):', player_sofifa_id)

            return player_sofifa_id,url
    return None,None
    #print('I wasnt able to return a value ##### WARNING #####')



data = []
base_url = 'https://www.bdfutbol.com/en/p/p.php?id='
# Loop over all indeces
for id_index in range(29720,29910):
    # Assign corresponding season
    if id_index >= 25600 and id_index <= 25979:
        Season = 2009
    elif id_index >= 26000 and id_index <= 26379:
        Season = 2010
    elif id_index >= 26643 and id_index <= 27022:
        Season = 2011
    elif id_index >= 27023 and id_index <= 27402:
        Season = 2012
    elif id_index >= 27403 and id_index <= 27782:
        Season = 2013
    elif id_index >= 27783 and id_index <= 28162:
        Season = 2014
    elif id_index >= 28200 and id_index <= 28579:
        Season = 2015
    elif id_index >= 28580 and id_index <= 28959:
        Season = 2016
    elif id_index >= 28960 and id_index <= 29339:
        Season = 2017
    elif id_index >= 29340 and id_index <= 29719:
        Season = 2018
    elif id_index >= 29720 and id_index <= 29909:
        Season = 2019
    else:
        continue
    print('#######################')
    print('New point. Index:', id_index)
    print('#######################')
    # Parse html with BeautifulSoup
    url = base_url + str(id_index)
    #print('#########')
    #print('TEST url:',url)
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    # Loop over each line to extract data
    counter=0
    counter_holder = -1000
    player_name = []
    for line in text:
        if line.rstrip():
            place_holder = re.findall(r"Round+",line)
            #print(line)
            # Use the string 'round' as a place holder to look for data
            if place_holder: 
                counter_holder = counter
                Round = line.split()[4]
                Date = line.split()[6]
            if counter > counter_holder and counter_holder > 0:
                # ignore info about when players scored
                if line.strip()[-1] == "'" or line.strip()[-1] == ")":
                    continue
            # Get TeamHome
            if counter > counter_holder and counter <= counter_holder+1:
                TeamHome = line
            # Get Result
            if counter > counter_holder+1 and counter <= counter_holder+2:
                Result = line.split()[0] + line.split()[1] + line.split()[2]
            # Get TeamAway
            if counter > counter_holder+2 and counter <= counter_holder+3:
                TeamAway = line
            # Get Stadium
            if counter > counter_holder+3 and counter <= counter_holder+4:
                Stadium = line.strip()
            # Get Referee
            if counter > counter_holder+4 and counter <= counter_holder+5:
                Referee = line.strip()
            # Get short names Players
            if counter > counter_holder+7 and counter_holder > 0:
                test = line.strip()
                # stop looking for players after string 'Manager' is found
                if test == 'Manager': break
                # skip line with 'Substitutes' string
                if test == 'Substitutes': continue
                # if possible, transform string to int, to ignore integers
                try:
                    test = int(test)
                except:
                    pass
                is_this_int_with_extra_time = re.findall(r".+\+.+",str(test))
                #if is_this_int_with_extra_time: print('I FOUND INT AT EXTRA TIME', test)
                #print(test,type(test))
                if type(test) == str and not is_this_int_with_extra_time:
                    player_name.append(test)
            counter = counter + 1
    #print(player_name)
    #print('### START bdfutbol ###')
    # Get bdfutbol ID from each player
    player_id_bdfutbol = []
    player_name_complete = []
    base_url_player_bdfutbol = "https://www.bdfutbol.com/en/j/j"
    for p in range(len(player_name)):
        for line in soup:
            #print('newline:', line)
            player_bdfutbol_id = re.findall(rf"<a href=\"../j/j[0-9]+.html\">{player_name[p]}</a>",str(line))
            #print('### test ###:',p, player_name[p], player_bdfutbol_id)
            player_bdfutbol_id = re.findall(r"[0-9]+",str(player_bdfutbol_id))
            if player_bdfutbol_id: 
                #print(p, player_name[p], player_bdfutbol_id)
                player_id_bdfutbol.append(player_bdfutbol_id[0])
                break

    # For each player
    #country_bdfutbol = []
    for p in range(len(player_name)):
    #for p in range(1):
        #print('TEST this is player_name[p]', player_name[p])
        #prev_line=None
        # go to the player page on bdfutbol
        #print('test',p,player_name)
        url_player_bdfutbol = base_url_player_bdfutbol + str(player_id_bdfutbol[p]) + ".html"
        #print('#########################3')
        #print('TEST url:',url_player_bdfutbol)
        res = requests.get(url_player_bdfutbol)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        # for each line in the bdfutbol page of the player
        for line in text:
            if line.rstrip():
                #print(line)
                #if prev_line == 'Birth Country:':
                    #country_bdfutbol.append(unidecode.unidecode(str(line)))
                player_complete_name = re.findall(rf"{player_name[p]}, .+ - Footballer",str(line))
                player_complete_name = re.findall(r",.+-",str(player_complete_name))
                # if we get the complete name of the player:
                if player_complete_name: 
                    #print(p,player_name[p],"##",player_complete_name[0][2:-2])
                    player_name_complete.append(player_complete_name[0][2:-2])
                #prev_line = str(line)
        # if no 'short name, long name' format is provided, use short name as long one
        if p == len(player_name_complete):
            player_name_complete.append(player_name[p])
        #print('p, and length:', p, len(player_name_complete))

    #print(player_name_complete)
    #print('#### END bdfutbol ####')
    #print('')
    #print('### START sofifa ###')
    player_rating = []
    player_potential = []
    fifa_year = int(str(Season)[-2:]) + 1
    #print('FIFA year:', fifa_year)
    base_url_sofifa_search = 'https://sofifa.com/players?keyword='
    base_url_sofifa_player = 'https://sofifa.com/player/'
    # For each player, look in sofifa and get player info
    counter_player=0
    for p in player_name_complete:
        #print('#################')
        #print('NEW PLAYER soFIFA',p)
        medium_name = p
        player_sofifa_id, final_url = get_id(medium_name)
        ##################################
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, try removing last word of long name
            if len(p.split()) > 1:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name = new_name[0:-1]
                medium_name=''
                for i in new_name:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        #################################
        if player_sofifa_id == None:
        ################################        
        # If no ID has been found when searching long name in sofifa, try removing 2nd word from long name
            if len(p.split()) > 2:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name2 = new_name[0:1] + new_name[2:]
                medium_name=''
                for i in new_name2:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        ################################        
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, use only first three names
            if len(p.split()) > 4:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name2 = new_name[0:3]
                medium_name=''
                for i in new_name2:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        ################################        
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, try using just 1 and 3 words
            if len(p.split()) > 3 and p.split()[2] not in ['do','de','di','da','del']:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name2 = new_name[0:1] + new_name[2:3]
                #print('provisional name:',new_name2)
                medium_name=''
                for i in new_name2:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        ################################        
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, try using just 2 first words
            if len(p.split()) > 2:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name2 = new_name[0:2]
                medium_name=''
                for i in new_name2:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        ################################        
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, drop first word
            if len(p.split()) > 2:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name2 = new_name[1:]
                medium_name=''
                for i in new_name2:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        ################################        
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, drop first and last name
            if len(p.split()) > 3:
                #print('long name split words:',p.split())
                new_name=[]
                for i in p.split():
                    new_name.append(i)
                new_name2 = new_name[1:-1]
                medium_name=''
                for i in new_name2:
                    medium_name = medium_name + ' ' + i
                #medium_name = unidecode.unidecode(medium_name)
                player_sofifa_id, final_url = get_id(medium_name)
                if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(medium_name))
        ################################        
        if player_sofifa_id == None:
        #################################
        # If no ID has been found when searching long name in sofifa, try with short name
            player_sofifa_id, final_url = get_id(player_name[counter_player])
        if player_sofifa_id == None: player_sofifa_id, final_url = get_id(unidecode.unidecode(player_name[counter_player]))
        if player_sofifa_id == None:
            print('####################################################################')
            print('ERROR: No ID found when looking in sofifa for:', p)
            print('ERROR: No ID found when looking in sofifa for:', player_name[counter_player])
            print('####################################################################')
            sys.exit()
        if len(player_sofifa_id) == 1:
            #print('I found only one sofifa entry:',p,player_sofifa_id, final_url)
            pass
        elif len(player_sofifa_id) > 1:
            pass
        #<a class="tooltip" data-tooltip="Aitor Fernández" href="/player/193314/aitor-fernandez/200010/"><div class=

            #####################################################
            #####################################################
            #player_sofifa_id2 = []
            #print('IDs:',player_sofifa_id)
            #print('Countries sofifa:', country_player)
            #for c in range(len(country_player[0])):
                #print(country_player[0][c], type(country_player[0][c]))
                #if country_player[0][c] in country_bdfutbol: 
                    #player_sofifa_id2.append(player_sofifa_id[c])
            #print('I finally found sofifa entry(ies):',p,player_sofifa_id2)
            #if len(player_sofifa_id2) == 1:  
                #print('I finally found only one sofifa entry:',p,player_sofifa_id2)
                #player_sofifa_id = player_sofifa_id2
            #####################################################
            #####################################################
        if len(player_sofifa_id) > 1:
            print('####################################################################')
            print('ERROR: More than 1 possible ID when looking in sofifa for:', p)
            print('####################################################################')
            sys.exit()
        counter_player = counter_player+1


        # Once we have one unique ID, get data from that player at corresponding time
        time_label = str(fifa_year) + "0010"
        url = base_url_sofifa_player + str(player_sofifa_id[0]) + "/" + str(time_label)
        #print('Take player info from:',url)
        res = requests.get(url)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        #print(soup)
        counter_line=0
        counter_placeholder=-100
        #prev_line = None
        look_for_sofifa_data = False
        for line in text:
            if line.rstrip():
                #if str(line) == 'FIFA '+str(fifa_year) and find_name_sofifa == True:
                    #name_sofifa = str(prev_line)
                    #find_name_sofifa = False
                    #print('#### I FOUND NAME IN sofifa:', name_sofifa)
                    #print('line is:',line)
                #print(line)
                #if counter_line==1:
                    #print('#### I FOUND NAME IN sofifa:', str(line))
                    #name_sofifa = re.findall(r".+(FIFA)",str(line))
                    #name_sofifa = re.findall(r"<a class=.+{medium_name}\" href=\"/player/[0-9]+",str(line))
                    #pass
                found_this =re.findall(r"^Calculator",str(line))
                if found_this: look_for_sofifa_data = True
                if look_for_sofifa_data == True:
                    name_sofifa = re.findall(r".+\(ID\:.+",str(line))
                    name_sofifa = re.findall(r".+?(?=\(ID\:)",str(name_sofifa))
                    name_sofifa = unidecode.unidecode(str(name_sofifa))
                    name_sofifa = re.findall(r"[a-zA-Z ]{2,}",str(name_sofifa))
                    if name_sofifa: 
                        #print('# Player', p, '---', name_sofifa[0], player_sofifa_id, final_url)
                        if unidecode.unidecode(p) != name_sofifa[0].strip():
                            print('### WARNING ### Player', p, '---', name_sofifa[0], player_sofifa_id, final_url)
                    player_lbs = re.findall(r"lbs$",str(line))
                    if player_lbs: counter_placeholder=counter
                    counter = counter+1
                    if counter == counter_placeholder+2: rating = line
                    if counter == counter_placeholder+4:
                        try:
                            int(line)
                            potential = line
                        except:
                            potential = None
                            pass
                    if counter == counter_placeholder+5 and potential == None:
                        try:
                            int(line)
                            potential = line
                        except:
                            pass
                        #potential = line
                    if counter > counter_placeholder+5 and counter_placeholder > 0: break
                    #prev_line = str(line)
                    #print('test prev_line:', prev_line)
        player_rating.append(int(rating))
        player_potential.append(int(potential))
        #print(p, '. Rating:',int(rating),'. Potential:',int(potential))
    #print('#### END sofifa ####')

    PlayersHome = []
    PlayersHome.append(player_name[0:11]) 
    PlayersHome.append(player_name[22:29]) 

    PlayersAway = []
    PlayersAway.append(player_name[11:22]) 
    PlayersAway.append(player_name[29:36]) 

    ratingHome = []
    ratingAway = []
    ratingHome.append(player_rating[0:11]) 
    ratingHome.append(player_rating[22:29]) 
    ratingAway.append(player_rating[11:22]) 
    ratingAway.append(player_rating[29:36]) 

    potentialHome = []
    potentialAway = []
    potentialHome.append(player_potential[0:11]) 
    potentialHome.append(player_potential[22:29]) 
    potentialAway.append(player_potential[11:22]) 
    potentialAway.append(player_potential[29:36]) 

    #PlayersAway = player_name[11:22] + player_name[29:36]
    #ratingHome = player_rating[0:11] + player_rating[22:29]
    #ratingAway = player_rating[11:22] + player_rating[29:36]
    #RatingHome = sum(ratingHome)
    #RatingAway = sum(ratingAway)
    #potentialHome = player_potential[0:11] + player_potential[22:29]
    #potentialAway = player_potential[11:22] + player_potential[29:36]
    #PotentialHome = sum(potentialHome)
    #PotentialAway = sum(potentialAway)

    #print('Rating Home:', ratingHome)
    #print('SUM Rating Home:', RatingHome)
    #print('Rating Away:', ratingAway)
    #print('SUM Rating Away:', RatingAway)
    #print('Potential Home:', potentialHome)
    #print('SUM Potential Home:', PotentialHome)
    #print('Potential Away:', potentialAway)
    #print('SUM Potential Away:', PotentialAway)


    data_row = [Season,Round,Date,TeamHome,Result,TeamAway,Stadium,Referee,PlayersHome,ratingHome,potentialHome,PlayersAway,ratingAway,potentialAway]
    data.append(data_row)

    df = pd.DataFrame(data,columns=['Season','Round','Date','TeamHome','Result','TeamAway','Stadium','Referee','PlayersHome','RatingHome','PotentialHome','PlayersAway','RatingAway','PotentialAway'])
    
    #print(df.to_string())
    
    df.to_csv (r'test_dataframe.csv', index = False, header=True)
