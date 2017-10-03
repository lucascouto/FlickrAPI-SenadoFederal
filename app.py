# -*-encoding: utf-8 -*-

import flickrapi
import json

api_key = u'a28c3fe50ca319c70f4f6d084bacfde0'
api_secret = u'11474440b560ace0'
user = '49143546@N06' #Usuário Senado Federal

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

#Retorna os albuns do Senado Federal
albums_meta = flickr.photosets.getList(user_id = user)
albums = albums_meta['photosets']['photoset']

# Total de albuns
albums_total = albums_meta['photosets']['total']
print("Total de albuns: " + str(albums_total))

with open('albums_meta.json', 'wb') as outfile:
    json.dump(albums_meta, outfile)

with open('albums.json', 'wb') as outfile:
    json.dump(albums, outfile)


album_index = 0

for albums_id in albums:
    #Recupera o ID do álbum e a lista de fotos associada ao álbum
    albums_id[album_index] = albums[album_index]["id"]


    album_title = albums[album_index]['title']['_content']
    #album_number_photos = albums[album_index]['photos']
    #album_views = albums[album_index]['count_views']
    


    photos_album_meta = flickr.photosets.getPhotos(user_id = user, photoset_id=albums_id[album_index])
    with open('photos_album_meta.json', 'wb') as outfile:
        json.dump(photos_album_meta, outfile)
    print("Album " + str(album_index+1) +  ": " + album_title + " (id: " + albums_id[album_index] + ")") #DEBUG
    photos_album = photos_album_meta['photoset']['photo']
    with open('photos_album.json', 'wb') as outfile:
        json.dump(photos_album, outfile)


    #Recupera os IDs das fotos da lista associada ao álbum anterior
    photos_index = 0
    for photo_id in photos_album:
        photo_id[photos_index] = photos_album[photos_index]["id"]
        #Recuperar informações da foto corrente
        photo_info_meta = flickr.photos.getInfo(user_id=user, photo_id=photo_id[photos_index])
        with open('photo_info_meta.json', 'wb') as outfile:
            json.dump(photo_info_meta, outfile)
        photo_info = photo_info_meta['photo']
        with open('photo_info.json', 'wb') as outfile:
            json.dump(photo_info, outfile)
        photo_url = photo_info['urls']['url'][0]['_content']


        #photo_description = photo_info['description']['_content']
        photo_title = photo_info['title']['_content']
        photo_views = photo_info['views']


        print("\t\tFoto " + str(photos_index+1) + ": " + photo_title +  " (id: " + str(photo_id[photos_index]) + ")") #para debug
        print("\t\t" + photo_url) #para debug
        #print("\t\t\t" + photo_description)
        print("\t\tVisualizacoes: " + photo_views + "\n\n")

        photos_index += 1
    album_index += 1
