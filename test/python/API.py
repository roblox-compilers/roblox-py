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