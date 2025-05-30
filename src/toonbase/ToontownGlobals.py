"""
ToonBase module: defines constants that are global across Toontown, and
may have meaning to several classes.
"""

from . import TTLocalizer
from otp.otpbase.OTPGlobals import *
from direct.showbase.PythonUtil import Enum, invertDict
from toontown.toonbase.ToontownModules import BitMask32, Vec4

# Questmap Update
MapHotkeyOn = "alt"
MapHotkeyOff = "alt-up"
MapHotkey = "alt"

AccountDatabaseChannelId = 4008
ToonDatabaseChannelId = 4021
DoodleDatabaseChannelId = 4023
DefaultDatabaseChannelId = AccountDatabaseChannelId
DatabaseIdFromClassName = {
    # AccountDatabaseChannelId
    'Account': AccountDatabaseChannelId,

    # ToonDatabaseChannelId
    #'DistributedPlayerToon': ToonDatabaseChannelId,

    # DoodleDatabaseChannelId
    #'DistributedDoodle': DoodleDatabaseChannelId,
    }

# Toontown specific camera FOVs
CogHQCameraFov = 60.0 * OriginalAspectRatio
BossBattleCameraFov = 72.0 * OriginalAspectRatio
MakeAToonCameraFov = 52.0 * OriginalAspectRatio

# Cogdominium collisions
CeilingBitmask = BitMask32(0x100)
FloorEventBitmask = BitMask32(0x10)

# Things we can throw a pie at.  (Pies also react to CameraBitmask and
# FloorBitmask, but not WallBitmask.):
# Brought in from OTPGlobals
PieBitmask = BitMask32(0x100)

# Pets avoid this
PetBitmask = BitMask32(0x08)

# For the catching minigame:
CatchGameBitmask = BitMask32(0x10)

# Things the magnet can pick up in the Cashbot CFO battle (same as
# CatchGameBitmask):
CashbotBossObjectBitmask = BitMask32(0x10)

# These are used by the furniture mover:
FurnitureSideBitmask = BitMask32(0x20)
FurnitureTopBitmask = BitMask32(0x40)
FurnitureDragBitmask = BitMask32(0x80)

# Used to detect who's looking at a pet and who pets are looking at
PetLookatPetBitmask = BitMask32(0x100)
PetLookatNonPetBitmask = BitMask32(0x200)

# Bitmask for the DistributedBanquetTable
BanquetTableBitmask = BitMask32(0x400)

# When we have this many pies, it means an infinite number.
FullPies = 65535

CogHQCameraFar = 900.0
CogHQCameraNear = 1.0

CashbotHQCameraFar = 2000.0
CashbotHQCameraNear = 1.0

LawbotHQCameraFar = 3000.0
LawbotHQCameraNear = 1.0

BossbotHQCameraFar = 3000.0
BossbotHQCameraNear = 1.0

SpeedwayCameraFar = 8000.0
SpeedwayCameraNear = 1.0

# How many items can be in the mailbox (or on the way to the mailbox)
# at once?
MaxMailboxContents = 30

# The maximum number of items you can have anywhere in your house at
# all, including in the attic.  This includes windows and wallpaper in
# the attic, but not those windows and wallpaper which are installed.
MaxHouseItems = 45

# The maximum number of accessories you can keep in your trunk.
MaxAccessories = 50

# How many extra items, over the above limit, can we keep on the
# deletedItems list?
ExtraDeletedItems = 5

# How many minutes to keep an item on the deletedItems list.
DeletedItemLifetime = 7 * 24 * 60

# How many weeks are in each catalog series?
CatalogNumWeeksPerSeries = 13

# How many total weeks are there in the catalog before we're done?
CatalogNumWeeks = 78

# task priorities
PetFloorCollPriority = 5 # must run after smoothing and before main
                         # collision loop
PetPanelProximityPriority = 6 # must run after pet floor collisions
                              # so that pet is at correct Z

# purchase codes returned by DistributedMailbox.acceptItem(), -15 and up extended for award manager
# DistributedPhone.requestPurchase, and CatalogItem.recordPurchase().
# In general, positive codes are success, negative codes are failure.
P_NoTrunk = -28 # doesn't own a trunk
P_AlreadyOwnBiggerCloset = -27 # already owns the bigger closet
P_ItemAlreadyRented = -26 # item already rented
P_OnAwardOrderListFull = -25 # unlikely, but just in case, he won 30 awards and their still in his onAwardOrder list
P_AwardMailboxFull = -24 # the award mailbox is full and can't take more
P_ItemInPetTricks= -23 # trying to give a pet trick award but the toon has it in his pet tricks
P_ItemInMyPhrases= -22 # trying to give a speed chat award but the toon has it in his My Phrases
P_ItemOnAwardOrder = -21 # trying to give an award but the toon has it onAwardOrder,
P_ItemInAwardMailbox = -20 # trying to give an award but the toon has it in his award mailbox
P_ItemAlreadyWorn = -19  # trying to give an award but the toon is already wearing the clothing item
P_ItemInCloset = -18  # trying to give an award but the toon has it in his closet
P_ItemOnGiftOrder = -17 # trying to give an award but the toon has it in the gift order queue
P_ItemOnOrder = -16 # trying to give an award but the toon has it in his onOrder queue
P_ItemInMailbox = -15 # trying to give an award but the toon has it in his mailbox
P_PartyNotFound = 14 # suspicious doublecheck if it needs to be negative
P_WillNotFit = -13
P_NotAGift = -12
P_OnOrderListFull = -11
P_MailboxFull = -10
P_NoPurchaseMethod = -9
P_ReachedPurchaseLimit = -8
P_NoRoomForItem = -7
P_NotShopping = -6
P_NotAtMailbox = -5
P_NotInCatalog = -4
P_NotEnoughMoney = -3
P_InvalidIndex = -2
P_UserCancelled = -1

P_ItemAvailable = 1
P_ItemOnOrder = 2
P_ItemUnneeded = 3

#gift codes
GIFT_user = 0
GIFT_admin = 1
GIFT_RAT = 2
GIFT_mobile = 3
GIFT_cogs = 4
GIFT_partyrefund = 5

# codes returned by DistributedFurnitureManager.moveItemToAttic,
# moveItemFromAttic, deleteItemFromAttic, and all similar related
# functions for wallpaper and windows.
FM_InvalidItem = -7
FM_NondeletableItem = -6
FM_InvalidIndex = -5
FM_NotOwner = -4
FM_NotDirector = -3
FM_RoomFull = -2
FM_HouseFull = -1
FM_MovedItem = 1
FM_SwappedItem = 2
FM_DeletedItem = 3
FM_RecoveredItem = 4

# Bits for the friend flags.  Presently, we only use bit 1.
#FriendChat = 1 # OTPGlobals

# Bits for the DistributedAvatar.commonChat word.
#CommonChat = 1 # OTPGlobals
#SuperChat = 2 # OTPGlobals

# Maximum number of custom chat phrases
#MaxCustomMessages = 15 # OTPGlobals

# Tokens for the various nodes we can parent avatars to via
# distributed setParent().
#SPHidden = 1 # OTPGlobals
#SPRender = 2 # OTPGlobals
#SPActors = 3 # OTPGlobals
SPDonaldsBoat = 4
SPMinniesPiano = 5
#SPDynamic = 6 # OTPGlobals

# These are in OTPGlobals
"""
# Cheesy rendering effects.
CENormal = 0
CEBigHead = 1
CESmallHead = 2
CEBigLegs = 3
CESmallLegs = 4
CEBigToon = 5
CESmallToon = 6
CEFlatPortrait = 7
CEFlatProfile = 8
CETransparent = 9
CENoColor = 10
CEInvisible = 11
CEPumpkin = 12
CEBigWhite = 13

# This one is not really a cheesy effect, but it is implemented by the
# cheesy effect system.  It's a string rather than a number to ensure
# that no one cheats and asks for this via the cheesy effect
# distributed message.
CEGhost = 'g'

# How big is big and how small is small?
BigToonScale = 1.5
SmallToonScale = 0.5
"""
#why are the above part of otp? JML
CEVirtual = 14

