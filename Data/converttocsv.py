import json,time

def xstr(s):
    return '""' if s is None else '"' + str(s) + '"'

f = open('out.json','r')
j = json.load(f)

f = open('data.csv','wb')
f.write(bytes('"Yr","Movie","DavidScore","MargScore","RvwDate","Link"\n','UTF-8'))

for yr in j:
    if yr=='yr_uri':continue
    for mov in j[yr]:
        strOut = xstr(yr) + ','
        strOut += '"' + mov.replace(',','') + '",'
        print(mov,yr)
        strOut += xstr(j[yr][mov].get('D_score')) + ','
        strOut += xstr(j[yr][mov].get('M_score')) + ','
        strOut += xstr(j[yr][mov].get('Review_date')) + ','
        strOut += xstr(j[yr][mov].get('_link')) + ','
        strOut += '\n'
        f.write(bytes(strOut,'UTF-8'))
f.close()
