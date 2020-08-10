=========================================================================================
=======================================[ Who am I? ]=====================================
=========================================================================================

Script made by:         SirPhilthyOwl (An Owl)
Twitch:                 http://www.twitch.tv/SirPhilthyOwl

=========================================================================================
=======================================[ Script Changes ]================================
=========================================================================================

Kappa anywhere v1.0.7


Previous versions:
v1.0.7 Removed the 10 special Emote cap, moved everything into textfile. INFINITE TRIGGERS!

v1.0.6 Added $sound() parameter, added blacklist, changed Special emotes 1 tab to be used as welcome message
       Rewritten ReadMe to be more "readable"

v1.0.5 Added multiple line output, added $file() parameter

v1.0.4 Added single mode as a special emote/message combination. Added multiple special message additions.

v1.0.3 Added cooldown for both General and Special emotes. Special emotes have independent cooldowns.

v1.0.2 Added Permission levels for general and specialized

v1.0.1 Changed Combo and Non-combo checkbox to dropdown.

v1.0.0 Script made.

=========================================================================================
=======================================[ Foreword ]======================================
=========================================================================================

This idea came from the simple fact that the chatbot custom command can't trigger in the middle of a sentence.
Many streamers have the "Kappa" custom command where the bot will respond "Kappa" back.
But only if the word is used at the beginning of the sentence.

This prompted me to write a script that could detect emotes anywhere in the sentences.
Over the several versions more options has been added, and now the script has grown into something bigger
than the original plan was.

There are many word trigger scripts made, but this one adds many more features than most of them.


I hope you have fun using this script!


=========================================================================================
=======================================[ Settings ]======================================
=========================================================================================

In the general tab you can turn off whichever module you don't want to use, by simple unchecking the checkbox.

In the blacklist textbox you can add users (case sensitive) so they don't trigger any module of the script.


=========================================================================================
=======================================[Advanced Settings ]==============================
=========================================================================================

The breakline character is the parameter the bot looks for when you want to set multiple random messages (see emote message).

This is default "|", but if you wanted to use the character "|" in your messages, you can set a new breakline character.

Likewise with the "~" character, which is a parameter to split your message in multiple message output in chat.

You could change this value if you want to be able to use "~" in your messages.



Be adviced, if you're not planning on using "|" or "~" in your messages, leave these values default.
If you did change this to a different symbol, then make sure that the "special messages" and "special emotes"
section will now use the new symbols. This means the examples offered in this ReadMe might differ from your situation.

Important;
If you want to change these values, here is a list to NOT change it to:

"/"
"\"
"$"

=========================================================================================
=======================================[ General ]=======================================
=========================================================================================

The general tab is the first module of this script, it allows you to add emotes (case sensitive) that will then be detected by the bot.
It will then output the emote back at the user, depending on the "mode" (explained below) you have chosen.

=======================================[1. Key Words ]===================================

Key words are the emotes/words that the bot will look for. These can be both words or emotes.

Important:
Leave a space between each emote/word to add another one.


=======================================[2. Mode ]===================================

The mode represents how the bot will output its message in chat. Down below we will discuss the modes:

+++++[First Emote]+++++

In this mode the bot will check the users message if any of the emotes are present from the "key words".
If there is, it will return a message containing the first emote he found.

Example:
Key words = Kappa Keepo
User writes: Hello streamer Keepo How are you doing Kappa
Bot output: Keepo

Here the bot detected the Keepo emote, which is in the "key words" and outputted it to chat.

+++++[All emotes once]++++++

In this mode the bot will check the users message if any of the emotes from the "key words".
If there is it will return all emotes it detected once.

Example:
Key words = Kappa Keepo
User writes: Keepo hype! Kappa Kappa
Bot output: Keepo Kappa

Here the bot found 2 emotes from the "key words" and outputted them both one time.

+++++[All emotes mirror]++++++

