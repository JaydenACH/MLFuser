import tkinter as tk
from tkinter import ttk
import json
import pandas as pd
import pyautogui
import threading
from time import sleep
import sys


#Creating window and it's settings
root = tk.Tk()
root.title('MLfuser')
#root.iconbitmap('')  --Jayden: Not required if not going to customize the icon of the window
root.resizable(width=False, height=False)
# windowPosition = str

#Restores last known position if possible
try:
    with open("config.txt", "r") as f:
        fuseConfig = json.loads(f.read())
        if "geometry" in fuseConfig:
            windowPosition = fuseConfig["geometry"]
            wh, xPos, yPos = windowPosition.split('+')
            root.geometry('427x415+' + xPos + '+' + yPos)
        else:
            root.geometry('427x415')
        f.close
except FileNotFoundError:
    root.geometry('427x415')

#Dictionary = {target : [mob1, mob2, statBonus]}
monsterDict = {
    'Petite Arkarium' : ['Timer', 'Nether Monk', 'Buff Duration +5%'], 
    'Von Bon' : ['Pink Bean', 'Griffey', 'Buff Duration +5%'], 
    'Commander Will' : ['Giant Spider', 'Big Operator Balloon', 'Buff Duration +6%'], 
    'Big Operator Balloon' : ['Small Operator Balloon', 'Small Operator Balloon', 'Skill Cooldown Ignore Chance +2%'], 
    'Petite Eunwol' : ['Petite Luminous (Light)', 'Petite Phantom', 'Skill Cooldown Ignore Chance +4%'], 
    'Petite Orchid' : ['Snow Giant', 'Twin Halloween Bunnies', 'Monster EXP +3%'], 
    'Petite Mercedes' : ['Reinforced Beryl', 'Ephenia', 'Monster EXP +3%'], 
    'Grown-up Mir' : ['Growing Mir', 'Growing Mir', 'All stats +20'], 
    'Growing Mir' : ['Mir', 'Mir', 'Abnormal status resistance +5'], 
    'Mir' : ['Snow Giant', 'Lupin Pig', 'Weapon/Magic ATT +5'], 
    'Petite Luminous (Dark)' : ['King Slime', 'Papulatus Watch', 'Weapon/Magic ATT +5'], 
    'Shadow of Black Mage' : ['Petite Luminous (Dark)', 'Master Omen', 'Weapon/Magic ATT +6'], 
    'Petite Luminous (Equilibrium)' : ['Petite Luminous (Light)', 'Petite Luminous (Dark)', 'Weapon/Magic ATT + 1 per 20 character levels'], 
    'Petite Hilla' : ['Riche', 'Elite Bloodfang', 'Critical damage +2%'], 
    'Romancist King Slime' : ['King Slime', 'Yeti Couple In Love', 'Critical rate +3%'], 
    'Petite Horntail' : ['Leviathan', 'Snow Witch', 'Critical rate +3%'], 
    'Petite Phantom' : ['Moon Bunny Thief', 'Romancist King Slime', 'Critical rate +4%'], 
    'Lazuli' : ['Eye of Time', 'Petite Hilla', 'Critical rate +5%'], 
    'Black Viking' : ['Viking Legion', 'Sober Viking', 'Damage +2%, DEX +5'], 
    'Petite Cygnus' : ['Shinsoo', 'Oberon', 'Damage +3%'], 
    'Scarecrow' : ['Thief Crow', 'Petite Arkarium', 'Damage +4%'], 
    'Petite Von Leon' : ['Lilynouch', 'Toy Black Knight', 'Damage to boss monsters +5%'], 
    'Lil Moonbeam' : ['Nine-Tailed Fox', 'Petite Orchid', 'Damage on boss monsters +8% ''if Petite Eunwol is alive'], 
    'Petite Magnus' : ['Crimson Balrog', 'Apsu', 'Ignore DEF +5%'], 
    'Lapis' : ['Eye of Time', 'Ifrit', 'Ignore DEF +5%'], 
    'Tin Woodman' : ['Inner Rage', 'Victor', 'Ignore DEF +6%'],
    'Pierre' : ['Jr Balrog', 'Targa', 'Final attack type skills damage +15%']
    }

