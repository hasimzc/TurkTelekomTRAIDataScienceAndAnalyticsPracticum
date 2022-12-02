# proje 1
liste = [[1,'a',['cat'],2],[[[3]],'dog'],4,5]
def flatten(liste,new_list = []):
    for l in liste:
        if type(l) == list:
            flatten(l,new_list)
        else:
            new_list.append(l)
    return new_list
print(flatten(liste))
# proje 2
liste = [[1, 2], [3, 4], [5, 6, 7]]
def reverser(liste,new_list = []):
    liste.reverse()
    for l in liste:
        if type(l) == list:
            l.reverse()
            new_list.append(l)
        else:
            new_list.append(l)
    return new_list
print(reverser(liste))