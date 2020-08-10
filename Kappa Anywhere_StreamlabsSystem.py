#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import re
import ast
import time
import winsound
import sys
import ctypes

import random
random = random.WichmannHill()

sys.path.append(os.path.join(os.path.dirname(__file__), "Lib"))
import commandBuy

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Kappa Anywhere"
Website = "https://www.twitch.tv/sirphilthyowl"
Creator = "SirPhilthyOwl"
Version = "1.0.7"
Description = "Returns Kappa from anywhere in a sentence and more..."
#---------------------------------------
# Versions
#---------------------------------------


#---------------------------------------
# Variables
#---------------------------------------
specialEmoteList = "Services\\Scripts\\Kappa Anywhere\\Lib\\Special Emotes.txt"
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
ReadList = os.path.join(os.path.dirname(__file__), "ReadMe.txt")
greetedUsers = []
EmotesFile = []
currencyPermission = []
generalCooldown = 0
permissionList = ["Everyone", "Regular", "Subscriber", "VIP+", "Moderator", "Editor", "Caster"]
modeList = ["First Emote", "All emotes, once", "All emotes, mirror"]
MB_YES = 6
MessageBox = ctypes.windll.user32.MessageBoxW

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no custom settings file is found
            self.onlyLive = True
            self.generalEmotes = True
            self.specialEmotes = True
            self.Blacklist = ""
            self.Words = ""
            self.Mode = "Single"
            self.Words = "Kappa"
            self.Permission = ""
            self.Cooldown = 0
            self.Permission = "Everyone"
            self.prefixCommand = "!greet"
            self.addGreet = "add"
            self.editGreet = "edit"
            self.deleteGreet = "delete"
            self.addCurrency = 0
            self.editCurrency = 0
            self.deleteCurrency = 0
            self.listGreet = "list"
            self.blacklistedWords = "[ ] /"
            self.breakSeperator = "|"
            self.lineSeperator = "~"
            self.testVolume = 50
            self.testPath = ""

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        try:
            """Save settings to files (json and js)"""
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
                json.dump(self.__dict__, f, encoding='utf-8', ensure_ascii=False)
            with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

#---------------------------------------
# Settings functions
#---------------------------------------

def ReloadSettings(jsondata):
    """Reload settings on Save"""
    # Reload saved settings
    MySet.ReloadSettings(jsondata)
    # End of ReloadSettings

def SaveSettings(self, settingsFile):
    """Save settings to files (json and js)"""
    try:
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8', ensure_ascii=False)
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
    except ValueError:
        Parent.Log(ScriptName, "Failed to save settings to file.")
    return

#---------------------------------------
# System functions
#---------------------------------------

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)
    # Load in saved settings
    MySet.SaveSettings(settingsFile)
    initLists()
    # End of Init
    return

def Execute(data):
    """Required Execute data function"""
    actualTime = time.time()

    if data.IsChatMessage() and not data.UserName.lower() in MySet.Blacklist.lower().split():

        if specEmoteMessageParse(data):
            return
        if data.GetParam(0).lower() == MySet.prefixCommand.lower() and MySet.welcomeModule:
            commandBuy.mainCommand(Parent, data, MySet)
            return
        else:
            words = data.Message
            if MySet.generalEmotes and word_count(words) and Parent.HasPermission(data.UserName,
                                            MySet.Permission, "") and generalCooldownCheck(actualTime, getattr(MySet, "Cooldown")):
                generalEmotes(words, data.UserName)
                Cooldown = actualTime + int(getattr(MySet, "Cooldown"))
    return


#---------------------------------------
# [Required] Tick handling
#---------------------------------------

def Tick():
    """Required tick function"""
    return

#---------------------------------------
# [Required] Emote Parsing
#---------------------------------------

