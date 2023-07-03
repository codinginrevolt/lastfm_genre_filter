Last.fm Library Genre Filter

filter tracks in your library by genres. 

INTRODUCTION:

the project started when i was trying to make a punk playlist in Tidal, only to realise I didn't know which songs i've heard are punk. 
so i went to last.fm to find out and turns out they dont let you sort by genre!! so i wrote some quick code.
this program fetches all the top 5 tags for all the tracks in your library and finds which tracks match up with the genres you enter. 
the output is a table of tracks and the artist, sorted by how many of the genres match the song's tags or how many times you've heard the songs. The output is saved in output.txt.
it runs in terminal right now. i intend to make a website out of this and include some more stuff like being able to add songs to a spotify playlist or something idk
i'll also probably work on making it run faster

it will take a long time to work if your library is big. For my 12k tracks library, it took 30 mins. go for a walk and check when you return.

GETTING STARTED(assuming you have python):
1. make an environment to run it using conda or pip(or you can skip this, im not ur mom):
   terminal command for conda: conda create --name <env_name>
   replace <env_name> with whatever u want
   then activate it with command: conda activate <env_name>

   with pip: python -m venv <env_name>
   if venv isn't install, install with: pip install virtualenv
  next activate the environment.
  on windows:   .\myenv\Scripts\activate
  on linux/mac: source myenv/bin/activate

2. download required libraries using the following command in terminal: pip install -r requirements.txt
3. you should be good to go. run the program in terminal by: python run.py
4. follow the instructions on the terminal
