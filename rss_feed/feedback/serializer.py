class LikeSerializer(serializers.Serializer):
    model = serializers.CharField(max_length = 50)
    model_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context['request']
        if validated_data["model"] == "podcast":
            podcast = Podcast.objects.get(id=validated_data["model_id"])
            if podcast:
                like = Like(content_object = podcast, account = request.user)
                like.save()
        elif validated_data["model"] == "episode":
            episode = Episode.objects.get(id=validated_data["model_id"])
            if episode:
                like = Like(content_object = episode, account = request.user)
                like.save()
        return like
