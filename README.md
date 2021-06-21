# Mobility destination picker
### Overview
Every student that has ever gone studying abroad knows that choosing destination is a real hustle, and there is no simple way to compare universities. Two of our members has been recently through this process, so we decided to attempt creating a solution during the HackUPC. Mobility destination picker is a Telegram Bot with a similar structure to the popular game Akinator. Through a series of simple questions and 5 possible answers, the program finds the University that fits the user better while trying to keep the number of questions as small as possible.

### Structure
- ``main.py`` contains the structure of the algorithm and the main caller functions, as well as some general behaviour and logic functions.
- ``dataparser.py`` contains the functions to read and normalize the data.
- ``bayes.py`` contains the algorithm used to update the prior probabilities of each university.
- ``best_question.py`` contains the algorithm used to find the most relevant question to ask.
- ``bot.py`` contains the entire code used to control the Telegram bot.

### Datasets
We have two aviable datasets to use:
- dataBig contains over 1000 universities, but its values were set randomly. While it is a great to test the performance of the code, its results won't accurately represent the best universities for the user.
- dataSmall contains around 20 universities, but its values have been manually introduced. Therefore, the results can be expected to match the interests of the user.

### How to run the bot
If you wish to run this bot on your own server, just follow these steps:
<ol>
  <li> Chat up @BotFather on Telegram.  </li>
  <li> Type in /newbot. Then specify your bot's id and username. </li>
  <li> BotFather will then give you a token (a large string of secret characters). Write this token on a file called token.txt and put it on the same folder where the project's code is located.</li>
  <li> Just run the script bot.py and your bot will be running! </li>
</ol>
Once you have it running, anyone can chat with your bot once you give them its ID (@...). The bot can handle multiple users concurrently, no problem!


### About us
We are **CorruptedBits**, a team formed by three students of the degree of Data Science and Engineering in UPC. We are very passionate about coding and learning :)

Members:
* Álvaro Francesc Budria
* Jaume Ros
* Miquel Martínez de Morentin