#Dictionary = {sourceMob : sheet_name}
mobSheet = {
    'Apsu' : 'Apsu', 
    'Big Operator Balloon' : 'Big Balloon', 
    'Crimson Balrog' : 'Crimson Balrog', 
    'Elite Bloodfang' : 'Elite Bloodfang', 
    'Ephenia' : 'Ephenia', 
    'Eye of Time' : 'Eye Of Time', 
    'Giant Spider' : 'Giant Spider', 
    'Griffey' : 'Griffey', 
    'Growing Mir' : 'Growing Mirr', 
    'Ifrit' : 'Ifrit', 
    'Inner Rage' : 'Inner Rage', 
    'Jr Balrog' : 'Jr. Balrog', 
    'King Slime' : 'King Slime', 
    'Leviathan' : 'Leviathan', 
    'Lilynouch' : 'Lilynouch', 
    'Lupin Pig' : 'Lupin Pig', 
    'Manon' : 'Manon', 
    'Master Omen' : 'Master Omen',
    'Mir' : 'Mirr',  
    'Moon Bunny Thief' : 'Moon Bunny Thief', 
    'Nether Monk' : 'Nether Monk', 
    'Nine-Tailed Fox' : 'Nine-Tailed Fox', 
    'Oberon' : 'Oberon', 
    'Papulatus Watch' : 'Papu Clock', 
    'Petite Arkarium' : 'Petite Arka', 
    'Petite Hilla' : 'Petite Hilla', 
    'Petite Luminous (Dark)' : 'Petite Lumi (Dark)', 
    'Petite Luminous (Light)' : 'Petite Lumi (Light)', 
    'Petite Orchid' : 'Petite Orchid', 
    'Petite Phantom' : 'Petite Phantom', 
    'Pink Bean' : 'Pink Bean', 
    'Reinforced Beryl' : 'Reinforced Beryl', 
    'Riche' : 'Riche', 
    'Romancist King Slime' : 'Romancist KS', 
    'Shinsoo' : 'Shinsoo', 
    'Small Operator Balloon' : 'Small Balloon', 
    'Snow Giant' : 'Snow Giant', 
    'Snow Witch' : 'Snow Witch', 
    'Sober Viking' : 'Sober Viking', 
    'Targa' : 'Targa', 
    'Thief Crow' : 'Thief Crow', 
    'Timer' : 'Timer', 
    'Toy Black Knight' : 'Toy Black Knight', 
    'Twin Halloween Bunnies' : 'Twin H.Bunnies', 
    'Victor' : 'Victor', 
    'Viking Legion' : 'Viking Legion', 
    'Yeti Couple In Love' : 'Yeti Couple'
    }
#Encodes sheet_name using percent encoding + ASCII code
for key, value in mobSheet.items():
    mobSheet[key] = value.replace(" ", "%20").replace("(", "%28").replace(")", "%29")

#List = [mobs to keep]
keepList = [
    'Elite Bloodfang', 'Eye of Time', 'Griffey', 'Ifrit', 
    'King Slime', 'Leviathan', 'Lupin Pig', 'Manon', 'Master Omen',
    'Nether Monk', 'Nine-Tailed Fox', 'Riche', 'Snow Giant', 
    'Sober Viking', 'Targa', 'Thief Crow', 
    'Toy Black Knight', 'Victor'
]

#List = [farms with alive mobs from google docs]
farmList = []

#Dictionary = {imageStr : ImageNotFoundError's massage}
imageError = {
    'greyMaple' : 'Please make Maple visable on the screen'
}