# Cap on the max hp
# Quests =   100
# Fishing =    7
# Racing =     3
# Lawbot HQ  = 5
# Cashbot HQ = 5
# Sellbot HQ = 5
# Gardening  = 4
# Golf       = 3
# Bossbot HQ = 5
MaxHpLimit = 137
# Cap on the max carry
MaxCarryLimit = 80
# Cap on the max carry
MaxQuestCarryLimit = 4

# the highest level you can attain for your Cog HQ cog suit
# levels are stored zero-based, so subtract one
MaxCogSuitLevel = 50-1
# the cog suit levels (of the most advanced cog suit of track) at which
# you get a +1 HP boost
# levels are stored zero-based, so subtract one
# NOTE: add 5 to MaxHpLimit every time we add a cog HQ
CogSuitHPLevels = (15-1,20-1,30-1,40-1,50-1,)

# How fast must we move before we start to walk?
#WalkCutOff = 0.5 # OTPGlobals

# How fast must we move before we break into a run cycle?
#RunCutOff = 8.0 # OTPGlobals

# Override some values in OTPGlobals
setInterfaceFont(TTLocalizer.InterfaceFont)
setSignFont(TTLocalizer.SignFont)
from toontown.toontowngui import TTDialog
setDialogClasses(TTDialog.TTDialog, TTDialog.TTGlobalDialog)

ToonFont = None
BuildingNametagFont = None
MinnieFont = None
SuitFont = None

# New Function to Choose Custom Fonts for Gateway
def getToonFont():
    global ToonFont
    if (ToonFont == None):
        ToonFont = loader.loadFont(TTLocalizer.ToonFont, lineHeight = 1.0)
    return ToonFont

def getBuildingNametagFont():
    global BuildingNametagFont
    if BuildingNametagFont == None:
        BuildingNametagFont = loader.loadFont(TTLocalizer.BuildingNametagFont)
    return BuildingNametagFont

def getMinnieFont():
    global MinnieFont
    if MinnieFont == None:
        MinnieFont = loader.loadFont(TTLocalizer.MinnieFont)
    return MinnieFont

def getSuitFont():
    global SuitFont
    if SuitFont == None:
        SuitFont = loader.loadFont(TTLocalizer.SuitFont,
                                   pixelsPerUnit = 40,
                                   spaceAdvance = 0.25, lineHeight = 1.0)
    return SuitFont


#### ZONE IDs ####

# Hood ids.  These are also the zone ids of the corresponding
# safezone, and also represent the first of a range of 1000 zone ids
# allocated to each hood.
DonaldsDock =           1000
ToontownCentral =       2000
TheBrrrgh =             3000
MinniesMelodyland =     4000
DaisyGardens =          5000
OutdoorZone =           6000
FunnyFarm =             7000
GoofySpeedway =         8000
DonaldsDreamland =      9000

# Street Branch zones
# DonaldsDock
BarnacleBoulevard =  1100
SeaweedStreet =      1200
LighthouseLane =     1300
# ToontownCentral
SillyStreet =        2100
LoopyLane =          2200
PunchlinePlace =     2300
# TheBrrrgh
WalrusWay =          3100
SleetStreet =        3200
PolarPlace =         3300
# MinniesMelodyland
AltoAvenue =         4100
BaritoneBoulevard =  4200
TenorTerrace =       4300
# DaisyGardens
ElmStreet =          5100
MapleStreet =        5200
OakStreet =          5300
# DonaldsDreamland
LullabyLane =        9100
PajamaPlace =        9200

# Keep a static zoneId for toonhall
ToonHall = 2513

HoodHierarchy = {
    ToontownCentral : (SillyStreet, LoopyLane, PunchlinePlace),
    DonaldsDock : (BarnacleBoulevard, SeaweedStreet, LighthouseLane),
    TheBrrrgh : (WalrusWay, SleetStreet, PolarPlace),
    MinniesMelodyland : (AltoAvenue, BaritoneBoulevard, TenorTerrace),
    DaisyGardens : (ElmStreet, MapleStreet, OakStreet),
    DonaldsDreamland : (LullabyLane, PajamaPlace),
    GoofySpeedway : (),
    }

# This is a special case.  It's not a real zoneId, but is used to
# represent the entire collection of WelcomeValley zones, which is
# maintained by the AI.  Requesting a transfer to this zone really
# means to go to a WelcomeValley zone of the AI's choosing.
WelcomeValleyToken =    0

# CogHQ hood/zone ids. (Some of these are not real zoneIds but are here
# so that quests can specify them as locations.)
BossbotHQ =            10000
BossbotLobby =         10100
BossbotCountryClubIntA = 10500
BossbotCountryClubIntB = 10600
BossbotCountryClubIntC = 10700
SellbotHQ =            11000
SellbotLobby =         11100
SellbotFactoryExt =    11200
SellbotFactoryInt =    11500 # for the sake of quests
CashbotHQ =            12000
CashbotLobby =         12100
CashbotMintIntA =      12500 # for the sake of quests
CashbotMintIntB =      12600 # for the sake of quests
CashbotMintIntC =      12700 # for the sake of quests
LawbotHQ =             13000
LawbotLobby =          13100
LawbotOfficeExt =      13200
LawbotOfficeInt =      13300 #should be a dynamic instance
LawbotStageIntA =      13300 # for the sake of quests
LawbotStageIntB =      13400 # for the sake of quests
LawbotStageIntC =      13500 # for the sake of quests
LawbotStageIntD =      13600 # for the sake of quests

# These are hood ids, but they are not zone ids.
Tutorial =             15000
MyEstate =             16000

# Minigolf hood ids
GolfZone =             17000

# Party zone hood id
PartyHood =            18000

# These hoods are considered children of other hoods and don't need to be explicitly visited
# NOTE: add all new zones of of the OZ here!
HoodsAlwaysVisited = [17000,18000,]

# This is the pool of zone ids reserved for the dynamically-allocated
# copies of ToontownCentral known as WelcomeValley.  Each dynamic hood
# gets 1000 zone ids.
WelcomeValleyBegin =      22000
WelcomeValleyEnd =        61000

# Everything from this zone up to the top of the available range is
# reserved for the dynamic zone pool.  Note that our effective maximum
# zone may be less than DynamicZonesEnd, depending on the assignment
# of available doIds--we must be careful not to overlap.
DynamicZonesBegin =    61000
DynamicZonesEnd =      (1 << 20)


cogDept2index = {
    'c':0,
    'l':1,
    'm':2,
    's':3,
    }
cogIndex2dept = invertDict(cogDept2index)

HQToSafezone = {
    SellbotHQ : DaisyGardens,
    CashbotHQ : DonaldsDreamland,
    LawbotHQ : TheBrrrgh,
    BossbotHQ : DonaldsDock, # ?
    }

CogDeptNames = [
    TTLocalizer.Bossbot,
    TTLocalizer.Lawbot,
    TTLocalizer.Cashbot,
    TTLocalizer.Sellbot,
    ]

# cogHQ hood id to dept index
def cogHQZoneId2deptIndex(zone):
    assert (zone >= 10000) and (zone <= 13999)
    if (zone >= 13000) and (zone <= 13999):
        return 1  # lawbot
    elif zone >= 12000:
        return 2  # cashbot
    elif zone >= 11000:
        return 3  # sellbot
    else:
        return 0  # bossbot

def cogHQZoneId2dept(zone):
    return cogIndex2dept[cogHQZoneId2deptIndex(zone)]

def dept2cogHQ(dept):
    dept2hq = {
        'c' : BossbotHQ, 'l' : LawbotHQ,
        'm' : CashbotHQ, 's' : SellbotHQ,
        }
    return dept2hq[dept]

# this is a phony zoneId for the 'mockup' testbed factory
MockupFactoryId  = 0

# these do not include the first (entrance) room of the mint floor
# mintId->(min,max)
MintNumFloors = {
    CashbotMintIntA : 20,
    CashbotMintIntB : 20,
    CashbotMintIntC : 20,
    }

CashbotMintCogLevel      = 10
CashbotMintSkelecogLevel = 11
CashbotMintBossLevel     = 12

