def divider(string, limit):
    string = string.strip()
    lst =[]
    x = 0
    if len(string) <= limit:
        lst.append(string)
    else:
        while len(string)>limit:
            try:
                if string[limit-x] == ' ':
                    lst.append(string[:limit-x].strip())
                    string = string[limit-x:].strip()
                    x = 0
                else:
                    x+=1
            except IndexError:
                string = "WARNING: SOME TEXT IS MISSING THIS IS THE INCOMPLETE SUMMARY"
                break
        lst.append(string)
        #print(lst)        
    return lst