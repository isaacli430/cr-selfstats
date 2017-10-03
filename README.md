# Clash Royale SelfStats
_A selfbot dedicated to getting your CR stats!_

# Installation
## Getting your token
1. Go into Discord and Inspect Element.

<p><img src="https://i.imgur.com/XeGhpvq.png", width="500px"></p>

2. Go into the top bar, click the arrow, and click `Application`.

<p><img src="https://i.imgur.com/lLLlN6C.png", width="500px"></p>

3. Click on the arrow next to `Local Storage`, and click `https://discordapp.com`.

<p><img src="https://i.imgur.com/KO2fr0a.png", width="500px"></p>

4. Double click on the text box next to your token, and copy that text (This is your token).

<p><img src="https://i.imgur.com/N8vkuz1.png", width="500px"></p>

## Local Installation
1. Make sure you have Git and Python 3.6 installed on your computer. If it's your first time installing Python 3.6, go into the Python 3.6 folder, and run `Install Certificates.command`.
2. Go into your Terminal/CMD and type in the following:
```
git clone http://github.com/kwugfighter/cr-selfstats
```
3. When that's done running, type in these commands:
```
cd cr-selfstats
python3 -m pip install -r requirements.txt
python3 bot.py
```
4. Follow the instructions from then on.

## Heroku
1. Create a [Github account](https://github.com/join?source=prompt-code) if you haven't already.
1. Create a [Heroku account](https://id.heroku.com/login) if you haven't already.
2. Fork the repository.

<p><img src="https://i.imgur.com/1vjMymh.png", width="500px"></p>

2. Create a Python app in Heroku.

<p><img src="https://i.imgur.com/gDhfELr.png", width="500px"></p>

3. Go into `Deploy`, and click `Github`. Then, login to Github by pressing `Connect to Github`.

<p><img src="https://i.imgur.com/LC9xmqE.png", width="500px"></p>

4. Type in `cr-selfstats` in the search bar, and click `Connect` on the first result.

<p><img src="https://i.imgur.com/rzSZlo4.jpg", width="500px"></p>

5. Click on `Enable Automatic Deploys` and `Deploy Branch`. Wait for it to finish running.

<p><img src="https://i.imgur.com/rlVbNue.png", width="500px"></p>

6. Go into `Settings`, press `Reveal Config Vars`, and enter in the info as shown here (With your info of course).

<p><img src="https://i.imgur.com/D9mwKer.png", width="500px"></p>

7. Go into `Resources`, click on the pen icon, click on the switch, and press `Confirm`.

<p><img src="https://i.imgur.com/22M81vb.png", width="500px"></p>

8. Now wait around a minute for the bot to boot up.

# Suggestions
If you have any suggestions, create an issue so I can add it.
# Acknowledgements
[@Selfish](https://github.com/selfish) and [@SML](https://github.com/smlbiobot) for creating [cr-api](https://cr-api.com)
