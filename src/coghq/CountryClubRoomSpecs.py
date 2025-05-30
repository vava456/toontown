"""MintRoomSpecs.py: contains table of mint room specs"""

from direct.showbase.PythonUtil import invertDict
from toontown.toonbase import ToontownGlobals
from toontown.coghq import BossbotCountryClubFairwayRoom_Battle00_Cogs
from toontown.coghq import BossbotCountryClubMazeRoom_Battle00_Cogs
from toontown.coghq import BossbotCountryClubMazeRoom_Battle01_Cogs
from toontown.coghq import BossbotCountryClubMazeRoom_Battle02_Cogs
from toontown.coghq import BossbotCountryClubMazeRoom_Battle03_Cogs
from toontown.coghq import NullCogs
from toontown.coghq import BossbotCountryClubKartRoom_Battle00_Cogs
from toontown.coghq import BossbotCountryClubPresidentRoom_Battle00_Cogs

def getCountryClubRoomSpecModule(roomId):
    return CashbotMintSpecModules[roomId]

def getCogSpecModule(roomId):
    roomName = BossbotCountryClubRoomId2RoomName[roomId]
    return CogSpecModules.get(roomName, NullCogs)

def getNumBattles(roomId):
    return roomId2numBattles[roomId]

# things that rooms need:
# r: reward (barrels, etc.)
# s: safe(s)
# x: adjust prop positions

BossbotCountryClubRoomId2RoomName = {
     0: 'BossbotCountryClubEntrance_Action00',
     2: 'BossbotCountryClubTeeOffRoom_Action00',
     4: 'BossbotCountryClubFairwayRoom_Battle00',
     5: 'BossbotCountryClubMazeRoom_Battle00',
     6: 'BossbotCountryClubMazeRoom_Battle01',
     7: 'BossbotCountryClubMazeRoom_Battle02',
     #8: 'BossbotCountryClubMazeRoom_Battle03',
     9: 'BossbotCountryClubGreenRoom_Action00',
    17: 'BossbotCountryClubKartRoom_Battle00',
    18: 'BossbotCountryClubPresidentRoom_Battle00',
    22: 'BossbotCountryClubTeeOffRoom_Action01',
    32: 'BossbotCountryClubTeeOffRoom_Action02',
    29: 'BossbotCountryClubGreenRoom_Action01',
    39: 'BossbotCountryClubGreenRoom_Action02',
    }
BossbotCountryClubRoomName2RoomId = invertDict(BossbotCountryClubRoomId2RoomName)

BossbotCountryClubEntranceIDs   = (0,)
BossbotCountryClubMiddleRoomIDs = (2,5,6)
BossbotCountryClubFinalRoomIDs = (18,)
#CashbotMintMiddleRoomIDs = (1,)
#CashbotMintMiddleRoomIDs = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,)
#CashbotMintFinalRoomIDs  = (17,18,19,20,21,22,23,24,25)

BossbotCountryClubConnectorRooms = ('phase_12/models/bossbotHQ/Connector_Tunnel_A',
                                    'phase_12/models/bossbotHQ/Connector_Tunnel_B')

# dict of roomId to spec Python module
CashbotMintSpecModules = {}
#if not isClient():
#    print("EXECWARNING CountryClubRoomSpecs: %s"%BossbotCountryClubRoomName2RoomId)
#    printStack()
for roomName, roomId in list(BossbotCountryClubRoomName2RoomId.items()):
    exec('from toontown.coghq import %s' % roomName)
    CashbotMintSpecModules[roomId] = eval(roomName)

## until cogs are entities...
CogSpecModules = {
    'BossbotCountryClubFairwayRoom_Battle00' : BossbotCountryClubFairwayRoom_Battle00_Cogs,
    'BossbotCountryClubMazeRoom_Battle00' : BossbotCountryClubMazeRoom_Battle00_Cogs,
    'BossbotCountryClubMazeRoom_Battle01' : BossbotCountryClubMazeRoom_Battle01_Cogs,
    'BossbotCountryClubMazeRoom_Battle02' : BossbotCountryClubMazeRoom_Battle02_Cogs,
    #'BossbotCountryClubMazeRoom_Battle03' : BossbotCountryClubMazeRoom_Battle03_Cogs,
    'BossbotCountryClubKartRoom_Battle00' : BossbotCountryClubKartRoom_Battle00_Cogs,
    'BossbotCountryClubPresidentRoom_Battle00' : BossbotCountryClubPresidentRoom_Battle00_Cogs,    
    }

roomId2numBattles = {}
for roomName, roomId in list(BossbotCountryClubRoomName2RoomId.items()):
    if roomName not in CogSpecModules:
        roomId2numBattles[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        roomId2numBattles[roomId] = len(cogSpecModule.BattleCells)

# override # of battles for some rooms that don't have battle blockers for
# some battles
name2id = BossbotCountryClubRoomName2RoomId
roomId2numBattles[name2id['BossbotCountryClubTeeOffRoom_Action00']] = 1 # 3 test override

#roomId2numBattles[name2id['BossbotCountryClubGreenRoom_Action00']] = 1 # 3 test override
del name2id

# make a table of middle rooms specifically, so MintLayout can easily pick
# and choose battle rooms to meet its battle quota
middleRoomId2numBattles = {}
for roomId in BossbotCountryClubMiddleRoomIDs:
    middleRoomId2numBattles[roomId] = roomId2numBattles[roomId]
