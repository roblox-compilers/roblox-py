local count
count = function(current)
  if current ~= nil then
    if typeof(current == "number") then
      if current > 0 then
        print(current)
        return count(current - 1)
      else
        if current == 0 then
          return print(current)
        else
          print(current)
          return count(current + 1)
        end
      end
    elseif typeof(current == "table") then
      if current.length > 0 then
        print(current)
        return count(current.slice(0, current.length - 1))
      else
        return print(current)
      end
    else
      print(current)
      return count(current + 1)
    end
  else
    return print("Next time, give me a number!")
  end
end
count(0)
count(5)
count()
count(-1)
count(0)
count(1)
count(2.0)
count("hi")
return count({
  1,
  2,
  3
})
