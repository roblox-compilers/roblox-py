"""Holds many useful functions for roblox-pyc"""

def backwordreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)
