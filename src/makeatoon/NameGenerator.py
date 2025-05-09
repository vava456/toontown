from toontown.toonbase.ToontownModules import *
import random
import string
import copy
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import os
from direct.showbase import AppRunnerGlobal
from direct.directnotify import DirectNotifyGlobal

class NameGenerator:

    # A TextNode we will use to measure the lengths of names
    text = TextNode('text')
    text.setFont(ToontownGlobals.getInterfaceFont())

    notify = DirectNotifyGlobal.directNotify.newCategory("NameGenerator")

    boyTitles = []
    girlTitles = []
    neutralTitles = []
    boyFirsts = []
    girlFirsts = []
    neutralFirsts = []
    capPrefixes = []
    lastPrefixes = []
    lastSuffixes = []

    def __init__(self):
        self.generateLists()
        return

    def generateLists(self):
        """ This method looks in a text file specified in the localizer and loads
            in all the names into the 8 lists as well as populating self.nameDictionary
            which has uniqueIDs mapped to a tuple of category and name
            """
        self.boyTitles = []
        self.girlTitles = []
        self.neutralTitles = []
        self.boyFirsts = []
        self.girlFirsts = []
        self.neutralFirsts = []
        self.capPrefixes = []
        self.lastPrefixes = []
        self.lastSuffixes = []
        self.nameDictionary = {}

        # Look for the name master file and read it in.
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            # In the web-publish runtime, it will always be here:
            searchPath.appendDirectory(Filename.expandFrom('$TT_3_ROOT/phase_3/etc'))
        else:
            # In other environments, including the dev environment, look here:
            searchPath.appendDirectory(Filename('phase_3/etc'))
            base = os.path.expandvars('$TOONTOWN') or './toontown'
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars(base+'/src/configfiles')))
            # RobotToonManager needs to look for file in current directory
            searchPath.appendDirectory(Filename('.'))

        filename = Filename(TTLocalizer.NameShopNameMaster)
        found = vfs.resolveFilename(filename, searchPath)

        if not found:
            self.notify.error("NameGenerator: Error opening name list text file '%s.'" % TTLocalizer.NameShopNameMaster)

        input = StreamReader(vfs.openReadFile(filename, 1), 1)

        currentLine = input.readlineStr().replace("\r", "")
        while currentLine:
            if currentLine.lstrip()[0:1] != '#':
                a1 = currentLine.find('*')
                a2 = currentLine.find('*', a1+1)
                self.nameDictionary[int(currentLine[0:a1])]=(int(currentLine[a1+1:a2]),
                                                             currentLine[a2+1:len(currentLine)-1])
            currentLine = input.readlineStr().replace("\r", "")

        masterList = [self.boyTitles, self.girlTitles, self.neutralTitles,
                      self.boyFirsts, self.girlFirsts, self.neutralFirsts,
                      self.capPrefixes, self.lastPrefixes, self.lastSuffixes]
        for tu in list(self.nameDictionary.values()):
            masterList[tu[0]].append(tu[1])
        return 1

    def _getNameParts(self, cat2part):
        # returns list of dict of string->index, one dict per name part
        nameParts = [{}, {}, {}, {}]
        # cat2part is mapping of NameMasterEnglish.txt category -> namePart index
        for id, tpl in list(self.nameDictionary.items()):
            cat, str = tpl
            if cat in cat2part:
                nameParts[cat2part[cat]][str] = id
        return nameParts

    def getMaleNameParts(self):
        return self._getNameParts({0: 0,
                                   2: 0,
                                   3: 1,
                                   5: 1,
                                   6: 2,
                                   7: 2,
                                   8: 3,
                                   })

    def getFemaleNameParts(self):
        return self._getNameParts({1: 0,
                                   2: 0,
                                   4: 1,
                                   5: 1,
                                   6: 2,
                                   7: 2,
                                   8: 3,
                                   })

    def getLastNamePrefixesCapped(self):
        return self.capPrefixes

    def returnUniqueID(self, name, listnumber):
        """ This is a helper function which accepts a name string, and a listnumber of
            type 0 = title, 1 = firstname, 2 = prefix, 3 = suffix
            It then makes a list of search tuples newtu and searches nameDictionary.
            If successful it returns the uniqueID, if not then -1
            """
        newtu = [(),(),()]
        if listnumber == 0:
            # Looking for a title
            newtu[0] = (0, name)
            newtu[1] = (1, name)
            newtu[2] = (2, name)
        elif listnumber == 1:
            # Looking for a first name
            newtu[0] = (3, name)
            newtu[1] = (4, name)
            newtu[2] = (5, name)
        elif listnumber == 2:
            # Looking for a prefix
            newtu[0] = (6, name)
            newtu[1] = (7, name)
        else:
            newtu[0] = (8, name)
        for tu in list(self.nameDictionary.items()):
            for g in newtu:
                if tu[1] == g:
                    return tu[0]
        return -1

    def findWidestInList(self, text, nameList):
        maxWidth = 0
        maxName = ""
        for name in nameList:
            width = text.calcWidth(name)
            if width > maxWidth:
                maxWidth = text.calcWidth(name)
                maxName = name
        print(maxName + " " + str(maxWidth))
        return maxName

    def findWidestName(self):
        longestBoyTitle = self.findWidestInList(self.text,
                                                self.boyTitles +
                                                self.neutralTitles)
        longestGirlTitle = self.findWidestInList(self.text,
                                                 self.girlTitles +
                                                 self.neutralTitles)
        longestBoyFirst = self.findWidestInList(self.text,
                                                self.boyFirsts +
                                                self.neutralFirsts)
        longestGirlFirst = self.findWidestInList(self.text,
                                                self.girlFirsts +
                                                self.neutralFirsts)
        longestLastPrefix = self.findWidestInList(self.text,
                                             self.lastPrefixes)
        longestLastSuffix = self.findWidestInList(self.text,
                                             self.lastSuffixes)

        longestBoyFront = self.findWidestInList(self.text,
                                                [longestBoyTitle,
                                                 longestBoyFirst])

        longestGirlFront = self.findWidestInList(self.text,
                                                 [longestGirlTitle,
                                                  longestGirlFirst])

        longestBoyName = (longestBoyTitle + " " + longestBoyFirst + " " +
                          longestLastPrefix + longestLastSuffix)
        longestGirlName = (longestGirlTitle + " " + longestGirlFirst + " " +
                           longestLastPrefix + longestLastSuffix)
        longestName = self.findWidestInList(self.text,
                                            [longestBoyName, longestGirlName])
        return longestName

    def findWidestTitleFirst(self):
        longestBoyTitle = self.findWidestInList(self.text,
                                                self.boyTitles +
                                                self.neutralTitles)
        longestGirlTitle = self.findWidestInList(self.text,
                                                 self.girlTitles +
                                                 self.neutralTitles)
        longestBoyFirst = self.findWidestInList(self.text,
                                                self.boyFirsts +
                                                self.neutralFirsts)
        longestGirlFirst = self.findWidestInList(self.text,
                                                self.girlFirsts +
                                                self.neutralFirsts)
        longestBoyName = (longestBoyTitle + " " + longestBoyFirst)
        longestGirlName = (longestGirlTitle + " " + longestGirlFirst)


        longestName = self.findWidestInList(self.text,
                                            [longestBoyName, longestGirlName])

    def findWidestTitle(self):
        widestTitle = self.findWidestInList(self.text,
                                            self.neutralTitles +
                                            self.boyTitles +
                                            self.girlTitles)
        return widestTitle

    def findWidestFirstName(self):
        widestFirst = self.findWidestInList(self.text,
                                            self.neutralFirsts +
                                            self.boyFirsts +
                                            self.girlFirsts)
        return widestFirst

    def findWidestLastName(self):
        longestLastPrefix = self.findWidestInList(self.text,
                                             self.lastPrefixes)
        longestLastSuffix = self.findWidestInList(self.text,
                                             self.lastSuffixes)
        longestLastName = longestLastPrefix + longestLastSuffix
        return longestLastName

    def findWidestNameWord(self):
        widestWord = self.findWidestInList(self.text,
                                           [self.findWidestTitle(),
                                            self.findWidestFirstName(),
                                            self.findWidestLastName()])
        return widestWord

    def findWidestNameWidth(self):
        name = self.findWidestName()
        return self.text.calcWidth(name)

    def printWidestName(self):
        name = self.findWidestName()
        width = self.text.calcWidth(name)
        widthStr = str(width)
        print(("The widest name is: " + name + " (" +
                widthStr + " units)"))

    def printWidestLastName(self):
        name = self.findWidestLastName()
        width = self.text.calcWidth(name)
        widthStr = str(width)
        print(("The widest last name is: " + name + " (" +
                widthStr + " units)"))

    def randomName(self, boy=0, girl=0):
        """ This method is outdated for current uses in Toontown, but good for
            general debugging.  You probably want to use randomNameMoreinfo
            """
        if boy and girl:
            self.error("A name can't be both boy and girl!")

        if (not boy) and (not girl):
            # Randomly pick the name sex
            boy = random.choice([0, 1])
            girl = not boy

        # Five types of name combos
        uberFlag = random.choice(["title-first", "title-last",
                                    "first", "last", "first-last", "title-first-last"])
        titleFlag = 0
        if ((uberFlag == "title-first") or
            (uberFlag == "title-last") or
            (uberFlag == "title-first-last")):
            titleFlag = 1

        firstFlag = 0
        if ((uberFlag == "title-first") or
            (uberFlag == "first") or
            (uberFlag == "first-last") or
            (uberFlag == "title-first-last")):
            firstFlag = 1

        lastFlag = 0
        if ((uberFlag == "title-last") or
            (uberFlag == "last") or
            (uberFlag == "first-last") or
            (uberFlag == "title-first-last")
            ):
            lastFlag = 1

        retString = ""

        if titleFlag:
            # Shallow copy, since we will be altering the list
            titleList = self.neutralTitles[:]
            if boy:
                titleList += self.boyTitles
            elif girl:
                titleList += self.girlTitles
            else:
                self.error("Must be boy or girl.")

            # Put a space because there will surely be another name.
            retString += random.choice(titleList) + " "

        if firstFlag:
            # Shallow copy, since we will be altering the list
            firstList = self.neutralFirsts[:]
            if boy:
                firstList += self.boyFirsts
            elif girl:
                firstList += self.girlFirsts
            else:
                self.error("Must be boy or girl.")

            retString += random.choice(firstList)
            # Put a space if there is going to be a last name.
            if lastFlag:
                retString += " "

        if lastFlag:
            lastPrefix = random.choice(self.lastPrefixes)
            lastSuffix = random.choice(self.lastSuffixes)
            if lastPrefix in self.capPrefixes:
                lastSuffix = lastSuffix.capitalize()
            retString += lastPrefix + lastSuffix

        return retString

    def randomNameMoreinfo(self, boy=0, girl=0):
        """This is just like randomName only it returns a list where the first three
           values are titleFlag, firstFlag, and lastFlag and the next four values are
           the title, firstname, and lastname (if applicable, '' if not)
           """

        if boy and girl:
            self.error("A name can't be both boy and girl!")

        if (not boy) and (not girl):
            # Randomly pick the name sex
            boy = random.choice([0, 1])
            girl = not boy

        # Five types of name combos
        uberFlag = random.choice(["title-first", "title-last",
                                    "first", "last", "first-last", "title-first-last"])


        titleFlag = 0
        if ((uberFlag == "title-first") or
            (uberFlag == "title-last") or
            (uberFlag == "title-first-last")):
            titleFlag = 1

        firstFlag = 0
        if ((uberFlag == "title-first") or
            (uberFlag == "first") or
            (uberFlag == "first-last") or
            (uberFlag == "title-first-last")):
            firstFlag = 1

        lastFlag = 0
        if ((uberFlag == "title-last") or
            (uberFlag == "last") or
            (uberFlag == "first-last") or
            (uberFlag == "title-first-last")):
            lastFlag = 1

        retString = ""
        uberReturn = [0,0,0,'','','','']

        uberReturn[0] = titleFlag
        uberReturn[1] = firstFlag
        uberReturn[2] = lastFlag

        # Choose random names in each slot even if we won't be using
        # them.  That way, if the user activates a previously deactive
        # slot, s/he'll start at a random point in the list instead of
        # always at the top.

        # Shallow copy, since we will be altering the list
        titleList = self.neutralTitles[:]
        if boy:
            titleList += self.boyTitles
        elif girl:
            titleList += self.girlTitles
        else:
            self.error("Must be boy or girl.")

        uberReturn[3] = random.choice(titleList)

        # Shallow copy, since we will be altering the list
        firstList = self.neutralFirsts[:]
        if boy:
            firstList += self.boyFirsts
        elif girl:
            firstList += self.girlFirsts
        else:
            self.error("Must be boy or girl.")

        uberReturn[4] = random.choice(firstList)

        lastPrefix = random.choice(self.lastPrefixes)
        lastSuffix = random.choice(self.lastSuffixes)
        if lastPrefix in self.capPrefixes:
            lastSuffix = lastSuffix.capitalize()
        uberReturn[5] = lastPrefix
        uberReturn[6] = lastSuffix

        # Put a space because there will surely be another name.
        if titleFlag:
            retString += uberReturn[3] + " "

        if firstFlag:
            retString += uberReturn[4]
            # Put a space if there is going to be a last name.
            if lastFlag:
                retString += " "

        if lastFlag:
            retString += uberReturn[5] + uberReturn[6]

        uberReturn.append(retString)
        return uberReturn



    def printRandomNames(self, boy=0, girl=0, total=1):
        i = 0
        origBoy = boy
        origGirl = girl
        while i < total:
            if (not origBoy) and (not origGirl):
                # Randomly pick the name sex
                boy = random.choice([0, 1])
                girl = not boy

            name = self.randomName(boy, girl)
            width = self.text.calcWidth(name)
            widthStr = str(width)
            if boy:
                print("Boy: " + name + " (" + widthStr + " units)")
            if girl:
                print("Girl: " + name + " (" + widthStr + " units)")

            i += 1

    def percentOver(self, limit=9.0, samples=1000):
        i = 0
        over = 0
        while i < samples:
            name = self.randomName()
            width = self.text.calcWidth(name)
            if width > limit:
                over += 1
            i += 1
        percent = (float(over) / float(samples)) * 100
        print(("Samples: " + str(samples) + " Over: " +
               str(over) + " Percent: " + str(percent)))

    def totalNames(self):
        # Firsts only
        firsts = (len(self.boyFirsts) + len(self.girlFirsts) +
                  len(self.neutralFirsts))
        print("Total firsts: " + str(firsts))

        # Lasts only
        lasts = len(self.lastPrefixes) * len(self.lastSuffixes)
        print("Total lasts: " + str(lasts))

        # Title plus first
        neutralTitleFirsts = len(self.neutralTitles) * len(self.neutralFirsts)
        boyTitleFirsts = ((len(self.boyTitles) *
                           (len(self.neutralFirsts) + len(self.boyFirsts))) +
                          ((len(self.neutralTitles) *
                            len(self.boyFirsts))))
        girlTitleFirsts = ((len(self.girlTitles) *
                            (len(self.neutralFirsts) + len(self.girlFirsts))) +
                           ((len(self.neutralTitles) *
                             len(self.girlFirsts))))
        totalTitleFirsts = (neutralTitleFirsts + boyTitleFirsts +
                            girlTitleFirsts)
        print("Total title firsts: " + str(totalTitleFirsts))

        # Title plus last
        neutralTitleLasts = len(self.neutralTitles) * lasts
        boyTitleLasts = (len(self.boyTitles) *
                         lasts)
        girlTitleLasts = (len(self.girlTitles) *
                          lasts)
        totalTitleLasts = (neutralTitleLasts + boyTitleFirsts +
                           girlTitleLasts)
        print("Total title lasts: " + str(totalTitleLasts))

        # First plus last
        neutralFirstLasts = len(self.neutralFirsts) * lasts
        boyFirstLasts = len(self.boyFirsts) * lasts
        girlFirstLasts = len(self.girlFirsts) * lasts
        totalFirstLasts = (neutralFirstLasts + boyFirstLasts +
                           girlFirstLasts)
        print("Total first lasts: " + str(totalFirstLasts))

        # Title plus first plus last
        neutralTitleFirstLasts = neutralTitleFirsts * lasts
        boyTitleFirstLasts = boyTitleFirsts * lasts
        girlTitleFirstLasts = girlTitleFirsts * lasts
        totalTitleFirstLasts = (neutralTitleFirstLasts + boyTitleFirstLasts + girlTitleFirstLasts)
        print("Total title first lasts: " + str(totalTitleFirstLasts))


        # Total
        totalNames = (firsts + lasts + totalTitleFirsts +
                      totalTitleLasts + totalFirstLasts + totalTitleFirstLasts)
        print("Total Names: " + str(totalNames))
