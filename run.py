import requests
import json
import numpy as np
from math import ceil
from tqdm import tqdm
from multiprocess import Pool

API_KEY = "91931beef051e70930c0c5bc9a37246b"

#### intro #####
art = '''


             ('-.      .-')    .-') _              _   .-')                 
            ( OO ).-. ( OO ). (  OO) )            ( '.( OO )_               
 ,--.       / . --. /(_)---\_)/     '._    ,------.,--.   ,--.)             
 |  |.-')   | \-.  \ /    _ | |'--...__)('-| _.---'|   `.'   |              
 |  | OO ).-'-'  |  |\  :` `. '--.  .--'(OO|(_\    |         |              
 |  |`-' | \| |_.'  | '..`''.)   |  |   /  |  '--. |  |'.'|  |              
(|  '---.'  |  .-.  |.-._)   \   |  |   \_)|  .--' |  |   |  |              
 |      |   |  | |  |\       /   |  |.-.  \|  |_)  |  |   |  |              
 `------'   `--' `--' `-----'    `--'`-'   `--'    `--'   `--'              
                 .-. .-')  _  .-')     ('-.     _  .-')                     
                 \  ( OO )( \( -O )   ( OO ).-.( \( -O )                    
 ,--.      ,-.-') ;-----.\ ,------.   / . --. / ,------.   ,--.   ,--.      
 |  |.-')  |  |OO)| .-.  | |   /`. '  | \-.  \  |   /`. '   \  `.'  /       
 |  | OO ) |  |  \| '-' /_)|  /  | |.-'-'  |  | |  /  | | .-')     /        
 |  |`-' | |  |(_/| .-. `. |  |_.' | \| |_.'  | |  |_.' |(OO  \   /         
(|  '---.',|  |_.'| |  \  ||  .  '.'  |  .-.  | |  .  '.' |   /  /\_        
 |      |(_|  |   | '--'  /|  |\  \   |  | |  | |  |\  \  `-./  /.__)       
 `------'  `--'   `------' `--' '--'  `--' `--' `--' '--'   `--'            
               ('-.       .-') _  _  .-')     ('-.                          
             _(  OO)     ( OO ) )( \( -O )  _(  OO)                         
  ,----.    (,------.,--./ ,--,'  ,------. (,------.                        
 '  .-./-')  |  .---'|   \ |  |\  |   /`. ' |  .---'                        
 |  |_( O- ) |  |    |    \|  | ) |  /  | | |  |                            
 |  | .--, \(|  '--. |  .     |/  |  |_.' |(|  '--.                         
(|  | '. (_/ |  .--' |  |\    |   |  .  '.' |  .--'                         
 |  '--'  |  |  `---.|  | \   |   |  |\  \  |  `---.                        
  `------'   `------'`--'  `--'   `--' '--' `------'                        
                             .-') _     ('-.  _  .-')                       
                            (  OO) )  _(  OO)( \( -O )                      
   ,------.,-.-')  ,--.     /     '._(,------.,------.                      
('-| _.---'|  |OO) |  |.-') |'--...__)|  .---'|   /`. '                     
(OO|(_\    |  |  \ |  | OO )'--.  .--'|  |    |  /  | |                     
/  |  '--. |  |(_/ |  |`-' |   |  |  (|  '--. |  |_.' |                     
\_)|  .--',|  |_.'(|  '---.'   |  |   |  .--' |  .  '.'                     
  \|  |_)(_|  |    |      |    |  |   |  `---.|  |\  \                      
   `--'    `--'    `------'    `--'   `------'`--' '--'                                    

'''

print(art)
print()
print()

