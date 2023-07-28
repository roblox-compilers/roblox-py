# CONFIG
# CFG will be in the same directory as this file
import pickle, os
cfgPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cfg.pkl")
def getconfig(arg1, arg2, default="None"):
    try:
      # Load the config file if it exists, or create a new one if it doesn't
      if os.path.exists(cfgPath):
          with open(cfgPath, "rb") as f:
              cfg = pickle.load(f)
      else:
          cfg = {}

      # Get the value from the config file, or use the default value if it doesn't exist
      value = cfg.get(arg1, {}).get(arg2, default)

      # Update the config file with the default value if it doesn't exist
      if arg1 not in cfg:
          cfg[arg1] = {}
      if arg2 not in cfg[arg1]:
          cfg[arg1][arg2] = default
          with open(cfgPath, "wb") as f:
              pickle.dump(cfg, f)

      return value
    except EOFError:
      # The file is empty, write a {} to it
      with open(cfgPath, "wb") as f:
        pickle.dump({}, f)
      return getconfig(arg1, arg2, default)

def setconfig(arg1, arg2, value, ignore=None):
    try:
      # Load the config file if it exists, or create a new one if it doesn't
      if os.path.exists(cfgPath):
          with open(cfgPath, "rb") as f:
              cfg = pickle.load(f)
      else:
          cfg = {}

      # Set the value in the config file and save it
      if arg1 not in cfg:
          cfg[arg1] = {}
      cfg[arg1][arg2] = value
      with open(cfgPath, "wb") as f:
          pickle.dump(cfg, f)
    except EOFError:
      # The file is empty, write a {} to it
      with open(cfgPath, "wb") as f:
        pickle.dump({}, f)
      return setconfig(arg1, arg2, value, ignore=ignore)