# An average DL 5-story building has about 224 cog 'level' points total.
# Every Mint battle has 4 cogs, and cog levels vary from
# CashbotMintCogLevel to CashbotMintCogLevel+1.
# 224 levels / 10.5 levels/cog = 21.33 cogs
# 21.33 cogs / 4 cogs/battle = 5
#
# As a point of reference, the factory has a minimum of 6 battles, with 3
# cogs in most battles, for a total of 18 cogs.

MintNumBattles = {
    CashbotMintIntA : 4, # 16 cogs = 8 merits
    CashbotMintIntB : 6, # 24 cogs = 12 merits
    CashbotMintIntC : 8, # 32 cogs = 16 merits
    }

MintCogBuckRewards = {
    CashbotMintIntA : 8,  #  8 * 1.0
    CashbotMintIntB : 14, # 12 * 1.1
    CashbotMintIntC : 20, # 16 * 1.2
    }

# these room counts do NOT include the entrance room
# table of mintId->list of num rooms for each floor
MintNumRooms = {
    CashbotMintIntA : 2*( 6,) + 5*( 7,) + 5*( 8,) + 5*( 9,) + 3*(10,),
    CashbotMintIntB : 3*( 8,) + 6*( 9,) + 6*(10,) + 5*(11,),
    CashbotMintIntC : 4*(10,) +10*(11,) + 6*(12,),
    }
if __debug__:
    for mintId in MintNumRooms:
        assert len(MintNumRooms[mintId]) == MintNumFloors[mintId]

# Country Club
BossbotCountryClubCogLevel      = 11
BossbotCountryClubSkelecogLevel = 12
BossbotCountryClubBossLevel     = 12

CountryClubNumRooms = {
    BossbotCountryClubIntA : (4,), #2*( 6,) + 5*( 7,) + 5*( 8,) + 5*( 9,) + 3*(10,),
    BossbotCountryClubIntB : 3*( 8,) + 6*( 9,) + 6*(10,) + 5*(11,),
    BossbotCountryClubIntC : 4*(10,) +10*(11,) + 6*(12,),
    }

CountryClubNumBattles = {
    BossbotCountryClubIntA : 3,
    BossbotCountryClubIntB : 2,
    BossbotCountryClubIntC : 3,
    }

CountryClubCogBuckRewards = {
    BossbotCountryClubIntA: 8,  #  8 * 1.0
    BossbotCountryClubIntB : 14, # 12 * 1.1
    BossbotCountryClubIntC: 20, # 16 * 1.2
    }

#Stage

LawbotStageCogLevel      = 10
LawbotStageSkelecogLevel = 11
LawbotStageBossLevel     = 12

# An average DL 5-story building has about 224 cog 'level' points total.
# Every Stage battle has 4 cogs, and cog levels vary from
# LawbotStageCogLevel to LawbotStageCogLevel+1.
# 224 levels / 10.5 levels/cog = 21.33 cogs
# 21.33 cogs / 4 cogs/battle = 5
#
# As a point of reference, the factory has a minimum of 6 battles, with 3
# cogs in most battles, for a total of 18 cogs.

StageNumBattles = {
    LawbotStageIntA : 0, # 16 cogs = 8 merits
    LawbotStageIntB : 0, # 24 cogs = 12 merits
    LawbotStageIntC : 0, # 32 cogs = 16 merits
    LawbotStageIntD : 0, # 40 cogs = 20 merits
    }

StageNoticeRewards = {
    LawbotStageIntA : 75,
    LawbotStageIntB : 150,
    LawbotStageIntC : 225,
    LawbotStageIntD : 300,
    }

# these room counts do NOT include the entrance room
# table of stageId->list of num rooms for each floor
StageNumRooms = {
    LawbotStageIntA : 2*( 6,) + 5*( 7,) + 5*( 8,) + 5*( 9,) + 3*(10,),
    LawbotStageIntB : 3*( 8,) + 6*( 9,) + 6*(10,) + 5*(11,),
    LawbotStageIntC : 4*(10,) +10*(11,) + 6*(12,),
    LawbotStageIntD : 4*(10,) +10*(11,) + 6*(12,),
    }
"""
if __debug__:
    for stageId in StageNumRooms:
        assert len(StageNumRooms[stageId]) == StageNumFloors[stageId]
        """

# CogHQ factory types
# these are internal, do not localize
FT_FullSuit = 'fullSuit'
FT_Leg      = 'leg'
FT_Arm      = 'arm'
FT_Torso    = 'torso'

# 'factory id' is actually the faux-zone set aside for the factory
factoryId2factoryType = {
    MockupFactoryId: FT_FullSuit,
    SellbotFactoryInt: FT_FullSuit,
    LawbotOfficeInt: FT_FullSuit,
    }


# Street names
StreetNames = TTLocalizer.GlobalStreetNames
StreetBranchZones = list(StreetNames.keys())

# hood name list
Hoods = ( DonaldsDock,
          ToontownCentral,
          TheBrrrgh,
          MinniesMelodyland,
          DaisyGardens,
          OutdoorZone,
          FunnyFarm,
          GoofySpeedway,
          DonaldsDreamland,
          BossbotHQ,
          SellbotHQ,
          CashbotHQ,
          LawbotHQ,
          GolfZone,
          )

HoodsForTeleportAll = ( DonaldsDock,
          ToontownCentral,
          TheBrrrgh,
          MinniesMelodyland,
          DaisyGardens,
          OutdoorZone,
          GoofySpeedway,
          DonaldsDreamland,
          BossbotHQ,
          SellbotHQ,
          CashbotHQ,
          LawbotHQ,
          GolfZone,
          )

# Minigame Ids
# This id indicates that this is the first game in a trolley
# sequence. We need to keep track because we don't want to
# ever play the same game twice in a row.
NoPreviousGameId = 0
# Real game Ids
RaceGameId = 1
CannonGameId = 2
TagGameId = 3
PatternGameId = 4
RingGameId = 5
MazeGameId = 6
TugOfWarGameId = 7
CatchGameId = 8
DivingGameId = 9
TargetGameId = 10
PairingGameId = 11
VineGameId = 12
IceGameId = 13
CogThiefGameId = 14
TwoDGameId = 15
PhotoGameId = 16
TravelGameId = 100 # only used in trolley metagame


MinigameNames = {
    "race" : RaceGameId,
    "cannon" : CannonGameId,
    "tag" : TagGameId,
    "pattern" : PatternGameId,
    "minnie" : PatternGameId,
    "match" : PatternGameId,
    "matching" : PatternGameId,
    "ring" : RingGameId,
    "maze" : MazeGameId,
    "tug" : TugOfWarGameId,
    "catch" : CatchGameId,
    "diving" : DivingGameId,
    "target" : TargetGameId,
    "pairing" : PairingGameId,
    "vine" : VineGameId,
    "ice" : IceGameId,
    "thief" : CogThiefGameId,
    "2d" : TwoDGameId,
    "photo" : PhotoGameId,
    "travel" : TravelGameId,
    }

# the minigame template; not used in final game
MinigameTemplateId = -1


MinigameIDs = ( RaceGameId, CannonGameId, TagGameId, PatternGameId, RingGameId, MazeGameId, TugOfWarGameId, CatchGameId, DivingGameId, TargetGameId, PairingGameId, VineGameId, IceGameId, CogThiefGameId, TwoDGameId, PhotoGameId, TravelGameId,)


# Minigame Id list
MinigamePlayerMatrix = {
    # If you only have one player, choose from these games
    # Technically pattern game can be single player, but it is not nearly as fun, especially for demos
    1 : (CannonGameId, PatternGameId, RingGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         CogThiefGameId, PhotoGameId, TwoDGameId),
    # If you have exactly two players, choose from these games
    2 : (CannonGameId, PatternGameId, RingGameId, TagGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         IceGameId, CogThiefGameId, PhotoGameId, TwoDGameId),
    # If you have exactly three players, choose from these games
    3 : (CannonGameId, PatternGameId, RingGameId, TagGameId, RaceGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         IceGameId, CogThiefGameId, PhotoGameId, TwoDGameId),
    # If you have exactly four players, choose from these games
    4 : (CannonGameId, PatternGameId, RingGameId, TagGameId, RaceGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         IceGameId, CogThiefGameId, PhotoGameId, TwoDGameId),
    }

