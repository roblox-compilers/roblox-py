class Inventory
  items: 1
  add_item: (name) =>
    if #@items > size then error "backpack is full"
    super name
  list_items: () =>
    for item in @items
      print item

class BackPack extends Inventory
  size: 10
  add_item: (name) =>
    if #@items > size then error "backpack is full"
    super name

newBackPack = new BackPack 10
newBackPack.add_item "sword"
newBackPack.add_item "shield"
newBackPack.add_item "potion"
newBackPack.list_items!