from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Song
from .serializers import SongSerializer
import os


class SongListView(APIView):
    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class SongUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongDeleteView(APIView):
    def delete(self, request, song_id):
        try:
            song = Song.objects.get(id=song_id)
            song_file_path = song.file.path

            # Delete the file from storage
            if os.path.exists(song_file_path):
                os.remove(song_file_path)

            # Delete the song record from the database
            song.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found."}, status=status.HTTP_404_NOT_FOUND)