In this mode the bot will check the users message if any of the emotes from the "key words".
If there is it will return the exact amount of emotes used, from the "key words".

Example:
Key words = Kappa Keepo SeemsGood
User writes: Keepo hype! Kappa Kappa SeemsGood
Bot output: Keepo Kappa Kappa SeemsGood

Here the bot mirrored all the emotes that were in the key words list, and outputted them exactly as
they were send.

+++++[Randomized]++++++

Here the bot will randomly pick one of the other 3 modes and outputs that to the chat.




=======================================[3. Permission ]===================================

Here you can set the permission level for who can trigger the general emotes.




=======================================[4. Cooldown ]=====================================

Here you can place a cooldown on the general emotes module, in seconds.



=========================================================================================
=======================================[ Special emotes ]================================
=========================================================================================

In the UI you have a special button; "open special emotes file". This will open up a textfile for the special emotes.
(If the button doesn't work, try setting notepad as your default. Or Rightclick in the script tab --> open script folder --> Go to the scriptfolder --> click the folder "Lib"
The textfile should be named: "Special Emotes.txt"

Important note: If you change the textfile name, or place this file anywhere else on your computer, the script will not work.

In this textfile you can make new wordtriggers/greeting messages. A wordtrigger would be made as follows:

++++The Greetings wordtrigger:+++++





          ["Permission", "Greet", "Message"]





The above trigger will produce a standard greeting message. Replace the "Permission" with one of the Permission-modes described further below.
In the trigger above we're simply stating that if a person that has the required permission, speaks in chat. The bot will greet them once with the "Message"
You can also use a name in the "Permission" field if you want the greet-trigger only to work for one special user.

++++Special emote triggers+++++



Next we're going to look for actual Special command triggers. These would look something like this:



          ["Permission", "Mode", "Cooldown", "Emotes", "Message"]




Again we have a Permission module, we have a "Mode" module, and a cooldown Module. Cooldown is always in seconds (So for 1 minute cooldown, replace Cooldown with 60).
Substitute the "Permission" from the Permission block, Substitute "Mode" from the Mode block.


Here are some examples:

["SirPhilthyOwl", "Combo", "10", "Hello SirphilthyOwl", "Hello $user!"]
      |              |   |         |                   |
      |              |   |         |                   |
      |              |   |         |                    --------- The Message the bot will output   (More info in the Message block below)
      |              |   |         --------------------------- The Emotes the bot will be looking for    (More info in the Emote block below)
      |              |    ------------------------------------ The Cooldown (in seconds)
                      --------------------------------------- The "Mode"    (More info in the Mode block below)
      ------------------------------------------------------- The "Permission" In this case a special username.   (More info in the Permission Block below)

["Everyone", "Greet", "Hello $user!"]
      |       |          |
      |       |          |
      |       |          |
      |       |          |
      |       |          ------------------------------------ The Message (More info in the Message block)
      |         ----------------------------------------- The "Mode" In this case its a greet message (More info in the Mode block below)
      --------------------------------------------------- The "Permission" In this case "Everyone" (More info in the Permission block below)

Another command you can use is the following:

["Permission", "Onjoin", "number"]


This command lets you give currency to a certain group when they join. For instance:


["Everyone", "Onjoin", "500"]

This gives 500 channel currency to anyone who joins for the first time during stream, that has the permission "Everyone"
Check the "Permission block" for all Permission modes.


TLDR;

Only these combinations are possible:

["Permission", "Greet", "Message]                                  Specialized greet, on first message in chat
["Permission", "Greet", "Mode", "Emotes", "Message"]               specialized greet, when emote is triggered.
["Permission", "Mode", "Cooldown", "Emotes", "Message"]            Special emote word triggers
["Permission", "Onjoin", "number"]                                 This command is used to give channel currency to the "permission group". It only triggers once.


Important information about each parameter can be read below.

Also make sure you type the Permission correctly, and make sure the format is correct.
If an emote trigger is not working, make sure the format is correct.

If a command is not working you could check the "info" screen in the Script tab in Chatbot (Topright corner) There might be an error message
That lets you know which command is not working.





=======================================[1. Permission block ]===================================

Everyone                  Everyone will have access to this trigger
Regular                   A regular checks if the person has spoken within a certain timeframe
Subscriber                Subscribers will have access to this trigger
Moderator                 Moderators have access to this trigger
Editor                    Editors have access to this trigger
Caster                    Only the owner of the channel has access to the trigger.
UserName                  Replace this by the persons name that you want the trigger to work for.




=======================================[2. Mode block ]========================================

The mode in the special emotes module are different from the general module. They are described below:

The following Modes are usable:

Greet                          (Only works in Greetings format)
Combo                          (Combo)
Non-Combo                      (Non-Combo)
Non-Combo+                     (Non-Combo+)
Single                         (Single)


++++[Combo]++++


Combo mode means its looking for the special emotes as a combination. And if the bot finds them (in a row) it will output them in chat.

Example:
Special emotes  = Kappa Keepo Kappa
Special message = KappaPride
User writes: Hey streamer! Kappa Keepo Kappa
Bot output: KappaPride

Another example:
User writes: Hey streamer! Kappa How are you Keepo Kappa
Bot output:

The bot saw the combination of emotes in the first message, and outputted the special message.
In the second example, the emotes were not next to each other. Therefor the bot didn't output anything.


+++++[Non-combo]++++++

This mode is the opposite of the Combo mode. It detects emotes anywhere in the chatmessage.
It will look if the chatmessage has the correct amount of emotes in the message and if this is true, output the special message.

Example:
Special emotes  = Kappa Keepo Kappa
Special message = KappaPride
User writes: Hey streamer! Kappa How are you doing Keepo Kappa
Bot output: KappaPride

Another example:
User writes: Hey streamer! Kappa How are you doing Keepo
Bot output:

In the first example, all emotes were used from the special emotes so the bot outputted the message.
In the second example the message only had 1 "Kappa" so the bot did NOT output its special message.

The Non-Combo is different from the Non-Combo Plus (described below) because the Non-combo only looks
if the chatmessage has all the emotes required to output it's message.


+++++[Non-Combo Plus]++++++

Have you ever wanted to make a secret trigger message? With Non-Combo Plus you can.
Non-Combo Plus works almost the same way as Non-Combo does, as it looks if all the emotes are in the message.
But it will then also check if there aren't more of the keywords in the message.

This means that if you wanted a message to trigger when someone writes exactly 5x "Kappa"

Example:
Special emotes  = Kappa Kappa Kappa
Special message = KappaPride
User writes: Hey streamer! Kappa How are you doing Kappa Kappa
Bot output: KappaPride

Another example:
User writes: Hey streamer! Kappa How are you doing Kappa Kappa Kappa
Bot output:

In the first example, the user writes the exact amount of Kappa's needed to trigger the message.
The second example, the user uses 1 more Kappa in it's message. Therefor the message does not get send.

Important:
Non-Combo Plus, will only check the same emote field to see if there aren't more of the same emotes in the message.



+++++[Single]++++++

In this mode the bot will look for any of the special emotes and if 1 of them is in the chatMessage
it will output its special messages

Example:
Special emotes  = Kappa Keepo Kappa
Special message = KappaPride
User writes: Hey streamer! How are you doing Kappa
Bot output: KappaPride

Another example:
User writes: Hey streamer! How are you doing Keepo
Bot output: KappaPride

In both instances, the bot found an emote from the special emotes and outputted the message

=======================================[3. Special Emotes block ]========================================

In here you can insert your special emotes that the bot is going to look for.
You can use "|" to seperate different set of emotes for the bot to look for:

Example:
Mode = Combo
Special emotes  = Kappa Keepo Kappa|Keepo Kappa Keepo
Special message = KappaPride
User writes: Hey streamer! How are you doing Keepo Kappa Keepo
Bot output: KappaPride

Another example:
User writes: Hey streamer! How are you doing Kappa Keepo Kappa
Bot output: KappaPride

In both instances, the bot found the combination of emotes and will output the message.
Basically the "|" seperator allows you to let the bot output the same special message with different emote combinations.



=======================================[4. Special message block ]======================================

This is what the bot will output to chat once it has found the keywords needed.
But the special message has several output options. You can for instance let the bot read from a textfile instead.

Special parameters:

"|"                     The bot can output multiple random messages with the same emote combination
                        For instance if you put the "|" in the message, the bot will split the message up and pick randomly between one of them.
                        (This can be changed in the "Advanced settings. Read the Advanced settings paragraph first in this ReadMe")

"~"                     If you use this parameter, the bot will output its message in more parts in the chat window.
                        (This can be changed in the "Advanced settings. Read the Advanced settings paragraph first in this ReadMe")


$user                   You can put this in the message to get the persons name in the message, who triggered the message.

$file(path)             The bot can read from a textfile. Make sure the path is something like: "C:\Path\Path\Path\textfile.txt"
                        It will only read the first line of the textfile.

$sound(path, volume)    The bot can also trigger a sound effect. Make sure the path is something like "C:\Path\Path\Path\soundfile.mp3"
                        You can also specify a volume, if no volume is set it will default to 50

$currency(Mode, value)  This parameter can add/remove currency from users. the "Mode" would be add or remove, the value would be the amount it removes.

$currencyname           this parameter will retrieve the currencyname of the channel.

Here is an examples:

Example:
Mode = Combo
Special emotes  = Kappa Keepo Kappa|Keepo Kappa Keepo
Special message = KappaPride|I am a bot~I do bot things
User writes: Hey streamer! How are you doing Keepo Kappa Keepo
Bot output: I am a bot
            I do bot things

Here the bot found the special emote combination and outputted the randomly chosen special message and outputted it in 2 seperate lines.

Important note: You CAN'T trigger $file in a textfile. This is intended, so the bot doesn't loop through 2 textfiles infinitely.
You can however use the "~", "$sound" and "|" parameter in the textfiles.



=======================================[5. Cooldown block ]=====================================

Just like in the general module here you can specify a cooldown for this special emote module.
The cooldown must be entered in seconds. Do note that every special emote module has its own cooldown.


=========================================================================================
=======================================[ Welcome module ]================================
=========================================================================================

The welcome module is a special welcome wordtrigger. It will display the welcome message in chat when the user first speaks.

Users are able to add their own welcome message with the commands you set in the UI menu (these can be changed)

Default they are set to "!greet" and then the modifier of the message. In this case "add" "edit" and "delete"

A user can use

!greet add <message>			 			to add a new welcome message.
!greet edit <welcome message number> <new message>		to edit an existing message.
!greet delete <welcome message number>				to delete an existing message.
!greet list							to show the greet list of that user
!greet								This will bring up the generic "greet menu" in chat.


You can also enter words in a blacklist. If any of the words is in the message they try to add/edit, it will not be accepted.



Important:

If your bot is mod in your channel, make sure to blacklist mod commands. Otherwise users can set the "mod commands" as their welcome message.
And time other people out. Simply blacklisting the "/" sign or "timeout" will prevent this.

You can open the textfile manually and edit their welcome commands (shortcut to textfile in the UI).





=========================================================================================
=======================================[ Test sound ]====================================
=========================================================================================


Here you can test a file path to check on which volume you want it to play. Afterwards you can update your special emotes module
with the correct desired volume. You will still have to change this manually to your desired volume.

To use the test sound, input a path and a desired volume. Then hit save and press the "Test Sound" button.
Make sure everytime you make a change, you press the save button and reload the script.