# ONLY USE WHEN DECIDED TO REMOVE THE PHOTO AND PATTERN GAME!
"""
# Minigame Id list
MinigamePlayerMatrix = {
    # If you only have one player, choose from these games
    # Technically pattern game can be single player, but it is not nearly as fun, especially for demos
    1 : (CannonGameId, RingGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         CogThiefGameId, TwoDGameId),
    # If you have exactly two players, choose from these games
    2 : (CannonGameId, PatternGameId, RingGameId, TagGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         IceGameId, CogThiefGameId, TwoDGameId),
    # If you have exactly three players, choose from these games
    3 : (CannonGameId, PatternGameId, RingGameId, TagGameId, RaceGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         IceGameId, CogThiefGameId, TwoDGameId),
    # If you have exactly four players, choose from these games
    4 : (CannonGameId, PatternGameId, RingGameId, TagGameId, RaceGameId, MazeGameId, TugOfWarGameId, CatchGameId,
         DivingGameId, TargetGameId, PairingGameId, VineGameId,
         IceGameId, CogThiefGameId, TwoDGameId),
    }
"""

# we are releasing one minigame a week for the new minigames
MinigameReleaseDates = {
    IceGameId : (2008, 8, 0o5),
    PhotoGameId : (2008,8,13),
    TwoDGameId : (2008,8,20),
    CogThiefGameId : (2008,8,27),
    }

# Moved to OTPGlobals
"""
# Hotkeys
ThinkPosHotkey = "f1-up"
PlaceMarkerHotkey = "f2-up"
FriendsListHotkey = "f7-up"
StickerBookHotkey = "f8-up"
OptionsPageHotkey = "escape-up"
ScreenshotHotkey = "f9-up"
SynchronizeHotkey = "f6-up"
QuestsHotkeyOn = "end"
QuestsHotkeyOff = "end-up"
InventoryHotkeyOn = "home"
InventoryHotkeyOff = "home-up"
PrintCamPosHotkey = "f12-up"   # just for dbging
"""

# Keyboard inactivity timeout
KeyboardTimeout = 300

# Maps hoods to download phases
phaseMap = {
    Tutorial : 4,
    ToontownCentral : 4, # TT streets are in 5
    MyEstate : 5.5,
    DonaldsDock : 6,
    MinniesMelodyland : 6,
    GoofySpeedway : 6,
    TheBrrrgh : 8,
    DaisyGardens : 8,
    FunnyFarm : 8,
    DonaldsDreamland : 8,
    OutdoorZone : 8,
    BossbotHQ : 12,
    SellbotHQ : 9,
    CashbotHQ : 10,
    LawbotHQ : 11,
    GolfZone : 8,
    PartyHood : 13,
    }


# town streets to download phases
streetPhaseMap = {
    ToontownCentral : 5,
    DonaldsDock : 6,
    MinniesMelodyland : 6,
    GoofySpeedway : 6,
    TheBrrrgh : 8,
    DaisyGardens : 8,
    FunnyFarm : 8,
    DonaldsDreamland : 8,
    OutdoorZone : 8,
    BossbotHQ : 12,
    SellbotHQ : 9,
    CashbotHQ : 10,
    LawbotHQ : 11,
    PartyHood : 13,
    }


# Maps hoods to download phases
dnaMap = {
    Tutorial : "toontown_central",
    ToontownCentral : "toontown_central",
    DonaldsDock : "donalds_dock",
    MinniesMelodyland : "minnies_melody_land",
    GoofySpeedway : "goofy_speedway",
    TheBrrrgh : "the_burrrgh",
    DaisyGardens : "daisys_garden",
    FunnyFarm : "not done yet",
    DonaldsDreamland : "donalds_dreamland",
    OutdoorZone : "outdoor_zone",
    BossbotHQ : "cog_hq_bossbot",
    SellbotHQ : "cog_hq_sellbot",
    CashbotHQ : "cog_hq_cashbot",
    LawbotHQ : "cog_hq_lawbot",
    GolfZone : "golf_zone",
    }

# Maps hoods to download phases
# TEMP
dnaMapQuest = {
    ToontownCentral : "toontown_central",
    DonaldsDock : "donalds_dock",
    MinniesMelodyland : "minnies_melody_land",
    TheBrrrgh : "the_burrrgh",
    DaisyGardens : "daisys_garden",
    FunnyFarm : "not done yet",
    DonaldsDreamland : "donalds_dreamland",
    }

# Maps hoods to names
hoodNameMap = {
    DonaldsDock : TTLocalizer.DonaldsDock,
    ToontownCentral : TTLocalizer.ToontownCentral,
    TheBrrrgh : TTLocalizer.TheBrrrgh,
    MinniesMelodyland : TTLocalizer.MinniesMelodyland,
    DaisyGardens : TTLocalizer.DaisyGardens,
    OutdoorZone : TTLocalizer.OutdoorZone,
    FunnyFarm : TTLocalizer.FunnyFarm,
    GoofySpeedway : TTLocalizer.GoofySpeedway,
    DonaldsDreamland : TTLocalizer.DonaldsDreamland,
    BossbotHQ : TTLocalizer.BossbotHQ,
    SellbotHQ : TTLocalizer.SellbotHQ,
    CashbotHQ : TTLocalizer.CashbotHQ,
    LawbotHQ : TTLocalizer.LawbotHQ,
    Tutorial : TTLocalizer.Tutorial,
    MyEstate : TTLocalizer.MyEstate,
    GolfZone : TTLocalizer.GolfZone,
    PartyHood : TTLocalizer.PartyHood
    }

# map of number of things to load per zone
safeZoneCountMap = {
    MyEstate : 8 ,
    Tutorial : 6,
    ToontownCentral : 6,
    DonaldsDock : 10,
    MinniesMelodyland : 5,
    GoofySpeedway : 500,
    TheBrrrgh : 8,
    DaisyGardens : 9,
    FunnyFarm : 500,
    DonaldsDreamland : 5,
    OutdoorZone : 500,
    GolfZone : 500,
    PartyHood : 500,
    }

townCountMap = {
    # HACK! JNS just guessed at a tutorial count.
    # and SDN guessed at Estate count
    MyEstate : 8 ,
    Tutorial : 40 ,
    ToontownCentral : 37,
    DonaldsDock : 40,
    MinniesMelodyland : 40,
    GoofySpeedway : 40,
    TheBrrrgh : 40,
    DaisyGardens : 40,
    FunnyFarm : 40,
    DonaldsDreamland : 40,
    OutdoorZone : 40,
    PartyHood : 20,
    }

hoodCountMap = {
    MyEstate : 2,
    Tutorial : 2,
    ToontownCentral : 2,
    DonaldsDock : 2,
    MinniesMelodyland : 2,
    GoofySpeedway : 2,
    TheBrrrgh : 2,
    DaisyGardens : 2,
    FunnyFarm : 2,
    DonaldsDreamland : 2,
    OutdoorZone : 2,
    BossbotHQ : 2,
    SellbotHQ : 43,
    CashbotHQ : 2,
    LawbotHQ : 2,
    GolfZone : 2,
    PartyHood : 2,
    }

# Number of buildings you must have in your name to earn stars.
# Note - these have gone up since the credit is based on the size of the building now
TrophyStarLevels = (
    10,  # A bronze star
    20,  # A spinning bronze star
    30,  # A silver star
    50,  # A spinning silver star
    75,  # A gold star
    100, # A spinning gold star
    )

TrophyStarColors = (
    Vec4(0.9,0.6,0.2,1),  # A bronze star
    Vec4(0.9,0.6,0.2,1),  # A bronze star
    Vec4(0.8,0.8,0.8,1),  # A silver star
    Vec4(0.8,0.8,0.8,1),  # A silver star
    Vec4(1,1,0,1),        # A gold star
    Vec4(1,1,0,1),        # A gold star
    )

# OTPGlobals
"""
ToonStandableGround = 0.707 # if ToonStandableGround > angle: toon is on ground.

ToonForwardSpeed = 16.0 # feet per second
ToonJumpForce = 24.0 # feet per second
ToonReverseSpeed = 8.0 # feet per second
ToonRotateSpeed = 80.0

# When you are "dead"
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0 # feet per second
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0
"""

