from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.conf import settings
import requests
from isodate import *
# Create your views here.
def index(request):


    chanel_url='https://www.googleapis.com/youtube/v3/channels'
    params={
        'part':'snippet,statistics',
        'key':settings.YOUTUBE_DATA_API_KEY,
        'id':settings.YOUTUBE_CHANNEL_ID
    }
    r=requests.get(chanel_url,params=params)
    results=r.json()['items'][0]
    chanel_details={
        'chanel_name':results['snippet']['title'],
        'chanel_description':results['snippet']['description'],
        'id':results['id'],
        'chanel_thumbnail':results['snippet']['thumbnails']['high']['url'],
        'subscriberCount':results['statistics']['subscriberCount'],
        'videoCount':results['statistics']['videoCount'],




    }


    search_url='https://www.googleapis.com/youtube/v3/search'

    params_search={
        'part':'snippet',
        'key':settings.YOUTUBE_DATA_API_KEY,
        'maxResults':24,
        'channelId':settings.YOUTUBE_CHANNEL_ID,
        'type':'video',
        'order':'date'

    }
    r=requests.get(search_url,params=params_search)
    results=r.json()['items']


    video_url='https://www.googleapis.com/youtube/v3/videos'
    video_ids=[]

    for result in results:
        video_ids.append(result['id']['videoId'])
    
    video_params={
        'part':'snippet,contentDetails',
        'key':settings.YOUTUBE_DATA_API_KEY,
        'maxResults':24,
        'id':','.join(video_ids),
        'order':'date'
    }

    r=requests.get(video_url,params=video_params)
    results=r.json()['items']
    videos=[]
    for result in results:
        video_data={
            'title':result['snippet']['title'],
            'id':result['id'],
            'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds() //60),
            'thumbnail':result['snippet']['thumbnails']['high']['url']

        }
        videos.append(video_data)
    
    print(videos)
    return render(request,'myapp/index.html',{'chanel_details':chanel_details,'videos':videos})

