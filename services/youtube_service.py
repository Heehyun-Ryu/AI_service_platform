from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = "AIzaSyBU7JOl10TTo3y3sZThPI0bBAaMpv0ZzbM"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

async def search_youtube(query, max_result):
    try:
        search_response = youtube.search().list(
            q = query,
            part = 'snippet',
            maxResults = max_result,
            type = 'video'
        ).execute()

        videos = []
        for item in search_response.get('items', []):
            video_data = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channel': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt']
            }
            videos.append(video_data)
        return JSONResponse(content={"results": videos})
    except HttpError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


async def video_details(video_id: str):
    try:
        video_response = youtube.videos().list(
            id=video_id,
            part='snippet,statistics,contentDetails'
        ).execute()

        if video_response['items']:
            video = video_response['items'][0]
            video_data = {
                'id': video['id'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'thumbnail': video['snippet']['thumbnails']['high']['url'],
                'channel': video['snippet']['channelTitle'],
                'publishedAt': video['snippet']['publishedAt'],
                'viewCount': video['statistics'].get('viewCount', '0'),
                'likeCount': video['statistics'].get('likeCount', '0'),
                'commentCount': video['statistics'].get('commentCount', '0'),
                'duration': video['contentDetails']['duration']
            }
            return JSONResponse(content=video_data)
        else:
            return JSONResponse(content={"error": "Video not found"}, status_code=404)
    except HttpError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)