import os
import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import googleapiclient.discovery

# YOUR VALUES HERE
CHANNEL_ID = "CHANNEL_ID_TO_CHECK"
SEARCH_TERM = "SEARCH_CONDITION"

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    # YOUR VALUE HERE
    DEVELOPER_KEY = "YOUR_DEV_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # Get list of all videos by channelId
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        maxResults=50
    )
    searchResponse = request.execute()

    videoIds = []

    while 'nextPageToken' in searchResponse:
        for i in range(len(searchResponse['items'])):
            if 'videoId' in searchResponse['items'][i]['id']:
                videoIds.append(searchResponse['items'][i]['id']['videoId'])

        request = youtube.search().list(
            part="snippet",
            channelId=CHANNEL_ID,
            pageToken=searchResponse['nextPageToken'],
            maxResults=50
        )
        
        searchResponse = request.execute()

    commentSums = []

    for videoId in videoIds:
        commentSum = 0

        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            searchTerms=SEARCH_TERM,
            videoId=videoId
        )
        commentThreadsResponse = request.execute()
        commentSum = len(commentThreadsResponse['items'])

        while 'nextPageToken' in commentThreadsResponse:
            request = youtube.commentThreads().list(
                part="snippet",
                maxResults=100,
                searchTerms=SEARCH_TERM,
                pageToken=commentThreadsResponse['nextPageToken'],
                videoId=videoId
            )
            commentThreadsResponse = request.execute()
            commentSum += len(commentThreadsResponse['items'])
        
        commentSums.append(commentSum)

    # print_comment_amount(commentThreadsResponse, videoId)

    present_graphically(videoIds, commentSums)

def print_comment_amount(response, videoId):
    print(videoId + ' - ' + str(response['pageInfo']['totalResults']))

def present_graphically(videoIds, commentSums):
    y_pos = np.arange(len(videoIds))
    
    plt.barh(y_pos, commentSums, align='center', alpha=0.5)
    plt.yticks(y_pos, videoIds)
    plt.xlabel('Number of comments')
    plt.title(SEARCH_TERM + ' instances in channel "' + CHANNEL_ID + '"')

    plt.show()

if __name__ == "__main__":
    main()