#Creating varibles
target = tk.StringVar(value='Select Target Mob')
mobNum = tk.IntVar(value=0)
mob1 = 'Source mob 1'
mob2 = 'Source mob 2'
farm = tk.StringVar()
keep0 = tk.BooleanVar()
keep1 = tk.BooleanVar()
keep2 = tk.BooleanVar()
keep3 = tk.BooleanVar()
keep4 = tk.BooleanVar()
keep5 = tk.BooleanVar()
keep5 = tk.BooleanVar()
keep5 = tk.BooleanVar()
keep6 = tk.BooleanVar()
keep7 = tk.BooleanVar()
keep8 = tk.BooleanVar()
keep9 = tk.BooleanVar()
keep10 = tk.BooleanVar()
keep11 = tk.BooleanVar()
keep12 = tk.BooleanVar()
keep13 = tk.BooleanVar()
keep14 = tk.BooleanVar()
keep15 = tk.BooleanVar()
keep16 = tk.BooleanVar()
keep17 = tk.BooleanVar()

#Saving window's last position for next use
def onClose():
    windowPosition = root.geometry() #Save the current position of the window
    with open("config.txt", "a+") as f:
        f.seek(0) #Move the pointer to the beginning of the file
        data = f.read()
        if len(data)==0:
            fuseConfig = {"geometry": windowPosition}
            json.dump(fuseConfig, f, indent=4)
        else:
            fuseConfig = json.loads(data)
            fuseConfig["geometry"] = windowPosition
            f.seek(0)
            f.truncate() #Removes all the data from the file after the current position of the file pointer, up to the end of the file
            json.dump(fuseConfig, f, indent=4)
        f.close()

    root.destroy()

#Update stat bonus and source mobs when new target mob selected
def targetDropChanged(event):
    global farmList
    statBonus = monsterDict[str(target.get())][2]
    statLabel.config(text=statBonus)
    mob1 = monsterDict[str(target.get())][0]
    radio1.config(text=mob1)
    mob2 = monsterDict[str(target.get())][1]
    radio2.config(text=mob2)
    farm.set('Please Press Update Farms')
    farmList = []
    farmDrop.config(textvariable=farm, values=farmList)
    startButton.config(state=tk.DISABLED)
    statusLabel.config(text='Stat bouns and source mobs updated')

#Calls for the farms for the target mob from google docs
def updateFarm():
    global farmList
    sourceMob = monsterDict[str(target.get())][int(mobNum.get())]
    sheet_id = '1um4UKZcYwRwRSjQh8i_5ujsJEt9AtDiR5nIZsD_9JtY'
    sheet_name = mobSheet.get(sourceMob, '( )')

    statusLabel.config(text='Retriving data from google docs')
    try:
        # Read the data from the Google Sheets document and store it in a DataFrame
        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}")
        # Select the rows in the DataFrame that have a value greater than 0 in column E
        statusLabel.config(text='Packing farms into a list')
        df = df.loc[df['Unnamed: 4'] > 0]
        # Reset the index of the resulting DataFrame
        df = df.reset_index()
        # Select the first column of the resulting DataFrame
        data = df.iloc[:, 1]
        # Transfers the names into a list
        for i in data:
            farmList.extend([i])
        farm.set(farmList[0])
        farmDrop.config(textvariable=farm, values=farmList)
        startButton.config(state=tk.NORMAL)
        statusLabel.config(text='Farms updated')
    except ConnectionError:
        statusLabel.config(text='Cannot connect to the google docs')
    except KeyError:
        statusLabel.config(text='Excel sheet name cannot be found')
    
