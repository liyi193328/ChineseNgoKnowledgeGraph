
s1 = r'<a target="_blank" href="/org'
ls1 = len(s1)
def findOrg(html):
    loc = 0
    result = set()
    while loc != -1:
        loc = html.find(s1, loc)
        # print("loc: ",loc)
        if loc != -1:
            sec = html.find('/', loc + ls1)
            if sec != -1:
                tmp = int(html[loc + ls1:sec])
                result.add(tmp)
                # print(tmp)
            loc = loc + ls1
        else:
            break
    # print("result:\n", result)
    return result
