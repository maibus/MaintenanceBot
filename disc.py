import asyncio
import discord
from discord.ext.tasks import loop
from discord.ext import tasks, commands
import numpy as np
import matplotlib.pyplot as plt
import nltk   
from urllib.request import urlopen
import requests
import urllib
import html5lib
from bs4 import BeautifulSoup
import re

Fcount = np.load("Fcount.npy")
Mcount = np.load("Mcount.npy")
names = np.load("names.npy")
points = np.load("points.npy")
msgvar = 0
group_names = ['Spark Platoon','Nova Platoon','Pyro Platoon','Ember Platoon']
print(names,points)

TOKEN = 'NjY0MTU2MGJfdcfGVy.XhS9oQ.CUnbLOgGBB-OCkDmrP0mMphrlDA'#fake token
client = discord.Client()
    
@client.event
async def on_message(message):
    global msgvar
    global group_names
    msgvar += 1
    auth_names = ['Sergeant','Sergeant Major','Drill Sergeant','Lieutenant','2nd Lieutenant','Captain']
    auths = []
    for n in range(len(auth_names)):
        auths.append(discord.utils.find(lambda r: r.name == auth_names[n], message.guild.roles))
    def prime_factors(n):  #fun function for !tag_factors function
        i = 2
        factors = []
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors
    if message.author == client.user:#dont want bot replying to itself
        return
    if message.content.startswith('!roles'):#giving roles
        role_list = ["PC", "X-box", "PS4"] 
        vals = message.content.split(",")
        print(vals[1])
        inp = vals[1]
        inp0 = vals[0]
        inp0 = inp0[6:]
        x = message.guild.members
        a = 0
        for member in x:
            x[a] = member.display_name
            a += 1
        x = x[:-1]
        for i in range(0,len(x)):
            temp = list(x[i])
            for j in range(len(temp)):
                if temp[j] == '"':
                    x[i] = temp[j:]
                    break
            temp = x[i]
            put = str()
            for j in range(1,len(temp)-1):
                put += temp[j]
            x[i] = put        
        temp = list(inp0)
        inp0 = inp0[1:]
        inp0 =  ''.join(inp0)
        FLIP = False
        for i in range(len(x)):
            inp01 = list(inp0)
            inp01 = inp01[1:-1]
            inp01 =  ''.join(inp01)
            if x[i] == inp01:
                print("nein")
                FLIP = True
        inp0 = 'CT-'+' '+message.author.discriminator+' '+inp0
        if inp[0] == ' ':
            inp = inp[1:]
        role = discord.utils.get(message.guild.roles,name=inp)
        channel = message.channel
        if role is None or role.name not in role_list:
            print("b")
            await message.channel.send('These arent the roles youre looking for... ')
            return
        else:
            print("a")
            await message.author.add_roles(role)
            await message.channel.send('Role succesfully added')
        if FLIP == False:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout = 180.0)
            except asyncio.TimeoutError:
                pass
            else:
                print(reaction)
                if str(reaction) == '✅':
                    print(reaction,"A")
                    print(inp0)
                    await message.author.edit(nick=inp0)
                    await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="Cadet"))
                else:
                    print(reaction,"B")
                    await message.channel.send('Its treason then! (Your name has not been approved, please wait for an SCO to make contact.)')
        else:
            await message.channel.send('Now there are two of them, this is getting out of hand! (this name is already taken, try another)')
