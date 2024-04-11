json = """local json = {}
function json.loads(t)
    return game.HttpService:JSONEncode(t)
end
function json.dumps(t)
    return game.HttpService:JSONDecode(t)
end
function fault()
    error("[roblox-py] (json-lib) Outputting to files is not supported.")
end
json.load, json.dump = fault, fault"""

libs = ["json"]
