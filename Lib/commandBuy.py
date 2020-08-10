#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
#---------------------------------------
# Libraries and references
#---------------------------------------




import os
import re
import codecs

ScriptName = "Kappa Anywhere"

specialEmoteList = os.path.join(os.path.dirname(__file__), "Special Emotes.txt")

def mainCommand(Parent, data, MySet):

    if data.GetParam(1).lower() == MySet.addGreet.lower():
        commandAdd(Parent, data, MySet)

    elif data.GetParam(1).lower() == MySet.editGreet.lower():
        commandEdit(Parent, data, MySet)

    elif data.GetParam(1).lower() == MySet.deleteGreet.lower():
        commandDelete(Parent, data, MySet)

    elif data.GetParam(1).lower() == MySet.listGreet.lower():
        commandList(Parent, data, MySet)

    else:
        Message = "{} Welcome to the greet menu: use {} {}/{}/{} to change your welcome messages. Alternatively you could use {} {} to view your welcome messages.".format(data.UserName, MySet.prefixCommand, MySet.addGreet, MySet.editGreet, MySet.deleteGreet, MySet.prefixCommand, MySet.listGreet)
        Parent.SendStreamMessage(Message)
        return

def commandList(Parent, data, MySet):
    welcomeString = textFileRead(Parent, data.User, "seek", "placeholder")
    if welcomeString:
        welcomeString = welcomeString.split(MySet.breakSeperator)
        Message = "{} your welcome messages are: {}".format(data.UserName, welcomeString)
        Parent.SendStreamMessage(Message)
    else:
        Message = "{} You don't have any welcome messages, use {} {} <message> to add a new welcome message!".format(data.User, MySet.prefixCommand, MySet.addGreet)
        Parent.SendStreamMessage(Message)
    return

def commandAdd(Parent, data, MySet):
    myGreet = textFileRead(Parent, data.User, "seek", "placeholder")
    if not myGreet:
        myGreet = ""
    words = data.Message.split(MySet.addGreet)
    if len(myGreet.split(MySet.breakSeperator)) > 1 and not permissionParse(Parent, data.User):
        Message = "Sorry {}, only subscribers get access to multiple welcome messages. Use {} to edit your welcome message instead".format(data.UserName, MySet.editGreet)
        Parent.SendStreamMessage(Message)
        return
    if len(myGreet.split(MySet.breakSeperator)) == 5:
        Message = "Sorry {} you've reached up to a maximum of 5 welcome messages".format(data.UserName)
        Parent.SendStreamMessage(Message)
        return
    if BlackListCheck(Parent, data, MySet, words[1].strip()) == True:
        return

    if pointsCheck(Parent, data, MySet, MySet.addCurrency, "add"):
        if not data.GetParam(2):
            Message = "{} you did not add a message, the correct prefix is: {} {} <Message>".format(data.UserName, MySet.prefixCommand, MySet.addGreet)
            Parent.SendStreamMessage(Message)
            return
        message = "{}|{}".format(myGreet, words[1].strip())
        textFileRead(Parent, data.User, "add", message)
        Message = "{} your welcome message: '{}' has been succesfully added!".format(data.UserName, words[1].strip())
        Parent.SendStreamMessage(Message)
        return True
    return

def commandEdit(Parent, data, MySet):

    if not data.GetParam(2).split() or data.GetParam(2).isdigit() == False or not data.GetParam(3).split():
        Message = "{} the proper syntax to use is; {} {} <number> <new message> that you want to edit. (Without <>)".format(data.UserName, MySet.prefixCommand, MySet.editGreet)
        Parent.SendStreamMessage(Message)
        return

    words = data.Message.split(data.GetParam(2))

    if BlackListCheck(Parent, data, MySet, words[1].strip()) == True:
        return

    myGreet = textFileRead(Parent, data.User, "seek", words[1].strip())

    if not myGreet:
        Message = "Sorry {} but you don't have any welcome messages to edit. Try {} to add a welcome message instead".format(MySet.addGreet)
        Parent.SendStreamMessage(Message)
        return

    myGreet = myGreet.split(MySet.breakSeperator)

    if int(data.GetParam(2)) > len(myGreet):
        Message = "You don't have that many welcome messages {}! You have a total of {} welcome messages!".format(data.UserName, len(myGreet))
        Parent.SendStreamMessage(Message)
        return

    if int(data.GetParam(2)) <= len(myGreet) and pointsCheck(Parent, data, MySet, MySet.editCurrency, "edit"):
        oldString = myGreet[int(data.GetParam(2)) - 1]
        myGreet[int(data.GetParam(2)) - 1] = words[1].strip()
        message = MySet.breakSeperator.join(myGreet)
        textFileRead(Parent, data.User, "edit", message)
        Message = "{} your welcome message has been succesfully changed from: {} TO {} ".format(data.UserName, oldString, words[1])
        Parent.SendStreamMessage(Message)
        return True
    return False

