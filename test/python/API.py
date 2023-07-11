@py.Workspace.ChildAdded
def childAdded():
    print("Child added")

@py.Workspace.ChildRemoved  
def childRemoved():
    print("Child removed")