def initLists():
    global EmotesFile
    global currencyPermission
    with codecs.open(specialEmoteList, encoding="utf-8-sig", mode="r") as file:
        Item = [line.strip() for line in file]
        for line in Item:
            Onjoin = re.search(r'\[\s*"([^"]*)",\s?"?([^"]*)",\s*"?(\d+)"?"\]', line)
            Greet = re.search(r'\[\s*"([^"]*)",\s?"?([^"]*)",\s?"?([^"]*)"\]', line)
            specialEmote = re.search(r'\[\s*"([^"]*)",\s?"?([^"]*)",\s*"?(\d+)"?,\s?"?([^"]*)",\s?"?([^"]*)"\]', line)
            if Onjoin:
                if Onjoin.group(2) == "Onjoin":
                    if Onjoin.group(1) in permissionList:
                        for value in permissionList:
                            if Onjoin.group(1) == value:
                                permission = [value, Onjoin.group(3)]
                                currencyPermission.append(permission)
                        continue
            if Greet:
                if Greet.group(2) == "Greet":
                    newDic = {"Greet": Greet.group(1), "Message": Greet.group(3)}
                    EmotesFile.append(newDic)
            if specialEmote:
                newDic = {"Permission": specialEmote.group(1), "Mode": specialEmote.group(2), "Cooldown": specialEmote.group(3), "Emotes": specialEmote.group(4), "Message": specialEmote.group(5), "cooldownTime": 0}
                EmotesFile.append(newDic)
    Parent.Log(ScriptName, str(currencyPermission))
    file.close()
    return

def specEmoteMessageParse(data):
    global EmotesFile
    index = 0
    for item in EmotesFile:
        for word in data.Message.split():
            if "Greet" in EmotesFile[index] and not data.User in greetedUsers:
                if greetMode(data, EmotesFile[index]):
                    currencyParse(data)
                    return True
            if "Emotes" in EmotesFile[index] and not "Greet" in EmotesFile[index] and specEmoteParse(data, EmotesFile[index]):
                if "Cooldown" in EmotesFile[index]:
                    if not EmotesFile[index]["Cooldown"] == "0":
                        try:
                            EmotesFile[index]["cooldownTime"] = time.time() + int(EmotesFile[index]["Cooldown"])
                        except ValueError:
                            errorLog = "[Error] Could not set cooldown for Special Emote [Emotes: {}][Message: {}][Line in text: {}]".format(EmotesFile[index]["Emotes"], emotesFile[index]["Message"], (index + 1))
                            Parent.Log(ScriptName, errorLog)
                        return True
        index += 1
    return False

def greetMode(data, emoteDic):
    if not emoteDic["Greet"] in permissionList:
        if not emoteDic["Greet"].lower() == data.User:
            return False
    if emoteDic["Greet"] in permissionList and not Parent.HasPermission(data.User, emoteDic["Greet"], ""):
        return False
    streamMessageParse(emoteDic["Message"], data.UserName)
    return True

def specEmoteParse(data, emoteDic):
    chatMessage = data.Message
    Emote = emoteDic["Emotes"]
    Message = emoteDic["Message"]
    Permission = emoteDic["Permission"]
    cooldownTime = emoteDic["cooldownTime"]
    Combo = emoteDic["Mode"].lower()

    if not time.time() >= cooldownTime:
        return False

    if Parent.HasPermission(data.User, Permission, ""):

        if Combo == "combo" and specEmoteCombo(Emote, Message, data.UserName, chatMessage):
            return True

        # For some reason, if this function isn't called from a variable, it doesn't work. Just leave it.
        mybool = specEmoteNonCombo(Emote, Message, data.UserName, chatMessage, Combo)
        if Combo == "non-combo" or Combo == "non-combo+" and mybool:
            return True

        if Combo == "single" and specEmoteSingle(Emote, Message, data.UserName, chatMessage):
            return True
    return False

def word_count(words):
    for word in words:
        if word in MySet.Words:
            return True
    return