MickeySpeed = 5.0 # feet per second
VampireMickeySpeed = 1.15
#VampireMickeySpeed = 5.15
MinnieSpeed = 3.2 # feet per second
WitchMinnieSpeed = 1.8
#DonaldSpeed = 4.6 # feet per second
DonaldSpeed = 3.68 # feet per second
FrankenDonaldSpeed = 0.9
DaisySpeed  = 2.3 # feet per second
GoofySpeed  = 5.2 # feet per second
SuperGoofySpeed = 1.6 # fps
PlutoSpeed  = 5.5 # feet per second per second
WesternPlutoSpeed = 3.2
ChipSpeed  = 3 # feet per second
DaleSpeed  = 3.5 # feet per second
DaleOrbitDistance = 3# feet


SuitWalkSpeed = 4.8

# The various pre-defined pieCode values in the world.  These are used
# in the throw-a-pie-wherever-you-want interface, particularly in the
# final boss battle.
PieCodeBossCog = 1
PieCodeNotBossCog = 2
PieCodeToon = 3
PieCodeBossInsides = 4
PieCodeDefensePan = 5 #defense pan for lawbot boss battle
PieCodeProsecutionPan =6  #prosecution pan for lawbot boss battle
PieCodeLawyer = 7 #prosecution lawyers for lawbot boss battle


# And the splat colors, if any, that correspond to a hit on any of the
# above.
PieCodeColors = {
    PieCodeBossCog : None,  # A successful hit on the boss cog is in color.
    PieCodeNotBossCog : (0.8, 0.8, 0.8, 1),
    PieCodeToon : None,     # hitting a toon is also in color.
    }



BossCogRollSpeed = 7.5
BossCogTurnSpeed = 20
BossCogTreadSpeed = 3.5


# Boss Cog attack codes:
BossCogDizzy = 0
BossCogElectricFence = 1
BossCogSwatLeft = 2
BossCogSwatRight = 3
BossCogAreaAttack = 4
BossCogFrontAttack = 5
BossCogRecoverDizzyAttack = 6
BossCogDirectedAttack = 7
BossCogStrafeAttack = 8
BossCogNoAttack = 9
BossCogGoonZap = 10
BossCogSlowDirectedAttack = 11
BossCogDizzyNow = 12
BossCogGavelStomp = 13
BossCogGavelHandle = 14
BossCogLawyerAttack = 15
BossCogMoveAttack = 16
BossCogGolfAttack = 17
BossCogGolfAreaAttack = 18
BossCogGearDirectedAttack = 19
BossCogOvertimeAttack = 20

# The amount of time it takes to play each attack.
BossCogAttackTimes = {
    BossCogElectricFence : 0,
    BossCogSwatLeft : 5.5,
    BossCogSwatRight : 5.5,
    BossCogAreaAttack : 4.21,
    BossCogFrontAttack : 2.65,
    BossCogRecoverDizzyAttack : 5.1,
    BossCogDirectedAttack : 4.84,
    BossCogNoAttack : 6,
    BossCogSlowDirectedAttack : 7.84,
    BossCogMoveAttack : 3,
    BossCogGolfAttack: 6,
    BossCogGolfAreaAttack: 7,
    BossCogGearDirectedAttack : 4.84,
    BossCogOvertimeAttack : 5,
    }

# The damage that each attack applies to a Toon.
BossCogDamageLevels = {
    BossCogElectricFence : 1,
    BossCogSwatLeft : 5,
    BossCogSwatRight : 5,
    BossCogAreaAttack: 10,
    BossCogFrontAttack: 3,
    BossCogRecoverDizzyAttack: 3,
    BossCogDirectedAttack: 3,
    BossCogStrafeAttack : 2,
    BossCogGoonZap : 5,
    BossCogSlowDirectedAttack : 10,
    BossCogGavelStomp : 20,
    BossCogGavelHandle : 2,
    BossCogLawyerAttack : 5,
    BossCogMoveAttack : 20,
    BossCogGolfAttack: 15,
    BossCogGolfAreaAttack: 15,
    BossCogGearDirectedAttack: 15,
    BossCogOvertimeAttack : 10,
    }


# Where are the Boss Cog's battles relative to him?
BossCogBattleAPosHpr = (0, -25, 0, 0, 0, 0)
BossCogBattleBPosHpr = (0, 25, 0, 180, 0, 0)

# How many pie hits does it take to kill the Sellbot VP?
SellbotBossMaxDamage = 100

# How many pie hits does it take to kill the Nerfed Sellbot VP?
SellbotBossMaxDamageNerfed = 100

# How many pie hits does it take to kill the Sellbot VP?
SellbotBossMaxDamageNerfed = 100

# Where is the Sellbot Boss sitting in the three stages of the
# VP sequence?
SellbotBossBattleOnePosHpr = (0, -35, 0, -90, 0, 0)
SellbotBossBattleTwoPosHpr = (0, 60, 18, -90, 0, 0)
SellbotBossBattleThreeHpr = (180, 0, 0)
SellbotBossBottomPos = (0, -110, -6.5)
SellbotBossDeathPos = (0, -175, -6.5)

# Where do the VP's doobers walk to?
SellbotBossDooberTurnPosA = (-20, -50, 0)
SellbotBossDooberTurnPosB = (20, -50, 0)
SellbotBossDooberTurnPosDown = (0, -50, 0)
SellbotBossDooberFlyPos = (0, -135, -6.5)

# How does the VP roll up the ramp?
SellbotBossTopRampPosA = (-80, -35, 18)
SellbotBossTopRampTurnPosA = (-80, 10, 18)
SellbotBossP3PosA = (-50, 40, 18)
SellbotBossTopRampPosB = (80, -35, 18)
SellbotBossTopRampTurnPosB = (80, 10, 18)
SellbotBossP3PosB = (50, 60, 18)


# How many points does it take to kill the Cashbot CFO?
CashbotBossMaxDamage = 500

# Where is the Cashbot Boss sitting in the CFO sequence?
CashbotBossOffstagePosHpr = (120, -195, 0, 0, 0, 0)
CashbotBossBattleOnePosHpr = (120, -230, 0, 90, 0, 0)
CashbotRTBattleOneStartPosHpr = (94, -220, 0, 110, 0, 0)
CashbotBossBattleThreePosHpr = (120, -315, 0, 180, 0, 0)

# Where are the starting points for the toons in battle 3?
CashbotToonsBattleThreeStartPosHpr = [
    (105, -285, 0, 208, 0, 0),
    (136, -342, 0, 398, 0, 0),
    (105, -342, 0, 333, 0, 0),
    (135, -292, 0, 146, 0, 0),
    (93, -303, 0, 242, 0, 0),
    (144, -327, 0, 64, 0, 0),
    (145, -302, 0, 117, 0, 0),
    (93, -327, 0, -65, 0, 0),
    ]
# How many safes in the final battle sequence, and where are they?
CashbotBossSafePosHprs = [
    (120, -315, 30, 0, 0, 0),    # safe 0 is special; it drops on from above.
    (77.2, -329.3, 0, -90, 0, 0),
    (77.1, -302.7, 0, -90, 0, 0),
    (165.7, -326.4, 0, 90, 0, 0),
    (165.5, -302.4, 0, 90, 0, 0),
    (107.8, -359.1, 0, 0, 0, 0),
    (133.9, -359.1, 0, 0, 0, 0),
    (107.0, -274.7, 0, 180, 0, 0),
    (134.2, -274.7, 0, 180, 0, 0),
    ]

# How many cranes, and where are they?
CashbotBossCranePosHprs = [
    (97.4, -337.6, 0, -45, 0, 0),
    (97.4, -292.4, 0, -135, 0, 0),
    (142.6, -292.4, 0, 135, 0, 0),
    (142.6, -337.6, 0, 45, 0, 0),
    ]

# How long does it take an object to fly from the ground to the magnet?
CashbotBossToMagnetTime = 0.2

# And how long to straighten out when dropped?
CashbotBossFromMagnetTime = 1

# How much impact does it take to hit the Cashbot boss with an object?
CashbotBossSafeKnockImpact = 0.5
CashbotBossSafeNewImpact = 0.0
CashbotBossGoonImpact = 0.1
CashbotBossKnockoutDamage = 15


