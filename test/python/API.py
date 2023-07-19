import example as examplelibrary
from signal import new as newSignal

ValidPlayers = [
    "builderman"
]

@py.Workspace.Spawn.Touched
def onTouch(touch):
    print("Spawn has been touched by", touch.Name)
    
@py.Players.PlayerAdded
def onPlrAdd(plr):
    if plr.Name in ValidPlayers:
        # The player is in our admin list, print admin joined
        print("Admin", plr.Name, "has joined the game!!")

examplelibrary() # -> Example Library!
@newSignal
def onSignal():
    print("Signal received!")

onSignal.Fire() # -> Signal received!