#        await client.add_roles(member,role)#client.send_message(message.channel, msg)
    if message.content.startswith('!members'):
        x = message.guild.members
        for member in x:
            print(member.display_name)
        print(len(x))
    if message.content.startswith('!warn'):
        auth = not set(message.author.roles).isdisjoint(auths)#cheks if user has any of the leadership roles stored in auths
        if auth == True:
            names = np.load("names.npy")
            points = np.load("points.npy")
            vals = message.content.split(",")
            name = vals[0]
            name = name[6:]
            point = float(vals[1])
            if name not in names:
                print("hi")
                names = np.append(names,name)
                points = np.append(points,point)
                await message.channel.send("First time offence successfully registered")
                print(names)
                print(points)
                np.save("names",names)
                np.save("points",points)
            else:
                print("e")
                temp = list(names)
                points[temp.index(name)] += point
                out = ''
                out += "Offence successfully registered, "
                out += str(int(points[temp.index(name)]))
                out += " points total"
                await message.channel.send(out)
                print(names)
                print(points)
                np.save("names",names)
                np.save("points",points)
        else:
            await message.channel.send("It's treason then! (Sorry, you cant use this command.)")
    if message.content.startswith('!offences'):
        names = np.load("names.npy")
        points = np.load("points.npy")
        name = message.content
        print(name)
        name = name[10:]
        print(name)
        temp = list(names)
        try:
            await message.channel.send(int(points[temp.index(name)]))
        except ValueError:
            await message.channel.send("No Offences")
    if message.content.startswith("!graph"):
        vals = message.content.split(',')
        if vals[1] == "messages":
            print("Graphed")
            Mcount = np.load("Mcount.npy")
            fig = plt.figure()
            ax = fig.gca()
            ax.plot(np.linspace(0,len(Mcount)/6,len(Mcount)),Mcount,c='black')
            plt.xlabel("Time(hours)")
            plt.ylabel("Messages")
        elif vals[1] == "members":
            print("Graphed")
            Fcount = np.load("Fcount.npy")
            Total = np.sum(np.reshape(Fcount,[4,int(len(Fcount)/4)]),axis=0)
            fig = plt.figure()
            ax = fig.gca()
            for a in range(len(group_names)):
                ax.plot(np.linspace(0,len(Fcount)/24,len(Fcount)/4),Fcount[a:][::len(group_names)],label=group_names[a])
            ax.plot(np.linspace(0,len(Fcount)/24,len(Fcount)/4),Total,c='black',label="Total")
            plt.xlabel("Time(hours)")
            plt.ylabel("Members")
            plt.legend()
        plt.savefig("disc_graph.png")
        ax.clear()
        plt.close("all")
        await message.channel.send(file=discord.File('disc_graph.png'))
    if message.content.startswith('!wookie'):
        vals = message.content.split(',')
        Query = str(vals[1])
        URL = "https://starwars.fandom.com/wiki/Special:Search?query={}".format(Query)
        r = requests.get(URL) 
        soup = BeautifulSoup(r.content, 'html5lib') 
        cont = str(soup.prettify())
        i = 0
        for match in re.finditer('https', cont):
            i += 1
            if i == 36:
                temp_url = str(cont[match.start():match.end()+100])
                sppos = temp_url.find('"')
                new_url = temp_url[:sppos]
                break
        print(new_url)

        r = requests.get(new_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        cont = str(soup.prettify())
        seg = cont[:cont.find("twitter:description")-11]
        back = seg[::-1]
        cut = back[:back.find('"')]
        search = cut[::-1]

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        holder = text[text.find(search):]
        print(holder.split("\n")[0])
        await message.channel.send(new_url)
        await message.channel.send(holder.split("\n")[0])
        
    if message.content.startswith('!tag_factors'):
        rolespk = discord.utils.find(lambda r: r.name == 'Spark Platoon', message.guild.roles)
        print(sum(member.status!=discord.Status.offline and not member.bot and rolespk in member.roles for member in message.guild.members))
        await message.channel.send(prime_factors(int(message.author.discriminator)))
'''
    if message.content.startswith('Im') or message.content.startswith('im')or message.content.startswith('I\'m') or message.content.startswith('i\'m'):
        out = str(message.content)
        num = 0
        for i in range(len(out)):
            num += 1
            if out[i] == ' ':
                break
        put = ''
        put += 'Hi '
        put += out[int(num):]
        put += ', I\'m Dad'
        print("gotteem")
        print(message.author)
        await message.channel.send(put)
'''


@tasks.loop(seconds=600.0)
async def slow_count():
    global msgvar
    global group_names
    Fcount = np.load("Fcount.npy")
    Mcount = np.load("Mcount.npy")
    try:
        Mcount = np.append(Mcount,msgvar)
    except NameError:
        pass
    np.save("Mcount",Mcount)
    msgvar = 0
    guild = client.get_guild(646793342595760150)
    memberson = sum(member.status!=discord.Status.offline and not member.bot for member in guild.members)
    print(memberson)
    groups = []
    for n in range(len(group_names)):
        groups.append(discord.utils.find(lambda r: r.name == group_names[n], guild.roles))
    on_array = []
    for m in range(len(groups)):
        on_array.append(sum(member.status!=discord.Status.offline and not member.bot and groups[m] in member.roles for member in guild.members))      
    Fcount = np.append(Fcount,on_array)
    print(on_array)
    np.save("Fcount",Fcount)
    print(slow_count.current_loop)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    slow_count.start()
client.run(TOKEN)
