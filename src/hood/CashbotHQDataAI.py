from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedMintElevatorExtAI
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.coghq import LobbyManagerAI
from toontown.building import DistributedCFOElevatorAI
from toontown.suit import DistributedCashbotBossAI
from toontown.building import FADoorCodes
from toontown.building import DistributedBoardingPartyAI
from toontown.toonbase.ToontownModules import ConfigVariableBool

class CashbotHQDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CashbotHqDataAI")

    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.CashbotHQ
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)


    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

        mins = ToontownGlobals.FactoryLaffMinimums[1]

        # TODO: define these in a more modular way
        self.testElev0 = DistributedMintElevatorExtAI.DistributedMintElevatorExtAI(self.air, self.air.mintMgr, ToontownGlobals.CashbotMintIntA, antiShuffle = 0, minLaff = mins[0]) # antiShufflePOI
        self.testElev0.generateWithRequired(ToontownGlobals.CashbotHQ)
        self.addDistObj(self.testElev0)

        self.testElev1 = DistributedMintElevatorExtAI.DistributedMintElevatorExtAI(self.air, self.air.mintMgr, ToontownGlobals.CashbotMintIntB, antiShuffle = 0, minLaff = mins[1]) # antiShufflePOI
        self.testElev1.generateWithRequired(ToontownGlobals.CashbotHQ)
        self.addDistObj(self.testElev1)

        self.testElev2 = DistributedMintElevatorExtAI.DistributedMintElevatorExtAI(self.air, self.air.mintMgr, ToontownGlobals.CashbotMintIntC, antiShuffle = 0, minLaff = mins[2]) # antiShufflePOI
        self.testElev2.generateWithRequired(ToontownGlobals.CashbotHQ)
        self.addDistObj(self.testElev2)

        # Lobby elevator
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, DistributedCashbotBossAI.DistributedCashbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.CashbotLobby)
        self.addDistObj(self.lobbyMgr)

        self.lobbyElevator = DistributedCFOElevatorAI.DistributedCFOElevatorAI(self.air, self.lobbyMgr, ToontownGlobals.CashbotLobby, antiShuffle = 1)#antiShufflePOI
        self.lobbyElevator.generateWithRequired(ToontownGlobals.CashbotLobby)
        self.addDistObj(self.lobbyElevator)

        if ConfigVariableBool('want-boarding-groups', 1).getValue():
            self.boardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.CashbotLobby)

        # CogHQ Main building -> Lobby doors
        destinationZone = ToontownGlobals.CashbotLobby
        extDoor0=DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.EXT_COGHQ,
            destinationZone, doorIndex=0,
            lockValue = FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoorList = [extDoor0]

        # Inside doors
        intDoor0=DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.INT_COGHQ,
            ToontownGlobals.CashbotHQ, doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.CashbotLobby


        mintIdList = [self.testElev0.doId, self.testElev1.doId, self.testElev2.doId]
        if ConfigVariableBool('want-boarding-groups', 1).getValue():
            self.mintBoardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, mintIdList, 4)
            self.mintBoardingParty.generateWithRequired(self.zoneId)

        # Setup the doors and generate them
        for extDoor in extDoorList:
            # Tell them about each other
            extDoor.setOtherDoor(intDoor0)
            # Put them in the right zones
            extDoor.zoneId = ToontownGlobals.CashbotHQ
            # Now that they both now about each other, generate them:
            extDoor.generateWithRequired(ToontownGlobals.CashbotHQ)
            extDoor.sendUpdate("setDoorIndex", [extDoor.getDoorIndex()])
            self.addDistObj(extDoor)

        intDoor0.generateWithRequired(ToontownGlobals.CashbotLobby)
        intDoor0.sendUpdate("setDoorIndex", [intDoor0.getDoorIndex()])
        self.addDistObj(intDoor0)
