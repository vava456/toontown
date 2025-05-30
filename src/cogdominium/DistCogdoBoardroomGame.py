from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.cogdominium.DistCogdoLevelGame import DistCogdoLevelGame
from toontown.cogdominium.CogdoBoardroomGameBase import CogdoBoardroomGameBase
from toontown.cogdominium import CogdoBoardroomGameConsts as Consts
from toontown.toonbase import ToontownTimer
from toontown.toonbase import TTLocalizer as TTL

class DistCogdoBoardroomGame(CogdoBoardroomGameBase, DistCogdoLevelGame):
    notify = directNotify.newCategory("DistCogdoBoardroomGame")

    def __init__(self, cr):
        #DistCogdoGame.__init__(self, cr)
        DistCogdoLevelGame.__init__(self, cr)

    def getTitle(self):
        return TTL.BoardroomGameTitle

    def getInstructions(self):
        return TTL.BoardroomGameInstructions

    def announceGenerate(self):
        #DistCogdoGame.announceGenerate(self)
        DistCogdoLevelGame.announceGenerate(self)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.setScale(Consts.Settings.TimerScale.get())
        self.timer.stash()

    def disable(self):
        self.timer.destroy()
        self.timer = None
        #DistCogdoGame.disable(self)
        DistCogdoLevelGame.disable(self)

    def enterGame(self):
        #DistCogdoGame.enterGame(self)
        DistCogdoLevelGame.enterGame(self)
        #self.timer.posInTopRightCorner()
        #timeLeft = 15. - (globalClock.getRealTime() - self.getStartTime())
        timeLeft = Consts.GameDuration.get() - (globalClock.getRealTime() - self.getStartTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def enterFinish(self):
        #DistCogdoGame.enterFinish(self)
        DistCogdoLevelGame.enterFinish(self)
        #timeLeft = 10 - (globalClock.getRealTime() - self.getFinishTime())
        timeLeft = Consts.FinishDuration.get() - (globalClock.getRealTime() - self.getFinishTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def timerExpired(self):
        pass

    if __dev__:

        def _handleTimerScaleChanged(self, timerScale):
            if hasattr(self, 'timer'):
                self.timer.setScale(timerScale)
