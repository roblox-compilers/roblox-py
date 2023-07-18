count = (current)->
    if current != nil
        if typeof current == "number"
            if current > 0
                print current
                count current-1
            else if current == 0
                print current
            else
                print current
                count current+1
        elseif typeof current == "table"
            if current.length > 0
                print current
                count current.slice(0,current.length-1)
            else
                print current
        else
            print current
            count current+1
        
    else
        print "Next time, give me a number!"

count(0)
count 5
count!
count -1
count 0
count 1
count 2.0
count "hi"
count {1,2,3}