#General Image scan
def imageScan(imageStr, dir):
    global image
    scanEvent = threading.Event()
    try:
        image = pyautogui.locateCenterOnScreen('Images/' + dir + imageStr + '.png')
        print(image)
        if not image:
            statusLabel.config(text=imageError[imageStr])
            print('2')
            callIDscan = root.after(1000, imageScan, imageStr, dir)
            print('3')
        else:
            try:
                root.after_cancel(callIDscan)
            except:
                pass
            scanEvent.set()
            print('4')
    except FileNotFoundError:
        statusLabel.config(text='Search image ' + imageStr + ' cannot be found')
    scanEvent.wait()
    print('5')
    return image
    # image = 0
    # try:
    #     while not image:
    #         image = pyautogui.locateCenterOnScreen('Images/' + dir + imageStr + '.png')
    #         print(f"in while loop: {image}") if image is None else print("\n")
    # except KeyboardInterrupt:
    #     print("Done")
    # except FileNotFoundError:
    #     statusLabel.config(text='Search image ' + imageStr + ' cannot be found')
    # print(f"outside while loop: {image}")
    # return image


#Searching the farms
def farmSearch(i):

    friendList = pyautogui.locateCenterOnScreen('Images/friendList.png')
    return

def prestartCheck():
    greyMaple = imageScan('greyMaple', '')
    pyautogui.click(x=greyMaple.x+63, y=greyMaple.y+127)
    pyautogui.press('esc')
    return

#Starts the fusing process
def startFuse():
    global farmList
    global farm
    global stop
    stop = False
    statusLabel.config(text='Starting')
    targetDrop.config(state=tk.DISABLED)
    farmDrop.config(state=tk.DISABLED)
    updateButton.config(state=tk.DISABLED)
    startButton.config(text='Pause', command=pauseFuse)
    stopButton.config(state=tk.NORMAL)
    farmIndex = farmList.index(farm.get())
    sleep(0.5)
    prestartCheck()
    #farmSearch(farmIndex)
    print('TestComplete')
    return

#Pauses the fusing process
def pauseFuse():
    startButton.config(text='Resume', command=resumeFuse)
    stopButton.config(state=tk.NORMAL)
    return

#Resumes after pausing the fusing process
def resumeFuse():
    startButton.config(text='Pause', command=pauseFuse)
    stopButton.config(state=tk.NORMAL)
    return

#Stops and resets the fusing process
def stopFuse():
    targetDrop.config(state=tk.NORMAL)
    farmDrop.config(state=tk.NORMAL)
    updateButton.config(state=tk.NORMAL)
    startButton.config(text='Start', command=startFuse)
    stopButton.config(state=tk.DISABLED)
    return

#Creating widgets
label1 = tk.Label(root, text='Target Mob :')
label2 = tk.Label(root, text='Stat Bonus :')
label3 = tk.Label(root, text='Source Mob :')
label4 = tk.Label(root, text='Starting Farm :')
label5 = tk.Label(root, text='Last Farm Used :')
label6 = tk.Label(root, text='Program Status :')
keepFrame = tk.LabelFrame(root, text='Mobs to keep :')
targetDrop = ttk.Combobox(root, textvariable=target, state='readonly', values=list(monsterDict.keys()))
targetDrop.bind('<<ComboboxSelected>>', targetDropChanged)
targetDrop.config(width=47)
statLabel = tk.Label(root, text='')
radio1 = tk.Radiobutton(root, text=mob1, variable=mobNum, value=0)
radio2 = tk.Radiobutton(root, text=mob2, variable=mobNum, value=1)
radio2.deselect
farmDrop = ttk.Combobox(root, textvariable=farm, state='readonly', values=farmList)
farmDrop.config(width=47)
farmLabel = tk.Label(root, text='')
updateButton = tk.Button(root, text='Update Farm', command=updateFarm, width=15)
statusLabel = tk.Label(root, text='')
keepFrame = tk.LabelFrame(root, text='Mob to keep :')
check0 = tk.Checkbutton(keepFrame, text='Elite Bloodfang', variable=keep0)
check1 = tk.Checkbutton(keepFrame, text='Eye of Time', variable=keep1)
check2 = tk.Checkbutton(keepFrame, text='Griffey', variable=keep2)
check3 = tk.Checkbutton(keepFrame, text='Ifrit', variable=keep3)
check4 = tk.Checkbutton(keepFrame, text='King Slime', variable=keep4)
check5 = tk.Checkbutton(keepFrame, text='Leviathan', variable=keep5)
check6 = tk.Checkbutton(keepFrame, text='Lupin Pig', variable=keep6)
check7 = tk.Checkbutton(keepFrame, text='Manon', variable=keep7)
check8 = tk.Checkbutton(keepFrame, text='Master Omen', variable=keep8)
check9 = tk.Checkbutton(keepFrame, text='Nether Monk', variable=keep9)
check10 = tk.Checkbutton(keepFrame, text='Nine-Tailed Fox', variable=keep10)
check11 = tk.Checkbutton(keepFrame, text='Riche', variable=keep11)
check12 = tk.Checkbutton(keepFrame, text='Snow Giant', variable=keep12)
check13 = tk.Checkbutton(keepFrame, text='Sober Viking', variable=keep13)
check14 = tk.Checkbutton(keepFrame, text='Targa', variable=keep14)
check15 = tk.Checkbutton(keepFrame, text='Thief Crow', variable=keep15)
check16 = tk.Checkbutton(keepFrame, text='Toy Black Knight', variable=keep16)
check17 = tk.Checkbutton(keepFrame, text='Victor', variable=keep17)
startButton = tk.Button(root, text='Start', state=tk.DISABLED, command=startFuse, width=22)
stopButton = tk.Button(root, text='Stop', state=tk.DISABLED, command=stopFuse, width=22)