#---------------------------------------
# [Required] Special & General emote functions.
#---------------------------------------
#
def specEmoteCombo(Emote, Message, name, words):
    specEmotes = Emote.split(MySet.breakSeperator)
    for item in specEmotes:
        Regex_Match = re.findall(r'\b' + item + r'\b', words)
        if Regex_Match:
            streamMessageParse(Message, name)
            return True
    return False

def specEmoteNonCombo(Emote, Message, name, words, Combo):
    specEmote = Emote.split(MySet.breakSeperator)
    controlList = []
    for item in specEmote:
        for word in item.split():
            word = word.strip()
            matchMessage = re.findall(r'\b' + word + r'\b', words)
            matchEmoteList = re.findall(r'\b' + word + r'\b', item)
            if Combo == "non-combo" and len(matchMessage) >= len(matchEmoteList):
                controlList.append("True")
            elif Combo == "non-combo+" and len(matchMessage) == len(matchEmoteList):
                controlList.append("True")
            else:
                del controlList[:]
                continue

        if len(controlList) == len(item.split()):
            streamMessageParse(Message, name)
            return True
        else:
            del controlList[:]
            continue
    return False


def specEmoteSingle(Emote, Message, name, words):
        for word in Emote.split():
            Regex_Match = re.search(r'\b' + word + r'\b', words)
            if Regex_Match:
                streamMessageParse(Message, name)
                return True
        return False


def generalEmotes(words, name):
    emoteSet = set()
    emoteList = []
    if MySet.Mode == "Randomized":
        randomChoice = random.choice(modeList)
    else:
        randomChoice = False

    for word in MySet.Words.split():
        Regex_Match = re.search(r'\b' + word + r'\b', words)

        if Regex_Match:

            if MySet.Mode == "First emote" or randomChoice == "First emote":
                Message = word
                sendMessageGeneral(Message)
                return
            emoteList.append(word)
            emoteSet.add(word)

    if MySet.Mode == "All emotes, once" or randomChoice == "All emotes, once":
        Message = ' '.join(emoteSet)
        sendMessageGeneral(Message)
        return

    if MySet.Mode == "All emotes, mirror" or randomChoice == "All emotes, mirror":
        Message = ' '.join(emoteList)
        sendMessageGeneral(Message)
        return
    return



#---------------------------------------
# [Required] Emote cooldown functions
#---------------------------------------
#Checks for cooldowns and sets cooldowns.

def generalCooldownCheck(actualTime, actualCooldown):
    if actualTime >= generalCooldown or not actualCooldown.strip():
        return True
    else:
        return False

#---------------------------------------
# [Required] Message Parsing/formatting
#---------------------------------------

def currencyParse(data):
    global greetedUsers
    if len(currencyPermission) >= 1:
        for index, value in enumerate(currencyPermission):
            try:
                if Parent.HasPermission(data.User, currencyPermission[index][0], "") and Parent.AddPoints(data.User, data.UserName, int(currencyPermission[index][1])):
                    Message = "Gave {} points to {} because his rank was {}".format(currencyPermission[index][1], data.UserName, currencyPermission[index][0])
                    Parent.Log(ScriptName, Message)
            except:
                Message = "Onjoin parameter for rank {} is not written in the right syntax.".format(currencyPermission[index][0])
                Parent.Log(ScriptName, Message)
    greetedUsers.append(data.User)
    return


#Functions for both $file and $sound parsing in messages.

def streamMessageParse(messageList, user):
    if "$file" in messageList:
        messageList = fileParse(messageList)

    messageList = messageList.split(MySet.breakSeperator)
    messageList = random.choice(messageList)

    if "$sound" in messageList:
        messageList = soundParse(messageList)

    if "$currency" in messageList:
        messageList = messageCurrencyParse(messageList, user)
    messageList = messageList.replace("$user", user)
    sendMessage(messageList)
    return