print("###################################################################################################")
print()
print("Filter your last.fm library using genres.")
print("This program fetches all the top 5 tags for all the tracks in your library.")
print("Then it finds which tracks match up with the genres you entered.")
print("The output is a table of tracks and the artist.")
print("Do keep in mind that it takes a fair bit of time.")
print("I would suggest coming back after the ETA.")
print()
print("###################################################################################################")
print()
print("How to use:")
print("1) Enter your username.")
print("2) Input number of genres.")
print("3) Enter the names of the genres. 1 genre per prompt, please.")
print("4) Select whether to sort by how many genres matched or by total playcounts of the songs.\n   Enter 'tags' for genre sorting, or 'plays' for sorting by playcount. " )
print()

#################


#### functions/methods #####
def get(prm):

    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    prm['api_key'] = API_KEY
    prm['format'] = 'json'

    response = requests.get(url, headers = headers, params = prm)
    return response

def tracks(page_no, user):
    user_tracks = {
    'method' : 'user.getTopTracks',
    'user' : user,
    'period' : 'overall',
    'limit' : 1000,
    'page': page_no
    }

    ut = get(user_tracks)
    ut_json = json.loads(ut.text)
    ut_dat = ut_json['toptracks']['track']

    names = [i['name'] for i in ut_dat if 'name' in i]
    artists = [i['artist']['name']  for i in ut_dat if 'artist' in i]
    playcount = [i['playcount'] for i in ut_dat if 'playcount' in i]

    return names, artists, playcount

def tags_track(artist,name):
    tags = {
    'method': "track.getTopTags",
    'artist' : artist,
    'track' : name,
    }
    tag = get(tags)
    tag_json = json.loads(tag.text)['toptags']['tag']
    alltags = [i['name'] for i in tag_json if 'name' in i]
    toptags = alltags[:min(5,len(alltags))]
    
    return toptags

def tags_artist(artist):
    tags = {
        'method': ' artist.getTopTags',
        'artist': artist,
    }
    tag = get(tags)
    tag_json = json.loads(tag.text)['toptags']['tag']
    alltags = [i['name'] for i in tag_json if 'name' in i]
    toptags = alltags[:min(5,len(alltags))]
    
    return toptags


#################


#### INPUTS #####
print('')
while True:
    USER_AGENT = input("Enter your last.fm username: ")

    usr_info = {
        'method' : 'user.getInfo',
        'user' : USER_AGENT,
    }
    ui = get(usr_info)
    if ui.status_code == 200:
        break
    if ui.status_code == 404:
        print("Username not found.\nMaybe you mispelt it.\nPlease try again.")



num_genres = int(input("Enter the number of genres: "))

tmpgenres = []
for i in range(num_genres):
    genre = input(f"Enter genre #{i+1}: ")
    tmpgenres.append(genre)

desired  = np.char.lower(tmpgenres)

while True:
    sortinginp = input("Enter sorting type('tags' or 'plays'): ")
    sorting = np.char.lower(sortinginp)
    if sorting == "tags" or sorting == "plays" or sorting == "tag" or sorting == "play":
        break
    else:
        print("Invalid input. Please enter either 'tags' or 'plays'.")


#################


###getting all tracks####
total_track = int(json.loads(ui.text)['user']['track_count'])
iterations = ceil(total_track/1000)
track_names = []
track_artists = []
track_playcount = []

for _ in tqdm(range(iterations), desc="Collecting Tracks"):
    temp_names, temp_artists, temp_playcount = tracks(_+1, USER_AGENT)
    track_names.extend(temp_names)
    track_artists.extend(temp_artists)
    track_playcount.extend(temp_playcount)

#################

#### getting tags #####
nt_art = np.array([])
nt_tag = np.array([])

taglist = [0 for i in range(total_track)]


for i in tqdm(range(total_track), desc="Collecting track tags"):
    try:
        if track_artists[i] in nt_art:
            n = np.where(nt_art == track_artists[i])[0]
            taglist[i] = nt_tag[n]
            
        else:
            temp_tag = np.array(tags_track(track_artists[i],track_names[i]))
            if temp_tag.size == 0:
                temp_tag = np.array(tags_artist(track_artists[i]))
                nt_art = np.append(nt_art,track_artists[i])
                nt_tag = np.append(nt_tag,temp_tag)
            
            taglist[i] = temp_tag
    except Exception as e:
        print(f"Error occurred: {e}, for track : {track_names[i]}, by {track_artists[i]}")
        taglist[i] = "error_occured"