# Values used in controlling toon ripples when walking through water
# Value in TT Central
TTWakeWaterHeight = -4.79
# Value in Donald's Dock
DDWakeWaterHeight = 1.669
# Value in Estate (type 1)
EstateWakeWaterHeight = -.3
# Value in Outdoor zone
OZWakeWaterHeight = -0.5
WakeRunDelta = 0.1
WakeWalkDelta = 0.2

# codes sent to setCatalogNotify().
NoItems = 0
NewItems = 1
OldItems = 2

# Values for Suit Invasion news
SuitInvasionBegin = 0
SuitInvasionUpdate = 1
SuitInvasionEnd = 2
SuitInvasionBulletin = 3


# Toon defines now in OTPGlobals


# Holiday name constants
NO_HOLIDAY = 0
JULY4_FIREWORKS = 1
NEWYEARS_FIREWORKS = 2
HALLOWEEN = 3
WINTER_DECORATIONS = 4
SKELECOG_INVASION = 5
MR_HOLLYWOOD_INVASION = 6
FISH_BINGO_NIGHT = 7
ELECTION_PROMOTION = 8
BLACK_CAT_DAY = 9
RESISTANCE_EVENT = 10
KART_RECORD_DAILY_RESET = 11
KART_RECORD_WEEKLY_RESET = 12
TRICK_OR_TREAT = 13
CIRCUIT_RACING = 14
POLAR_PLACE_EVENT = 15
CIRCUIT_RACING_EVENT = 16
TROLLEY_HOLIDAY = 17
TROLLEY_WEEKEND = 18
SILLY_SATURDAY_BINGO = 19
SILLY_SATURDAY_CIRCUIT = 20
SILLY_SATURDAY_TROLLEY = 21
ROAMING_TRIALER_WEEKEND = 22
BOSSCOG_INVASION = 23
MARCH_INVASION = 24
MORE_XP_HOLIDAY = 25
HALLOWEEN_PROPS = 26
HALLOWEEN_COSTUMES = 27
DECEMBER_INVASION = 28
APRIL_FOOLS_COSTUMES = 29
CRASHED_LEADERBOARD = 30


# Japanese Holiday name constants
JULY22_FIREWORKS = 201
JULY23_FIREWORKS = 202
JULY25_FIREWORKS = 203
JULY30_FIREWORKS = 204
JULY31_FIREWORKS = 205
AUGUST1_FIREWORKS = 206
AUGUST3_FIREWORKS = 207
AUGUST5_FIREWORKS = 208
AUGUST7_FIREWORKS = 209
AUGUST8_FIREWORKS = 210
AUGUST10_FIREWORKS = 211
AUGUST13_FIREWORKS = 212
AUGUST14_FIREWORKS = 213
AUGUST16_FIREWORKS = 214
AUGUST31_FIREWORKS = 215

# Brazil Holiday name constants
VALENTINES_FIREWORKS = 1000
BIGWIG_INVASION = 1100
BLOODSUCKER_INVASION = 1101
MOVER_SHAKER_INVASION = 1102
HEAD_HUNTER_INVASION = 1103
THE_MINGLER_INVASION = 1104
MONEY_BAGS_INVASION = 1105
TELEMARKETER_INVASION = 1106
BOTTOMFEEDER_INVASION = 1107
AMBULANCE_CHASER_INVASION = 1108
THE_BIG_CHEESE_INVASION = 1109
NUMBER_CRUNCHER_INVASION = 1110
YESMAN_INVASION = 1111

# German Holiday name constants
OCTOBER31_FIREWORKS = 31
NOVEMBER19_FIREWORKS = 32

# these are holiday invasions, different cog types per number
SELLBOT_SURPRISE_1 = 33
SELLBOT_SURPRISE_2 = 34
SELLBOT_SURPRISE_3 = 35
SELLBOT_SURPRISE_4 = 36
CASHBOT_CONUNDRUM_1 = 37
CASHBOT_CONUNDRUM_2 = 38
CASHBOT_CONUNDRUM_3 = 39
CASHBOT_CONUNDRUM_4 = 40
LAWBOT_GAMBIT_1 = 41
LAWBOT_GAMBIT_2 = 42
LAWBOT_GAMBIT_3 = 43
LAWBOT_GAMBIT_4 = 44
TROUBLE_BOSSBOTS_1 = 45
TROUBLE_BOSSBOTS_2 = 46
TROUBLE_BOSSBOTS_3 = 47
TROUBLE_BOSSBOTS_4 = 48

JELLYBEAN_DAY = 49

# French Holiday name constants
FEBRUARY14_FIREWORKS = 51
JULY14_FIREWORKS = 52
JUNE22_FIREWORKS = 53
BIGWIG_INVASION = 54

# August Weekend Invasion
COLD_CALLER_INVASION = 53
BEAN_COUNTER_INVASION = 54
DOUBLE_TALKER_INVASION = 55
DOWNSIZER_INVASION = 56
WINTER_CAROLING = 57
# Animated Props Holidays
HYDRANT_ZERO_HOLIDAY = 58
VALENTINES_DAY = 59
SILLYMETER_HOLIDAY = 60
# Continuation of animted Prop Holidays
MAILBOX_ZERO_HOLIDAY = 61
TRASHCAN_ZERO_HOLIDAY = 62
SILLY_SURGE_HOLIDAY = 63
HYDRANTS_BUFF_BATTLES = 64
MAILBOXES_BUFF_BATTLES = 65
TRASHCANS_BUFF_BATTLES = 66

SILLY_CHATTER_ONE = 67
SILLY_CHATTER_TWO = 68
SILLY_CHATTER_THREE = 69
SILLY_CHATTER_FOUR = 70

SILLY_TEST = 71

YES_MAN_INVASION = 72
TIGHTWAD_INVASION = 73
TELEMARKETER_INVASION = 74
HEADHUNTER_INVASION = 75
SPINDOCTOR_INVASION = 76
MONEYBAGS_INVASION = 77
TWOFACES_INVASION = 78
MINGLER_INVASION = 79
LOANSHARK_INVASION = 80
CORPORATE_RAIDER_INVASION = 81
ROBBER_BARON_INVASION = 82
LEGAL_EAGLE_INVASION = 83
BIG_WIG_INVASION = 84
BIG_CHEESE_INVASION = 85
DOWN_SIZER_INVASION = 86
MOVER_AND_SHAKER_INVASION = 87
DOUBLETALKER_INVASION = 88
PENNY_PINCHER_INVASION = 89
NAME_DROPPER_INVASION = 90
AMBULANCE_CHASER_INVASION = 91
MICROMANAGER_INVASION = 92
NUMBER_CRUNCHER_INVASION = 93

SILLY_CHATTER_FIVE = 94

VICTORY_PARTY_HOLIDAY = 95

SELLBOT_NERF_HOLIDAY = 96

JELLYBEAN_TROLLEY_HOLIDAY = 97
JELLYBEAN_FISHING_HOLIDAY = 98
JELLYBEAN_PARTIES_HOLIDAY = 99

BANK_UPGRADE_HOLIDAY = 100

TOP_TOONS_MARATHON = 101

SELLBOT_INVASION = 102
SELLBOT_FIELD_OFFICE = 103
SELLBOT_INVASION_MOVER_AND_SHAKER = 104

IDES_OF_MARCH = 105

EXPANDED_CLOSETS = 106

TAX_DAY_INVASION = 107

LAWBOT_NERF_HOLIDAY = 108

KARTING_TICKETS_HOLIDAY = 109

PRE_JULY_4_DOWNSIZER_INVASION = 110
PRE_JULY_4_BIGWIG_INVASION = 111

COMBO_FIREWORKS = 112

JELLYBEAN_TROLLEY_HOLIDAY_MONTH = 113
JELLYBEAN_FISHING_HOLIDAY_MONTH = 114
JELLYBEAN_PARTIES_HOLIDAY_MONTH = 115

SILLYMETER_EXT_HOLIDAY = 116
SPOOKY_BLACK_CAT = 117
SPOOKY_TRICK_OR_TREAT = 118
SPOOKY_PROPS = 119
SPOOKY_COSTUMES = 120
WACKY_WINTER_DECORATIONS = 121
WACKY_WINTER_CAROLING = 122