def fileParse(messageList):
    linkPath = re.findall('(?<=\().*?(?=\))', messageList)
    for index, value in enumerate(linkPath):
        if value.endswith(".txt"):
            messageList = re.sub('\$file[^)]+\)', fileDetection(linkPath[index]), messageList, 1)
        else:
            messageList = re.sub('\$file[^)]+\)', "[Error: $file name not found]", messageList, 1)
    return messageList

def soundParse(messageList):
    linkPath = re.findall('(?<=\().*?(?=\))', messageList)
    for index, value in enumerate(linkPath):
        slicePath = value
        if slicePath.split(",")[0].endswith((".mp3", ".wav")):
            messageList = re.sub('\$sound[^)]+\)', soundDetection(linkPath[index]), messageList, 1)
        else:
            messageList = re.sub('\$sound[^)]+\)', "[Error: $sound name not found]", messageList, 1)
    return messageList

def messageCurrencyParse(messageList, user):
    currencyPath = re.findall('(?<=\$currency\().*?(?=\))', messageList)
    bool = False
    for index, value in enumerate(currencyPath):
        if len(currencyPath[index].split(",")) == 2 and currencyPath[index].split(",")[1].isdigit():
            if currencyPath[index].split(",")[0].lower() == "add":
                Parent.AddPoints(user.lower(), user, int(currencyPath[index].split(",")[1]))
                bool = True
            if currencyPath[index].split(",")[0].lower() == "remove":
                Parent.RemovePoints(user.lower(), user, int(currencyPath[index].split(",")[1]))
                bool = True
            else:
                Message = "Failed to parse currency from {}. Check $currency parameters".format(user)
                Parent.Log(ScriptName, Message)
        if bool:
            messageList = re.sub('\$currency[^)]+\)', "", messageList, 1)
        else:
            messageList = re.sub('\$currency[^)]+\)', "[Error: $currency parameters wrong]", messageList, 1)
    messageList = messageList.replace("$currencyname", Parent.GetCurrencyName())
    return messageList


#---------------------------------------
# [Required] file/sound detection
#---------------------------------------
#After the file and sound parse, these functions will check if the pathnames are files

def fileDetection(file):
    if os.path.isfile(file):
        #open file, and put first line into variable
        f = codecs.open(file, encoding='utf-8-sig', mode='r')
        newLine = f.readline()
        f.close()
        return newLine
    else:
        newLine = "[Error: $file path not found]"
        return newLine

def soundDetection(file):
    file = file.split(",")
    actualFile = file[0]
    if os.path.isfile(actualFile):
        if len(file) < 2:
            volume = 50
        else:
            volume = file[1]
        playSound(actualFile, volume)
        newLine = ""
        return newLine
    else:
        newLine = "[Error: $sound path not found]"
        return newLine

#---------------------------------------
# [Required] Sound play function
#---------------------------------------
#Seperate function so UI "Test Sound" can call this function aswell.

def playSound(file, volume):
    try:
        Parent.PlaySound(file, int(volume)*0.01)
    except ValueError:
        volume = 50
        Parent.PlaySound(file, int(volume)*0.01)
    return

#---------------------------------------
# [Required] Message handling
#---------------------------------------

def sendMessage(messageList):
    for item in messageList.split(MySet.lineSeperator):
        Parent.SendStreamMessage(item)
    return

def sendMessageGeneral(Message):
    Parent.SendStreamMessage(Message)
    return

#---------------------------------------
# [Required] UI functions
#---------------------------------------

def testSound():
    file = getattr(MySet, "testPath")
    volume = MySet.testVolume
    if os.path.isfile(file) == False and not file.lower().endswith(('.mp3', '.wav')):
        winsound.MessageBeep()
        returnValue = MessageBox(0, u"Couldn't find the specified soundfile."
                                "\r\nMake sure the path is correct", u"File not found", 4)
    playSound(file, volume)

def openreadme():
    os.startfile(ReadList)

def openSpecialEmotes():
    os.startfile(specialEmoteList)

def reloadSpecialEmotes():
    initLists()