#Packing widgets onto window
label1.grid(row=0, column=0, sticky='e', padx=5, pady=5)
label2.grid(row=1, column=0, sticky='e', padx=5, pady=5)
label3.grid(row=2, column=0, sticky='e', padx=5, pady=5)
label4.grid(row=3, column=0, sticky='e', padx=5, pady=5)
label5.grid(row=4, column=0, sticky='e', padx=5, pady=5)
label6.grid(row=5, column=0, sticky='e', padx=5, pady=5)
keepFrame.grid(row=6, column=0, columnspan=3, sticky='e', padx=0, pady=5)
targetDrop.grid(row=0, column=1, columnspan=2)
statLabel.grid(row=1, column=1, columnspan=2)
radio1.grid(row=2, column=1)
radio2.grid(row=2, column=2)
farmDrop.grid(row=3, column=1, columnspan=2)
farmLabel.grid(row=4, column=1, sticky='w')
updateButton.grid(row=4, column=2, sticky='e', padx=0, pady=5)
statusLabel.grid(row=5, column=1, columnspan=2, sticky='w')
check0.grid(row=0, column=0, sticky='w', padx=8)
check1.grid(row=1, column=0, sticky='w', padx=8)
check2.grid(row=2, column=0, sticky='w', padx=8)
check3.grid(row=3, column=0, sticky='w', padx=8)
check4.grid(row=4, column=0, sticky='w', padx=8)
check5.grid(row=5, column=0, sticky='w', padx=8)
check6.grid(row=0, column=1, sticky='w', padx=8)
check7.grid(row=1, column=1, sticky='w', padx=8)
check8.grid(row=2, column=1, sticky='w', padx=8)
check9.grid(row=3, column=1, sticky='w', padx=8)
check10.grid(row=4, column=1, sticky='w', padx=8)
check11.grid(row=5, column=1, sticky='w', padx=8)
check12.grid(row=0, column=2, sticky='w', padx=8)
check13.grid(row=1, column=2, sticky='w', padx=8)
check14.grid(row=2, column=2, sticky='w', padx=8)
check15.grid(row=3, column=2, sticky='w', padx=8)
check16.grid(row=4, column=2, sticky='w', padx=8)
check17.grid(row=5, column=2, sticky='w', padx=8)
startButton.grid(row=7, column=0, columnspan=2, sticky='w', padx=20, pady=5)
stopButton.grid(row=7, column=1, columnspan=2, sticky='e', padx=0, pady=5)


root.protocol("WM_DELETE_WINDOW", onClose)
root.mainloop()

