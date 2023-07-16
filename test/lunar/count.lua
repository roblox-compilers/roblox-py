local Inventory
do
  local _class_0
  local _base_0 = {
    items = 1,
    add_item = function(self, name)
      if #self.items > size then
        error("backpack is full")
      end
      return _class_0.__parent.__base.add_item(self, name)
    end,
    list_items = function(self)
      for item in self.items do
        print(item)
      end
    end
  }
  _base_0.__index = _base_0
  _class_0 = setmetatable({
    __init = function() end,
    __base = _base_0,
    __name = "Inventory"
  }, {
    __index = _base_0,
    __call = function(cls, ...)
      local _self_0 = setmetatable({}, _base_0)
      cls.__init(_self_0, ...)
      return _self_0
    end
  })
  _base_0.__class = _class_0
  Inventory = _class_0
end
local BackPack
do
  local _class_0
  local _parent_0 = Inventory
  local _base_0 = {
    size = 10,
    add_item = function(self, name)
      if #self.items > size then
        error("backpack is full")
      end
      return _class_0.__parent.__base.add_item(self, name)
    end
  }
  _base_0.__index = _base_0
  setmetatable(_base_0, _parent_0.__base)
  _class_0 = setmetatable({
    __init = function(self, ...)
      return _class_0.__parent.__init(self, ...)
    end,
    __base = _base_0,
    __name = "BackPack",
    __parent = _parent_0
  }, {
    __index = function(cls, name)
      local val = rawget(_base_0, name)
      if val == nil then
        local parent = rawget(cls, "__parent")
        if parent then
          return parent[name]
        end
      else
        return val
      end
    end,
    __call = function(cls, ...)
      local _self_0 = setmetatable({}, _base_0)
      cls.__init(_self_0, ...)
      return _self_0
    end
  })
  _base_0.__class = _class_0
  if _parent_0.__inherited then
    _parent_0.__inherited(_parent_0, _class_0)
  end
  BackPack = _class_0
end
local newBackPack = new(BackPack(10))
newBackPack.add_item("sword")
newBackPack.add_item("shield")
newBackPack.add_item("potion")
return newBackPack.list_items()