# Trick or Treat Holiday Values
TOT_REWARD_JELLYBEAN_AMOUNT = 100
TOT_REWARD_END_OFFSET_AMOUNT = 0 # Pumpkins will disappear as soon as the holiday ends
#TOT_REWARD_END_OFFSET_AMOUNT = 60*60*24*7 # a week's worth of seconds to be added to the end time of the holiday


# How many points does it take to kill the Lawbot Boss?
# This will probably represent evidence or gavel points
LawbotBossMaxDamage = 2700

#final scale tilt to indicate a win, in degrees
LawbotBossWinningTilt = 40

# if it becomes 0, the toons have lost the case
LawbotBossInitialDamage = 1350

# Where is the Sellbot Boss sitting in the three stages of the
# VP sequence?
LawbotBossBattleOnePosHpr = (-2.798, -60, 0, 0, 0, 0)

#LawbotBossBattleTwoPosHpr = (50.0,-9, 0, -90, 0, 0)
LawbotBossBattleTwoPosHpr = (-2.798, 89, 19.145,0, 0, 0)


#temp only
# How does the VP roll up the ramp?
LawbotBossTopRampPosA = (-80, -35, 18)
LawbotBossTopRampTurnPosA = (-80, 10, 18)
#LawbotBossP3PosA = (-50, 40, 18)
LawbotBossP3PosA = (55, -9, 0)
LawbotBossTopRampPosB = (80, -35, 18)
LawbotBossTopRampTurnPosB = (80, 10, 18)
#LawbotBossP3PosB = (50, 60, 18)
LawbotBossP3PosB = (55, -9, 0)

#LawbotBossBattleThreeHpr = (180, 0, 0)
#LawbotBossBattleThreePosHpr = (20.5, 152.7, 20,0, 0, 0)
LawbotBossBattleThreePosHpr = LawbotBossBattleTwoPosHpr


LawbotBossBottomPos = (50, 39, 0)
LawbotBossDeathPos = (50, 40, 0)

# How many gavels, and where are they?
LawbotBossGavelPosHprs = [
    (35, 78.328, 0,  -135, 0, 0), #corner near judge far from witness stand
    ( 68.5,  78.328, 0, 135, 0, 0), # corner near witness stand
    (  47,  -33, 0,  45, 0, 0), # corner next nearest witness stand
    ( -50, -39, 0,   -45, 0, 0), # corner diagonally opposite witness stand

    (-9, -37, 0, 0, 0, 0), #along wall opposite judge
    (-9, 49,  0, -180, 0, 0), #along wall near judge
    (32, 0, 0, 45, 0, 0), #opposite witness stand
    (33, 56, 0, 135, 0, 0), #between center of room and witness stand
    ]

#first number is time to go down, 2nd is time to go up, 3rd number is how long it stays down
LawbotBossGavelTimes = [
    (0.20,0.9,0.6),
    (0.25,1, 0.5),
    (1.0,6,0.5),
    (0.3,3,1),

    (0.26,0.9, 0.45),
    (0.24,1.1, 0.65),
    (0.27,1.2, 0.45),
    (0.25,0.95, 0.5),
    ]

#change relative heading where the gavel lands, but give it a pattern so the observant player can predict where it lands
LawbotBossGavelHeadings = [
    (0, -15, 4, -70 -45, 5, 45),
    (0, -45, -4, -35, -45,-16, 32),
    (0, -8, 19, -7, 5, 23),
    (0, -4, 8, -16, 32, -45, 7, 7, -30, 19, -13, 25),

    (0, -45, -90, 45, 90),
    (0, -45, -90, 45, 90),
    (0, -45, 45),
    (0, -45, 45),
    ]


# Where are the Boss Cog's battles relative to him?
LawbotBossCogRelBattleAPosHpr = (-25, -10, 0, 0, 0, 0)
LawbotBossCogRelBattleBPosHpr = (-25, 10, 0, 0, 0, 0)

LawbotBossCogAbsBattleAPosHpr = (-5, -2, 0, 0, 0, 0)
LawbotBossCogAbsBattleBPosHpr = (-5, 0, 0, 0, 0, 0)

LawbotBossWitnessStandPosHpr = (54,100,0,-90,0,0)

LawbotBossInjusticePosHpr = ( -3, 12, 0, 90, 0, 0)
LawbotBossInjusticeScale = (1.75,1.75,1.5)
#LawbotBossInjusticePosHpr = ( 0, 0, 0, 0, 0, 0)

#how much damage does each evidence on the defense pan do
LawbotBossDefensePanDamage = 1

# How many lawyers, and where are they?
LawbotBossLawyerPosHprs = [
    (-57, -24, 0, -90, 0, 0),
    (-57, -12, 0, -90, 0, 0),
    (-57,   0, 0, -90, 0, 0),
    (-57,  12, 0, -90, 0, 0),
    (-57,  24, 0, -90, 0, 0),
    (-57,  36, 0, -90, 0, 0),
    (-57,  48, 0, -90, 0, 0),
    (-57,  60, 0, -90, 0, 0),
    (-3, -37.3, 0,  0, 0, 0),
    (-3, 53, 0, -180, 0, 0),
    ]

#how many seconds to wait till we attack or prosecute again
LawbotBossLawyerCycleTime = 6

#how many seconds does it take for evidence to fly from lawyers to prosecution
LawbotBossLawyerToPanTime = 2.5

#chance for the lawyers to do an attack (throw evidence at the toons)
LawbotBossLawyerChanceToAttack = 50

#when the lawyers throw stuff on the prosecution pan, how much damage to heal the boss
LawbotBossLawyerHeal = 2

#how many seconds do lawyers get stunned when we hit them
LawbotBossLawyerStunTime =5

#ammo count, how many gavels, how many lawyers, how much toonup, do jurors influence evidence weight, cog bonus subtractor (e.g. if this value is 1 and you seated 2 jurors), 2-1 leads to 1 as your bonus weight
LawbotBossDifficultySettings = [
    (38, 4,  8, 1, 0, 0),
    (36, 5,  8, 1, 0, 0),
    (34, 5,  8, 1, 0, 0),
    (32, 6,  8, 2, 0, 0),
    (30, 6,  8, 2, 0, 0),
    (28, 7,  8, 3, 0, 0),
    (26, 7,  9, 3, 1, 1),
    (24, 8,  9, 4, 1, 1),
    (22, 8, 10, 4, 1, 0),
    ]

#where are the cannons and how many are they
LawbotBossCannonPosHprs = [
    (-40, -12, 0, -90, 0, 0),
    (-40,   0, 0, -90, 0, 0),
    (-40,  12, 0, -90, 0, 0),
    (-40,  24, 0, -90, 0, 0),
    (-40,  36, 0, -90, 0, 0),
    (-40,  48, 0, -90, 0, 0),
    (-40,  60, 0, -90, 0, 0),
    (-40,  72, 0, -90, 0, 0),
    ]


LawbotBossCannonPosA = (-80, -51.48, 0)
LawbotBossCannonPosB = (-80, 70.73, 0)

#where are the juror chairs and how many are they
LawbotBossChairPosHprs = [
    (60,  72, 0, -90, 0, 0),
    (60,  62, 0, -90, 0, 0),
    (60,  52, 0, -90, 0, 0),
    (60,  42, 0, -90, 0, 0),
    (60,  32, 0, -90, 0, 0),
    (60,  22, 0, -90, 0, 0),

    (70,  72, 5, -90, 0, 0),
    (70,  62, 5, -90, 0, 0),
    (70,  52, 5, -90, 0, 0),
    (70,  42, 5, -90, 0, 0),
    (70,  32, 5, -90, 0, 0),
    (70,  22, 5, -90, 0, 0),

    ]

LawbotBossChairRow1PosB = (59.3, 48, 14.05)
LawbotBossChairRow1PosA = (59.3, -18.2, 14.05)
LawbotBossChairRow2PosB = (75.1, 48, 28.2)
LawbotBossChairRow2PosA = (75.1, -18.2, 28.2)

#how many cannon balls can each toon fire
LawbotBossCannonBallMax = 12

#jury box info
LawbotBossJuryBoxStartPos = (94,  -8, 5)
LawbotBossJuryBoxRelativeEndPos = (30,0,12.645)
LawbotBossJuryBoxMoveTime = 70

