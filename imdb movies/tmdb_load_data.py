import requests
import pandas as pd

def get_data(base_url,page_no=None):
    flag = False
    data = None
    base_url = base_url+str(page_no)
    while flag !=True:            
        try:
            res = requests.get(base_url)
            if res.status_code == 200:
                data = res.json()
                flag = True
        except Exception as e:
            pass
    return data


#genre ids to genre name
genre_url = "https://api.themoviedb.org/3/genre/movie/list?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
genre_data  = get_data(genre_url)

id_list = []
genre_list = []
for i in genre_data['genres']:
    id_list.append(i['id'])
    genre_list.append(i['name'])
genre_dict = dict(zip(id_list,genre_list))



def load_data():
    base_url = "https://api.themoviedb.org/3/movie/top_rated?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US&page="
    movie_titles = []
    genre_list = []
    descriptions = []
    for no in range(1,472):
        #create a seprate url for every page
        data = get_data(base_url,page_no=no)
        for result in range(len(data['results'])):
            # movies titles 
            movie_titles.append(data['results'][result]['title'])

            # movie description
            descriptions.append(data['results'][result]['overview'])       

            #genre list
            ids = data['results'][result]['genre_ids']
            temp_list = []
            for id in ids:
                temp_list.append(genre_dict[id])
            genre_list.append(",".join(temp_list))
            temp_list.clear()


    dataset = pd.DataFrame({
        'movie_name':movie_titles,
        'description':descriptions,
        'genre':genre_list
    })
    return dataset


df = load_data()
df.to_csv(r'D:\nlp-basics\movies.csv',index=False)