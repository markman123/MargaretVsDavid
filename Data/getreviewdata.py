from bs4 import BeautifulSoup
import requests, time, re, datetime,json

score = {'two-and-a-half stars':2.5
                ,'four stars':4.0
                ,'three-and-a-half stars':3.5
                ,'three stars':3.0
                ,'four-and-a-half stars':4.5
                ,'five stars': 5.0
                ,'two stars': 2.0
                ,'one-and-a-half stars': 1.5
                ,'one stars': 1
                ,'half stars':0.5
                ,'zero stars':0
                }

def getReviews(pg):
    #with the page thats passed in (BS4), get the review data
    #Get the top level table
    lst = {}
    bTest = False
    rvw_tbl = pg.find('div',{'id':'reviewsList'})
    for chd in rvw_tbl.find_all(('h3','p')):
        
        #print(chd)
        if '<h3>' in chd.prettify():
            #This is where the name of the movie is
            thisMovie = chd.text
            if chd.a.get('href') == 'http://www.abc.net.au/atthemovies/txt/s2590277.htm': bTest = True
            lst[thisMovie] = {'_link':chd.a.get('href')}

        else:
            #else its the actual review
            if 'class' in chd.attrs:
                #This means its where the scores are
                if re.search('Margaret',str(chd)) or re.search('David',str(chd)):
                    mPattern = "Margaret:\s\<img.*?alt=\"(.*?)\""
                    mFnd = re.search(mPattern,str(chd))
                    if mFnd: lst[thisMovie]['M_score'] = score[mFnd.group(1)]
                    dPattern = "David:\s\<img.*?alt=\"(.*?)\""
                    dFnd = re.search(dPattern,str(chd))
                    if dFnd: lst[thisMovie]['D_score'] = score[dFnd.group(1)]
                    
                    
            else:
                #This is where the title and reviewed date is
               lst[thisMovie]['Review_date'] = datetime.datetime.strptime(re.sub('Reviewed '
                                               ,'',next(chd.children))
                                        ,'%d %B, %Y').strftime('%Y-%m-%d')  
    return lst
           
def Main():
   lst = {}
   for yr in range(2014,2003,-1):
       uri = 'http://www.abc.net.au/atthemovies/review/byyear/%s.htm' % str(yr)
       req = requests.get(uri)
       print("Getting %s..." %str(yr))
       bs = BeautifulSoup(req.text, 'html.parser')
       lst['yr_uri'] = uri
       lst[yr] = getReviews(bs)
       

   with open('out.json','w') as f:
       json.dump(lst,f,indent=4)

if __name__ == '__main__':
    Main()