LawbotBossJurorsForBalancedScale = 8
LawbotBossDamagePerJuror = 68

LawbotBossCogJurorFlightTime = 10
LawbotBossCogJurorDistance = 75

#starting toon in cannon is Flippy at 2001
LawbotBossBaseJurorNpcId = 2001

LawbotBossWitnessEpiloguePosHpr = ( -3, 0, 0, 180, 0, 0)

LawbotBossChanceForTaunt = 25

#how long to wait before you can get  bonus state again
LawbotBossBonusWaitTime = 60
#how long does the bonus state last
LawbotBossBonusDuration = 20
#how much of a toonup to give when they reach the bonus state
LawbotBossBonusToonup = 10
#multiplier on defense evidence
LawbotBossBonusWeightMultiplier = 2

#spice it up they say, give the CJ a chance to do the area attack
LawbotBossChanceToDoAreaAttack = 11

# shard population limits
LOW_POP_JP = 0
MID_POP_JP = 100
HIGH_POP_JP = 200

LOW_POP_INTL = 399
MID_POP_INTL = 499
HIGH_POP_INTL = -1

LOW_POP = 399
MID_POP = 599
HIGH_POP = -1

# Cannon pinball stuff

PinballCannonBumper = 0
PinballCloudBumperLow = 1
PinballCloudBumperMed = 2
PinballCloudBumperHigh = 3
PinballTarget = 4
PinballRoof = 5
PinballHouse =6
PinballFence = 7
PinballBridge = 8
PinballStatuary = 9

#first number adds to score, 2nd number adds to multiplier
PinballScoring = [
    (100,1), #Cannon Bumper
    (150,1), #Low cloud bumpers
    (200,1), #medium cloud bumpers
    (250,1), #high cloud bumpers
    (350,1), #target
    (100,1), #roof
    (50,1),  #house
    (25,1), #fence
    (100,1), #bridge
    (10,1) #planted statuary items
    ]

PinballCannonBumperInitialPos = (0,-20,40)

#rental types
RentalCop = 0
RentalCannon = 1
RentalGameTable = 2

#glichkiller zone list
GlitchKillerZones = [13300, 13400, 13500, 13600]

#colors for the friends list panel
#could be a ColorCode in Name Tag groups
#but maybe all those should really be in script anyway

ColorPlayer = (0.3, 0.7, 0.3, 1)
ColorAvatar = (0.3, 0.3, 0.7, 1)
ColorPet    = (0.6, 0.4, 0.2, 1)

ColorFreeChat  = (0.3, 0.3, 0.8, 1)
ColorSpeedChat = (0.2, 0.6, 0.4, 1)
ColorNoChat    = (0.8, 0.5, 0.1, 1)

# Factory elevator laff point minimums

FactoryLaffMinimums = [
    # sellbot
    (0, 31),
    # cashbot
    (0, 66, 71),
    # lawbot
    (0, 81, 86, 96),
    # bossbot
    (0, 101, 106),
    ]

# Picnic table sitting ime
PICNIC_COUNTDOWN_TIME = 60

# CEO Battle stuff
BossbotRTIntroStartPosHpr = (0, -64, 0, 180, 0, 0)
BossbotRTPreTwoPosHpr = (0, -20, 0, 180, 0, 0)
BossbotRTEpiloguePosHpr = ( 0, 90, 0, 180, 0, 0)
BossbotBossBattleOnePosHpr = (0, 355, 0, 0, 0, 0)
BossbotBossPreTwoPosHpr = (0, 20, 0, 0, 0, 0)
BossbotElevCamPosHpr  = (0,  -100.544,  7.18258, 0, 0, 0)
BossbotFoodModelScale = 0.75 # do we scale up or down from the cog food model
BossbotNumFoodToExplode = 3
BossbotBossServingDuration = 300
BossbotPrepareBattleThreeDuration = 20
# relative to bosscog coordinates for waiter battles
WaiterBattleAPosHpr = (20, -400, 0, 0, 0, 0)
WaiterBattleBPosHpr = (-20, -400, 0, 0, 0, 0)
BossbotBossBattleThreePosHpr = (0, 355, 0, 0, 0, 0)
DinerBattleAPosHpr = (20, -240, 0, 0, 0, 0)
DinerBattleBPosHpr = (-20, -240, 0, 0, 0, 0)
BossbotBossMaxDamage = 500
BossbotMaxSpeedDamage = 90
BossbotSpeedRecoverRate = 20 # in speed damage recovered per MINUTE
# num tables, diners per table, level of diners, table unflatten time, hungry duration, eating duration
BossbotBossDifficultySettings = [
    (8, 4, 11, 3,   30, 25),
    (9, 5, 12, 6,   28, 26),
    (10, 6, 11, 7,  26, 27),
    (8, 8, 12, 8, 24, 28),
    (13, 5, 12, 9, 22, 29),
    ]
#BossbotRollSpeedMax = 15
BossbotRollSpeedMax = 22
#BossbotRollSpeedMin = 3.75
BossbotRollSpeedMin = 7.5
#BossbotTurnSpeedMax = 40
BossbotTurnSpeedMax = 60
#BossbotTurnSpeedMin = 10
BossbotTurnSpeedMin = 20
#BossbotTreadSpeedMax = 7
BossbotTreadSpeedMax = 10.5
#BossbotTreadSpeedMin = 1.75
BossbotTreadSpeedMin = 3.5


# Calendar Stuff
CalendarFilterShowAll = 0
CalendarFilterShowOnlyHolidays = 1
CalendarFilterShowOnlyParties = 2

# Hood identifiers
TTC = 1
DD = 2
MM = 3
GS = 4
DG = 5
BR = 6
OZ = 7
DL = 8

# NewsPage stuff
DefaultWantNewsPageSetting = 1

# GM magic words
gmMagicWordList = [
    "restock",  "restockUber",  "autoRestock",
    "resistanceRestock", "restockSummons",
    "uberDrop", "rich", "maxBankMoney",
    "toonUp", "rod", "cogPageFull", "pinkSlips",
    "Tickets",  "newSummons", "who",  "who all"
 ]

NewsPageScaleAdjust = 0.85
# Prop types for the new animating props
AnimPropTypes = Enum(("Unknown",
                      "Hydrant",
                      "Mailbox",
                      "Trashcan",
                      ),
                     start = -1
                     )

# Cogdo Reward Emblems
EmblemTypes = Enum(("Silver", "Gold"))
NumEmblemTypes = 2

# Max Bank Update
DefaultMaxBankMoney = 12000
DefaultBankItemId = 1350

# This is the tuple of allowed animations that can be set by using toon.setAnimState().
# If you add an animation that you want to do a setAnimState on please add this
# animation to this list.
ToonAnimStates = set([
    "off",
    "neutral",
    "victory",
    "Happy",
    "Sad",
    "Catching",
    "CatchEating",
    "Sleep",
    "walk",
    "jumpSquat",
    "jump",
    "jumpAirborne",
    "jumpLand",
    "run",
    "swim",
    "swimhold",
    "dive",
    "cringe",
    "OpenBook",
    "ReadBook",
    "CloseBook",
    "TeleportOut",
    "Died",
    "TeleportedOut",
    "TeleportIn",
    "Emote",
    "SitStart",
    "Sit",
    "Push",
    "Squish",
    "FallDown",
    "GolfPuttLoop",
    "GolfRotateLeft",
    "GolfRotateRight",
    "GolfPuttSwing",
    "GolfGoodPutt",
    "GolfBadPutt",
    "Flattened",
    "CogThiefRunning",
    "ScientistJealous",
    "ScientistEmcee",
    "ScientistWork",
    "ScientistLessWork",
    "ScientistPlay",
    ]
   )

# Avatar Colliding Values
AV_FLAG_REASON_TOUCH = 1
AV_FLAG_HISTORY_LEN = 500
AV_TOUCH_CHECK_DELAY_AI = 3.0
AV_TOUCH_CHECK_DELAY_CL = 1.0
AV_TOUCH_CHECK_DIST = 2.0
AV_TOUCH_CHECK_DIST_Z = 5.0
AV_TOUCH_CHECK_TIMELIMIT_CL = 0.002
AV_TOUCH_COUNT_LIMIT = 5
AV_TOUCH_COUNT_TIME = 300