#################

#### finding tracks with the wanted genres####
common_index = np.array([])
common_count = np.array([]) #storing how many counts of common tags
common_playcount = np.array([])
common_tag = [] 

for i in tqdm(range(total_track), desc="Collecting track tags"):
    common = np.intersect1d(desired, taglist[i])
    aic = len(common) #amount in common

    if aic>0:
        common_tag.append(common)
        common_index = np.append(common_index,i)
        common_count = np.append(common_count,aic)

common_index = np.array(common_index, dtype=int)

if len(common_index) == 0:
    print(":( Sorry, no songs matching the desired genre(s) found.\nPerhaps you misspelled the name of the genre?")
    print("I suggest checking a song you know if of this genre on last.fm to see if you're using the same spelling of the genre,")

else:
    track_names = np.array(track_names)
    track_artists = np.array(track_artists)
    track_playcount = np.array(track_playcount)

    common_tracks = track_names[common_index]
    common_artists = track_artists[common_index]
    common_playcount = track_playcount[common_index]


    max_tags = max(max(len(word) for word in arr) for arr in common_tag)
    max_song = max(len(item) for item in common_tracks)
    max_artist = max(len(item) for item in common_artists)

    int_pc = list(map(int, common_playcount))

    if sorting == "tags" or sorting == "tag":
        #sorting by amount of genre match
        sorted_lists = sorted(zip(common_count, common_tracks, common_artists,int_pc, common_tag), reverse=True)
        sorted_count, sorted_tracks, sorted_artists,common_playcount, sorted_tags = zip(*sorted_lists)
    else:
        #sorting by playcount
        sorted_lists = sorted(zip(int_pc, common_tracks, common_artists, common_tag), reverse=True)
        sorted_playcount, sorted_tracks, sorted_artists, sorted_tags = zip(*sorted_lists)



    digit_count = len(str(len(sorted_tracks)))
    dig_count2 = len(str(len(sorted_playcount)))
    print(dig_count2)

    #################
    outputgenre = [tag for tag in desired]
    outputgenre = ", ".join(outputgenre).replace(",", "_") 
     
    #### printing output ####
    output_file = f'{USER_AGENT}_{outputgenre}.txt'  # Specify the path and filename for the output file
    with open(output_file, 'w') as file:
        header0 = " ".ljust(digit_count)
        header1 = "Track Name".ljust(max_song)
        header2 = "Artist".ljust(max_artist)
        header3 = "Playcount".ljust(dig_count2)
        pc_len = len("playcount")
        header4 = "Genres".ljust(max_tags)
        space = " "
        print(f"{header0} | {header1} | {header2} | {header3} | {header4}\n")
        file.write(f"{header0} | {header1} | {header2} | {header3} | {header4}\n")



        c = 0
        for sorted_tracks, sorted_artists, sorted_playcount, sorted_tags in zip(sorted_tracks, sorted_artists, sorted_playcount,sorted_tags):
            c = c+1

            column1 = sorted_tracks.ljust(max_song)
            column2 = sorted_artists.ljust(max_artist)
            sorted_tags = np.array(sorted_tags).astype(str)
            column3 = [tag.ljust(max_tags) for tag in sorted_tags]
            column3_str = ", ".join(column3).replace(" ,", ",")   
            print(f"{c:0{digit_count}} | {column1} | {column2} | {space:>{pc_len-dig_count2}}{sorted_playcount:0>{dig_count2}}| {column3_str}\n")
            file.write(f"{c:0{digit_count}} | {column1} | {column2} | {space:>{pc_len-dig_count2}}{sorted_playcount:0>{dig_count2}}| {column3_str}\n")

    



