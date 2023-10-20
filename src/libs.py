json = """local json = {}
function json.encode(t)
    return game.HttpService:JSONEncode(t)
end
function json.decode(t)
    return game.HttpService:JSONDecode(t)
end
function fault()
    error("[roblox-py] (json-lib) Outputting to files is not supported.")
end
json.load, json.dump = fault, fault"""

libs = ["json"]