from toontown.toonbase.ToontownModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from toontown.toon import GroupInvitee
from toontown.toon import GroupPanel
from toontown.toon import BoardingGroupInviterPanels
from toontown.building import BoardingPartyBase
from direct.gui.DirectGui import *
from toontown.toontowngui import TTDialog
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel
from direct.interval.IntervalGlobal import *
from . import BoardingGroupShow

class DistributedBoardingParty(DistributedObject.DistributedObject, BoardingPartyBase.BoardingPartyBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBoardingParty')

    # This is the length of time that should elapse before we allow
    # another InvitationFailed message to be displayed from the same avatar.
    InvitationFailedTimeout = 60.0

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        BoardingPartyBase.BoardingPartyBase.__init__(self)
        if __debug__:
            base.bparty = self
        self.groupInviteePanel = None
        self.groupPanel = None
        self.inviterPanels = BoardingGroupInviterPanels.BoardingGroupInviterPanels()
        self.lastInvitationFailedMessage = {} #key->avatarId : time
        self.goToPreShowTrack = None
        self.goToShowTrack = None

    def generate(self):
        self.load()
        DistributedObject.DistributedObject.generate(self)
        localAvatar.boardingParty = self

    def announceGenerate(self):
        canonicalZoneId = ZoneUtil.getCanonicalZoneId(self.zoneId)
        self.notify.debug('canonicalZoneId = %s' %canonicalZoneId)
        localAvatar.chatMgr.chatInputSpeedChat.addBoardingGroupMenu(canonicalZoneId)

        #REMOVE THIS from here and put it in the right place:
        if ConfigVariableBool('want-singing', 0).getValue():
            localAvatar.chatMgr.chatInputSpeedChat.addSingingGroupMenu()

    def delete(self):
        DistributedObject.DistributedObject.delete(self)

    def disable(self):
        #self.demandDrop()
        self.finishGoToPreShowTrack()
        self.finishGoToShowTrack()
        self.forceCleanupInviteePanel()
        self.forceCleanupInviterPanels()
        self.inviterPanels = None
        if self.groupPanel:
            self.groupPanel.cleanup()
        self.groupPanel = None
        DistributedObject.DistributedObject.disable(self)
        BoardingPartyBase.BoardingPartyBase.cleanup(self)
        localAvatar.boardingParty = None
        localAvatar.chatMgr.chatInputSpeedChat.removeBoardingGroupMenu()
        self.lastInvitationFailedMessage = {}

    def getElevatorIdList(self):
        return self.elevatorIdList

    def setElevatorIdList(self, elevatorIdList):
        self.notify.debug("setElevatorIdList")
        self.elevatorIdList = elevatorIdList

    def load(self):
        """
        Load any assets here if required.
        """
        pass

    def postGroupInfo(self, leaderId, memberList, inviteeList, kickedList):
        """
        A group has changed so the AI is sending us new information on it
        """
        self.notify.debug("postgroupInfo")
        isMyGroup = 0
        removedMemberIdList = []
        if leaderId in self.groupListDict:
            oldGroupEntry = self.groupListDict[leaderId]
        else:
            oldGroupEntry = [[],[],[]]
        oldMemberList = oldGroupEntry[0]

        newGroupEntry = [memberList, inviteeList, kickedList]
        self.groupListDict[leaderId] = newGroupEntry

        # Comb the avIdDict if there is a change in the number of members in the group.
        # Remove any avId that has left the group or has been kicked out.
        if not (len(oldMemberList) == len(memberList)):
            for oldMember in oldMemberList:
                if not oldMember in memberList:
                    # This member has been removed.
                    if oldMember in self.avIdDict:
                        # Remove this member from the avIdDict ONLY if we doesn't have a different leader.
                        # This means he hasn't joined a different group.
                        if (self.avIdDict[oldMember] == leaderId):
                            self.avIdDict.pop(oldMember)
                            removedMemberIdList.append(oldMember)

        self.avIdDict[leaderId] = leaderId
        if leaderId == localAvatar.doId:
            isMyGroup = 1
        for memberId in memberList:
            self.avIdDict[memberId] = leaderId
            if memberId == localAvatar.doId:
                isMyGroup = 1

        if (newGroupEntry[0]) == [0] or (not newGroupEntry[0]): # if the new memberList is empty
            dgroup = self.groupListDict.pop(leaderId)
            for memberId in dgroup[0]:
                if memberId in self.avIdDict:
                    self.avIdDict.pop(memberId)

        if isMyGroup:
            self.notify.debug("new info posted on my group")
            if not self.groupPanel:
                self.groupPanel = GroupPanel.GroupPanel(self)
            messenger.send('updateGroupStatus')
            for removedMemberId in removedMemberIdList:
                removedMember = base.cr.doId2do.get(removedMemberId)
                # Send the message to the members only if you can find the removedMember.
                # This means that this would work only if the removedMember left the
                # group using the leave button. It won't work if the removedMember Alt+F4ed out.
                if not removedMember:
                    # Try second time, just in case removedMemberId is a friend.
                    removedMember = base.cr.identifyFriend(removedMemberId)
                if removedMember:
                    removedMemberName = removedMember._name
                    # Message to the members in the group that the removedMember has left the Boarding Group.
                    messageText = TTLocalizer.BoardingMessageLeftGroup %(removedMemberName)
                    localAvatar.setSystemMessage(0, messageText, WhisperPopup.WTToontownBoardingGroup)

        elif (localAvatar.doId in oldMemberList) and not (localAvatar.doId in memberList):
            # localAvatar's doId was there in the old list but is not there in the new list
            # This must mean that he has either left the group or kicked out.
            messenger.send('updateGroupStatus')
			# Cleanup the GroupPanel.
            if self.groupPanel:
                self.groupPanel.cleanup()
            self.groupPanel = None
        else:
            self.notify.debug("new info posted on some other group")

    def postInvite(self, leaderId, inviterId):
        """
        The AI tells us someone has been invited into a group
        """
        self.notify.debug("post Invite")
        if not base.cr.avatarFriendsManager.checkIgnored(inviterId):
            inviter = base.cr.doId2do.get(inviterId)
            if inviter:
                if self.inviterPanels.isInvitingPanelUp() or self.inviterPanels.isInvitationRejectedPanelUp():
                    self.inviterPanels.forceCleanup()
                self.groupInviteePanel = GroupInvitee.GroupInvitee()
                self.groupInviteePanel.make(self, inviter, leaderId)
                if ConfigVariableBool('reject-boarding-group-invites', 0).getValue():
                    self.groupInviteePanel.forceCleanup()
                    self.groupInviteePanel = None

    def postKick(self, leaderId):
        self.notify.debug("%s was kicked out of the Boarding Group by %s" % (localAvatar.doId, leaderId))
        # Message to the kicked player that the leader kicked him out.
        localAvatar.setSystemMessage(0, TTLocalizer.BoardingMessageKickedOut, WhisperPopup.WTToontownBoardingGroup)

    def postSizeReject(self, leaderId, inviterId, inviteeId):
        self.notify.debug("%s was not invited because the group is full" % (inviteeId))

    def postKickReject(self, leaderId, inviterId, inviteeId):
        self.notify.debug("%s was not invited because %s has kicked them from the group" % (inviteeId, leaderId))

    def postInviteDelcined(self, inviteeId):
        self.notify.debug("%s delinced %s's Boarding Group invitation." %(inviteeId, localAvatar.doId))
        # Show Boarding Group Invitation Rejected Panel
        invitee = base.cr.doId2do.get(inviteeId)
        if invitee:
            self.inviterPanels.createInvitationRejectedPanel(self, inviteeId)

    def postInviteAccepted(self, inviteeId):
        self.notify.debug("%s accepted %s's Boarding Group invitation." %(inviteeId, localAvatar.doId))
        # Remove the Boarding Group Inviting Panel if it has the same inviteeId
        if self.inviterPanels.isInvitingPanelIdCorrect(inviteeId):
            self.inviterPanels.destroyInvitingPanel()

    def postInviteCanceled(self):
        self.notify.debug("The invitation to the Boarding Group was cancelled")
        # Remove the Boarding Group Invitation Panel
        if self.isInviteePanelUp():
            self.groupInviteePanel.cleanup()
            self.groupInviteePanel = None

    def postInviteNotQualify(self, avId, reason, elevatorId):
        messenger.send('updateGroupStatus')
        rejectText = ''
        minLaff = TTLocalizer.BoardingMore

        if elevatorId:
            elevator = base.cr.doId2do.get(elevatorId)
            if elevator:
                minLaff = elevator.minLaff

        if (avId == localAvatar.doId):
            if (reason == BoardingPartyBase.BOARDCODE_MINLAFF):
                rejectText = TTLocalizer.BoardingInviteMinLaffInviter %(minLaff)
            if (reason == BoardingPartyBase.BOARDCODE_PROMOTION):
                rejectText = TTLocalizer.BoardingInvitePromotionInviter
        else:
            avatar = base.cr.doId2do.get(avId)
            if avatar:
                avatarNameText = avatar._name
            else:
                avatarNameText = ''
            if (reason == BoardingPartyBase.BOARDCODE_MINLAFF):
                rejectText = TTLocalizer.BoardingInviteMinLaffInvitee %(avatarNameText, minLaff)
            if (reason == BoardingPartyBase.BOARDCODE_PROMOTION):
                rejectText = TTLocalizer.BoardingInvitePromotionInvitee %(avatarNameText)
            if (reason == BoardingPartyBase.BOARDCODE_BATTLE):
                rejectText = TTLocalizer.TeleportPanelNotAvailable %(avatarNameText)
            if (reason == BoardingPartyBase.BOARDCODE_NOT_PAID):
                rejectText = TTLocalizer.BoardingInviteNotPaidInvitee %(avatarNameText)
            if (reason == BoardingPartyBase.BOARDCODE_DIFF_GROUP):
                rejectText = TTLocalizer.BoardingInviteeInDiffGroup %(avatarNameText)
            if (reason == BoardingPartyBase.BOARDCODE_PENDING_INVITE):
                rejectText = TTLocalizer.BoardingInviteePendingIvite %(avatarNameText)
            if (reason == BoardingPartyBase.BOARDCODE_IN_ELEVATOR):
                rejectText = TTLocalizer.BoardingInviteeInElevator %(avatarNameText)
        if self.inviterPanels.isInvitingPanelIdCorrect(avId) or (avId == localAvatar.doId):
            self.inviterPanels.destroyInvitingPanel()
        self.showMe(rejectText)

    def postAlreadyInGroup(self):
        """
        The invitee is already part of a group and cannot accept another invitation.
        """
        self.showMe(TTLocalizer.BoardingAlreadyInGroup)

    def postGroupAlreadyFull(self):
        """
        The invitee cannot accept the invitation because the group is already full.
        """
        self.showMe(TTLocalizer.BoardingGroupAlreadyFull)

    def postSomethingMissing(self):
        """
        The AI determines that something is wrong and this cannot be accepted.
        Eg 1: The leader of the group is not there in the avIdDict.
        """
        self.showMe(TTLocalizer.BoardcodeMissing)

    def postRejectBoard(self, elevatorId, reason, avatarsFailingRequirements, avatarsInBattle):
        """
        Problem when the leader tried to enter the elevator detected on AI
        """
        self.showRejectMessage(elevatorId, reason, avatarsFailingRequirements, avatarsInBattle)
        # Enable the Group Panel GO Button here.
        self.enableGoButton()

    def postRejectGoto(self, elevatorId, reason, avatarsFailingRequirements, avatarsInBattle):
        """
        Problem when the leader tried to use a GO Button detected on AI.
        """
        self.showRejectMessage(elevatorId, reason, avatarsFailingRequirements, avatarsInBattle)

    def postMessageInvited(self, inviteeId, inviterId):
        """
        The AI tells all the members (except the inviter) in the Boarding Group that
        the inviter has invited the invitee.
        """
        inviterName = ''
        inviteeName = ''
        inviter = base.cr.doId2do.get(inviterId)
        if inviter:
            inviterName = inviter._name
        invitee = base.cr.doId2do.get(inviteeId)
        if invitee:
            inviteeName = invitee._name
        # Message to the members in the group that the inviter has invited the invitee.
        messageText = TTLocalizer.BoardingMessageInvited %(inviterName, inviteeName)
        localAvatar.setSystemMessage(0, messageText, WhisperPopup.WTToontownBoardingGroup)

    def postMessageInvitationFailed(self, inviterId):
        """
        The AI tells the invitee that an inviter had tried to invite him to their
        Boarding Group, but failed for some reason.
        """
        inviterName = ''
        inviter = base.cr.doId2do.get(inviterId)
        if inviter:
            inviterName = inviter._name
        # Don't generate the message more than once a minute, so that the inviter can't spam the invitee.
        if self.invitationFailedMessageOk(inviterId):
            # Message to the invitee that the inviter had tried to invite the invitee.
            messageText = TTLocalizer.BoardingMessageInvitationFailed %(inviterName)
            localAvatar.setSystemMessage(0, messageText, WhisperPopup.WTToontownBoardingGroup)

    def postMessageAcceptanceFailed(self, inviteeId, reason):
        '''
        The AI tells the inviter that the invitee tried to accept the invitation
        because of the following reason.
        '''
        inviteeName = ''
        messageText = ''
        invitee = base.cr.doId2do.get(inviteeId)
        if invitee:
            inviteeName = invitee._name

        if (reason == BoardingPartyBase.INVITE_ACCEPT_FAIL_GROUP_FULL):
            messageText = TTLocalizer.BoardingMessageGroupFull %inviteeName

        # Message to the inviter that the invitee failed to accept the invitation.
        localAvatar.setSystemMessage(0, messageText, WhisperPopup.WTToontownBoardingGroup)

        # Remove the Boarding Group Inviting Panel if it has the same inviteeId
        if self.inviterPanels.isInvitingPanelIdCorrect(inviteeId):
            self.inviterPanels.destroyInvitingPanel()

    def invitationFailedMessageOk(self, inviterId):
        """
        Returns True if it is OK to display this message from this inviter.
        Returns False if this message should be suppressed because we just
        recently displaced this message from this inviter.
        This check is added so that the inviter can't spam the invitee.
        """
        now = globalClock.getFrameTime()
        lastTime = self.lastInvitationFailedMessage.get(inviterId, None)
        if lastTime:
            elapsedTime = now - lastTime
            if elapsedTime < self.InvitationFailedTimeout:
                return False

        self.lastInvitationFailedMessage[inviterId] = now
        return True

    def showRejectMessage(self, elevatorId, reason, avatarsFailingRequirements, avatarsInBattle):
        leaderId = localAvatar.doId
        rejectText = ''
        def getAvatarText(avIdList):
            """
            This function takes a list of avIds and returns a string of names.
            If there is only 1 person it returns "avatarOneName"
            If there are 2 people it returns "avatarOneName and avatarTwoName"
            If there are 3 or more people it returns "avatarOneName,  avatarTwoName and avatarThreeName"
            """
            avatarText = ''
            nameList = []
            for avId in avIdList:
                avatar = base.cr.doId2do.get(avId)
                if avatar:
                    nameList.append(avatar._name)
            if (len(nameList) > 0):
                lastName = nameList.pop()
                avatarText = lastName
                if (len(nameList) > 0):
                    secondLastName = nameList.pop()
                    for name in nameList:
                        avatarText = name + ', '
                    avatarText += secondLastName + ' ' + TTLocalizer.And + ' ' + lastName
            return avatarText

        if (reason == BoardingPartyBase.BOARDCODE_MINLAFF):
            self.notify.debug("%s 's group cannot board because it does not have enough laff points." % (leaderId))

            elevator = base.cr.doId2do.get(elevatorId)
            if elevator:
                minLaffPoints = elevator.minLaff
            else:
                minLaffPoints = TTLocalizer.BoardingMore

            if (leaderId in avatarsFailingRequirements):
                rejectText = TTLocalizer.BoardcodeMinLaffLeader %(minLaffPoints)
            else:
                avatarNameText = getAvatarText(avatarsFailingRequirements)
                if (len(avatarsFailingRequirements) == 1):
                    rejectText = TTLocalizer.BoardcodeMinLaffNonLeaderSingular %(avatarNameText, minLaffPoints)
                else:
                    rejectText = TTLocalizer.BoardcodeMinLaffNonLeaderPlural %(avatarNameText, minLaffPoints)

        elif (reason == BoardingPartyBase.BOARDCODE_PROMOTION):
            self.notify.debug("%s 's group cannot board because it does not have enough promotion merits." % (leaderId))
            if (leaderId in avatarsFailingRequirements):
                rejectText = TTLocalizer.BoardcodePromotionLeader
            else:
                avatarNameText = getAvatarText(avatarsFailingRequirements)
                if (len(avatarsFailingRequirements) == 1):
                    rejectText = TTLocalizer.BoardcodePromotionNonLeaderSingular %(avatarNameText)
                else:
                    rejectText = TTLocalizer.BoardcodePromotionNonLeaderPlural %(avatarNameText)

        elif (reason == BoardingPartyBase.BOARDCODE_BATTLE):
            self.notify.debug("%s 's group cannot board because it is in a battle" % (leaderId))
            if (leaderId in avatarsInBattle):
                rejectText = TTLocalizer.BoardcodeBattleLeader
            else:
                avatarNameText = getAvatarText(avatarsInBattle)
                if (len(avatarsInBattle) == 1):
                    rejectText = TTLocalizer.BoardcodeBattleNonLeaderSingular %(avatarNameText)
                else:
                    rejectText = TTLocalizer.BoardcodeBattleNonLeaderPlural %(avatarNameText)

        elif (reason == BoardingPartyBase.BOARDCODE_SPACE):
            self.notify.debug("%s 's group cannot board there was not enough room" % (leaderId))
            rejectText = TTLocalizer.BoardcodeSpace

        elif (reason == BoardingPartyBase.BOARDCODE_MISSING):
            self.notify.debug("%s 's group cannot board because something was missing" % (leaderId))
            rejectText = TTLocalizer.BoardcodeMissing
        base.localAvatar.elevatorNotifier.showMe(rejectText)

    def postGroupDissolve(self, quitterId, leaderId, memberList, kick):
        self.notify.debug("%s group has dissolved" % (leaderId))

        isMyGroup = 0
        if (localAvatar.doId == quitterId) or (localAvatar.doId == leaderId):
            isMyGroup = 1
        if leaderId in self.groupListDict:
            if leaderId == localAvatar.doId:
                isMyGroup = 1
                if leaderId in self.avIdDict:
                    self.avIdDict.pop(leaderId)
            dgroup = self.groupListDict.pop(leaderId)

            for memberId in memberList:
                if memberId == localAvatar.doId:
                    isMyGroup = 1
                if memberId in self.avIdDict:
                    self.avIdDict.pop(memberId)

        if isMyGroup:
            self.notify.debug("new info posted on my group")
            messenger.send('updateGroupStatus')
            groupFormed = False
            if self.groupPanel:
                groupFormed = True
                self.groupPanel.cleanup()
            self.groupPanel = None

            # Cheap Hack: If the group panel was not there, I'm assuming that the group
            # wasn't formed. So don't show any of the whisper messages.
            if groupFormed:
                # We can get here in 2 ways:
                #   leader has disbanded the group OR
                #   non-leader(quitterId) has left a 2 member group.
                # If the leader is the quitter.
                if (leaderId == quitterId):
                    # Don't message the leader because he already knows.
                    if not (localAvatar.doId == leaderId):
                        # Message to the members in the group that the group was dissolved by the leader.
                        localAvatar.setSystemMessage(0, TTLocalizer.BoardingMessageGroupDissolved, WhisperPopup.WTToontownBoardingGroup)
                # If the non-leader is the quitter.
                else:
                    # kick = 1 means leader kicked out the quitter. Don't show any message to the leader.
                    if not kick:
                        # Don't message the quitter because he already knows.
                        if not (localAvatar.doId == quitterId):
                            quitter = base.cr.doId2do.get(quitterId)
                            if quitter:
                                # If we can find the quitter, message saying quitter has left the group.
                                quitterName = quitter._name
                                # Message to the members in the group that the quitter has left the Boarding Group.
                                messageText = TTLocalizer.BoardingMessageLeftGroup %(quitterName)
                                localAvatar.setSystemMessage(0, messageText, WhisperPopup.WTToontownBoardingGroup)
                            else:
                                # If we can't find the quitter write a generic message saying your group was disbanded.
                                messageText = TTLocalizer.BoardingMessageGroupDisbandedGeneric
                                localAvatar.setSystemMessage(0, messageText, WhisperPopup.WTToontownBoardingGroup)

    def requestInvite(self, inviteeId):
        self.notify.debug("requestInvite %s" % (inviteeId))
        # Check for trial toon
        elevator = base.cr.doId2do.get(self.getElevatorIdList()[0])
        if elevator:
            if elevator.allowedToEnter():
                # Check if the inviteeId is in the kick out list
                if inviteeId in self.getGroupKickList(localAvatar.doId):
                    if not self.isGroupLeader(localAvatar.doId):
                        # You cannot invite a toon if he is in the kick out list
                        # and if you are not the group leader
                        avatar = base.cr.doId2do.get(inviteeId)
                        if avatar:
                            avatarNameText = avatar._name
                        else:
                            avatarNameText = ''
                        rejectText = TTLocalizer.BoardingInviteeInKickOutList %(avatarNameText)
                        self.showMe(rejectText)
                        return

                # Check if any Boarding Group Inviting Panel is up
                if self.inviterPanels.isInvitingPanelUp():
                    self.showMe(TTLocalizer.BoardingPendingInvite, pos = (0, 0, 0))
                elif (len(self.getGroupMemberList(localAvatar.doId)) >= self.maxSize):
                    # The Boarding Group is full, so you can't send any more invites.
                    self.showMe(TTLocalizer.BoardingInviteGroupFull)
                else:
                    # Show BoardingGroupInviter panel
                    invitee = base.cr.doId2do.get(inviteeId)
                    if invitee:
                        self.inviterPanels.createInvitingPanel(self, inviteeId)
                        # TODO: Add invitee to the groupListDict
                        # Sending the invite
                        self.sendUpdate("requestInvite", [inviteeId])
            else:
                place = base.cr.playGame.getPlace()
                if place:
                    place.fsm.request('stopped')
                self.teaserDialog = TeaserPanel.TeaserPanel(pageName='cogHQ', doneFunc = self.handleOkTeaser)

    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.teaserDialog.destroy()
        del self.teaserDialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def requestCancelInvite(self, inviteeId):
        self.sendUpdate("requestCancelInvite", [inviteeId])

    def requestAcceptInvite(self, leaderId, inviterId):
        self.notify.debug("requestAcceptInvite %s %s" % (leaderId, inviterId))
        self.sendUpdate("requestAcceptInvite", [leaderId, inviterId])

    def requestRejectInvite(self, leaderId, inviterId):
        self.sendUpdate("requestRejectInvite", [leaderId, inviterId])

    def requestKick(self, kickId):
        self.sendUpdate("requestKick", [kickId])

    def requestLeave(self):
        # Don't request to leave if the toon is doing the goToShowTrack.
        if self.goToShowTrack and self.goToShowTrack.isPlaying():
            return

        # Don't request to leave if the toon is already in the elevator.
        place = base.cr.playGame.getPlace()
        if place:
            if not (place.getState() == 'elevator'):
                if localAvatar.doId in self.avIdDict:
                    leaderId = self.avIdDict[localAvatar.doId]
                    self.sendUpdate("requestLeave", [leaderId])

    def handleEnterElevator(self, elevator):
        """
        If you are the leader of the boarding group, do it the boarding group way.
        We come into this function only if the player is the leader of the boarding group.
        """
        if self.getGroupLeader(localAvatar.doId) == localAvatar.doId:
            if base.localAvatar.hp > 0:
                # Put localToon into requestBoard mode.
                self.cr.playGame.getPlace().detectedElevatorCollision(elevator)
                self.sendUpdate("requestBoard", [elevator.doId])
                # Change the destination name on everybody's GroupPanel
                elevatorId = elevator.doId
                if elevatorId in self.elevatorIdList:
                    offset = self.elevatorIdList.index(elevatorId)
                    if self.groupPanel:
                        self.groupPanel.scrollToDestination(offset)
                    self.informDestChange(offset)
                # Disable the Group Panel GO Button and Destination Scrolled List here.
                self.disableGoButton()

    def informDestChange(self, offset):
        """
        This function is called from Group Panel when the leader changes the destination.
        """
        self.sendUpdate('informDestinationInfo', [offset])

    def postDestinationInfo(self, offset):
        """
        The destination has been changed by the leader. Change the GroupPanel of
        this client to reflect the change.
        """
        if self.groupPanel:
            self.groupPanel.changeDestination(offset)

    def enableGoButton(self):
        """
        Enables the GO Button in the Group Panel.
        """
        if self.groupPanel:
            self.groupPanel.enableGoButton()
            self.groupPanel.enableDestinationScrolledList()

    def disableGoButton(self):
        """
        Disables the GO Button in the Group Panel.
        """
        if self.groupPanel:
            self.groupPanel.disableGoButton()
            self.groupPanel.disableDestinationScrolledList()

    def isInviteePanelUp(self):
        """
        Helper function to determine whether any Group Invitee panel is up or not.
        """
        if self.groupInviteePanel:
            if not self.groupInviteePanel.isEmpty():
                return True
            self.groupInviteePanel = None
        return False

    def requestGoToFirstTime(self, elevatorId):
        """
        Request the AI if the leader and all the members can go directly to the elevator destination.
        This is the first request the leader makes to the AI.
        The AI responds back only to the leader with a rejectGoToRequest if anything goes wrong or
        responds back only to the leader with a acceptGoToFirstTime if everything goes well.
        """
        self.waitingForFirstResponse = True
        self.firstRequestAccepted = False
        self.sendUpdate("requestGoToFirstTime", [elevatorId])
        # Start the Go To pre show immediately, we'll stop it if we hear a reject from the AI.
        self.startGoToPreShow(elevatorId)

    def acceptGoToFirstTime(self, elevatorId):
        """
        The AI's response back to the leader's first request saying that everybody was accepted.
        Flag this response and use this response flag before we requestGoToSecondTime.
        """
        self.waitingForFirstResponse = False
        self.firstRequestAccepted = True

    def requestGoToSecondTime(self, elevatorId):
        """
        Request the AI if the leader and all the members can go directly to the elevator destination.
        This is the first request the leader makes to the AI.
        The AI responds back only to the leader with a rejectGoToRequest if anything goes wrong or
        responds back to all the members with a acceptGoToSecondTime if everything goes well.
        """
        if not self.waitingForFirstResponse:
            if self.firstRequestAccepted:
                self.firstRequestAccepted = False
                self.disableGoButton()
                self.sendUpdate("requestGoToSecondTime", [elevatorId])
        else:
            # 3 seconds have passed and we haven't heard back from the AI yet.
            # Post a generic reject message.
            self.postRejectGoto(elevatorId, BoardingPartyBase.BOARDCODE_MISSING, [], [])
            self.cancelGoToElvatorDest()

    def acceptGoToSecondTime(self, elevatorId):
        """
        The AI's response to all the members of the group that everybody was accepted to
        Go directly to the elevator destination.
        Now all the members can start the GoToShow.
        """
        self.startGoToShow(elevatorId)

    def rejectGoToRequest(self, elevatorId, reason, avatarsFailingRequirements, avatarsInBattle):
        """
        The AI's response back to the leader's first request saying that something went wrong.
        Now the leader should stop GoToPreShow.
        """
        self.firstRequestAccepted = False
        self.waitingForFirstResponse = False
        self.cancelGoToElvatorDest()
        self.postRejectGoto(elevatorId, reason, avatarsFailingRequirements, avatarsInBattle)

    def startGoToPreShow(self, elevatorId):
        """
        This is where the first 3 seconds of GO Pre show happens only on the leader's client.
        GO Button becomes Cancel GO Button and the leader can't move.
        """
        self.notify.debug('Starting Go Pre Show.')

        place = base.cr.playGame.getPlace()
        if place:
            place.setState('stopped')

        goButtonPreShow = BoardingGroupShow.BoardingGroupShow(localAvatar)
        goButtonPreShowTrack = goButtonPreShow.getGoButtonPreShow()

        if self.groupPanel:
            self.groupPanel.changeGoToCancel()
            self.groupPanel.disableQuitButton()
            self.groupPanel.disableDestinationScrolledList()

        self.finishGoToPreShowTrack()
        self.goToPreShowTrack = Sequence()
        self.goToPreShowTrack.append(goButtonPreShowTrack)
        # Request to the AI the second time using requestGoToSecondTime
        self.goToPreShowTrack.append(Func(self.requestGoToSecondTime, elevatorId))
        self.goToPreShowTrack.start()

    def finishGoToPreShowTrack(self):
        """
        Finish the goToPreShowTrack, if it is still going on.
        """
        if self.goToPreShowTrack:
            self.goToPreShowTrack.finish()
            self.goToPreShowTrack = None

    def startGoToShow(self, elevatorId):
        """
        This is where the 3 seconds of GO show happens. This is essentially the teleport track
        and then the client is taken to the elevator destination.
        """
        self.notify.debug('Starting Go Show.')

        # Retract any pending invitations.
        localAvatar.boardingParty.forceCleanupInviterPanels()

        elevatorName = self.__getDestName(elevatorId)
        if self.groupPanel:
            self.groupPanel.disableQuitButton()
        goButtonShow = BoardingGroupShow.BoardingGroupShow(localAvatar)

        place = base.cr.playGame.getPlace()
        if place:
            place.setState('stopped')

        self.goToShowTrack = goButtonShow.getGoButtonShow(elevatorName)
        self.goToShowTrack.start()

    def finishGoToShowTrack(self):
        """
        Finish the goToShowTrack, if it is still going on.
        """
        if self.goToShowTrack:
            self.goToShowTrack.finish()
            self.goToShowTrack = None

    def cancelGoToElvatorDest(self):
        """
        The leader has decided to Cancel going to the elevator destination
        using the Cancel Go Button.
        """
        self.notify.debug('%s cancelled the GoTo Button.' %(localAvatar.doId))
        self.firstRequestAccepted = False
        self.waitingForFirstResponse = False
        self.finishGoToPreShowTrack()
        place = base.cr.playGame.getPlace()
        if place:
            place.setState('walk')
        if self.groupPanel:
            self.groupPanel.changeCancelToGo()
            self.groupPanel.enableGoButton()
            self.groupPanel.enableQuitButton()
            self.groupPanel.enableDestinationScrolledList()

    def __getDestName(self, elevatorId):
        elevator = base.cr.doId2do.get(elevatorId)
        destName = ''
        if elevator:
            destName = elevator.getDestName()
        return destName

    def showMe(self, message, pos = None):
        """
        Making a version of elevatorNotifier.showMe. This version doesn't put the toon
        into stopped state while displaying the panel. At the same time, the OK button
        in the panel doesn't put the toon in the walk state.
        """
        base.localAvatar.elevatorNotifier.showMeWithoutStopping(message, pos)

    def forceCleanupInviteePanel(self):
        """
        Forcibly close the group invitee panel, with a reject as the default answer.
        """
        if self.isInviteePanelUp():
            self.groupInviteePanel.forceCleanup()
            self.groupInviteePanel = None

    def forceCleanupInviterPanels(self):
        """
        Forcibly cleanup the inviter panels, with a reject as the default answer.
        """
        if self.inviterPanels:
            self.inviterPanels.forceCleanup()