def commandDelete(Parent, data, MySet):

    if data.GetParam(2) == "all":
        textFileRead(Parent, data.User, "delete", "placeholder")
        Message = "{} all of your welcome messages have been deleted!".format(data.User)
        Parent.SendStreamMessage(Message)
        return

    if not data.GetParam(2).split() or data.GetParam(2).isdigit() == False:
        Message = "{} the proper syntax to use is; {} {} <number>/<all> that you want to delete. (Without <>)".format(data.UserName, MySet.prefixCommand, MySet.deleteGreet)
        Parent.SendStreamMessage(Message)
        return

    words = data.Message.split(data.GetParam(2))
    myGreet = textFileRead(Parent, data.User, "seek", words[1].strip())

    if not myGreet:
        Message = "Sorry {} but you don't have any welcome messages to delete.".format(data.UserName)
        Parent.SendStreamMessage(Message)
        return

    myGreet = myGreet.split(MySet.breakSeperator)

    if int(data.GetParam(2)) <= len(myGreet) and myGreet and pointsCheck(Parent, data, MySet, MySet.deleteCurrency, "delete"):
        oldString = myGreet[int(data.GetParam(2)) - 1]
        myGreet.pop(int(data.GetParam(2)) - 1)
        message = MySet.breakSeperator.join(myGreet)
        textFileRead(Parent, data.User, "edit", message)
        Message = "{} your welcome message: {} has been succesfully deleted".format(data.UserName, oldString)
        Parent.SendStreamMessage(Message)
        return True

    if int(data.GetParam(2)) > len(myGreet):
        Message = "You don't have that many welcome messages {}! You have a total of {} welcome messages!".format(data.UserName, len(myGreet))
        Parent.SendStreamMessage(Message)
        return
    return

def textFileRead(Parent, name, mode, message):
    Item = []
    found = False
    with codecs.open(specialEmoteList, encoding="utf-8-sig", mode="r") as file:
        for line in file:
            if name in line and "Greet" in line:
                Regex = re.search(r'\[\s*"([^"]*)",\s?"?([^"]*)",\s?"?([^"]*)"\]', line)
                if mode == "seek":
                    changeLine = Regex.group(3)
                    file.close()
                    return changeLine
                if mode == "add" or mode == "edit":
                    changeLine = '["{}", "{}", "{}"]\n'.format(Regex.group(1), Regex.group(2), message)
                    Item.append(changeLine)
                    found = True
                    continue
                if mode == "delete":
                    continue
            Item.append(line)

    if mode == "add" and not found:
        changeLines = '["{}", "Greet", "{}"]'.format(name, message)
        Item = [changeLines] + Item
    if mode == "edit" and not found:
        file.close()
        return False

    textFileWrite(Item)
    file.close()
    return

def textFileWrite(Item):
    with codecs.open(specialEmoteList, encoding="utf-8-sig", mode="w") as file:
        for line in Item:
            file.write(line)
    file.close()
    return

def BlackListCheck(Parent, data, MySet, message):
    for word in MySet.blacklistedWords.split():
        if word in message:
            Message = "Sorry {} but your welcome message could not be added due to blacklisted words.".format(data.UserName)
            Parent.SendStreamMessage(Message)
            return True
    return False

def permissionParse(Parent, name):
    permissions = ["Subscriber", "VIP+", "Moderator", "Caster"]
    for item in permissions:
        if Parent.HasPermission(name, item, ""):
            return True
    return False

def pointsCheck(Parent, data, MySet, amount, mode):
    if Parent.RemovePoints(data.User, data.UserName, amount):
        return True
    else:
        Message = "Sorry {} You don't have enough points to {} your welcome message!".format(data.UserName, mode)
        return False
