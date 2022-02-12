RabbitHoleSerializer(
    <RabbitHole: RabbitHole object (1)>, 
    context={
        'request': <rest_framework.request.Request object>, 
        'format': None, 
        'view': <bunnies.views.RabbitHoleViewSet object>}
        
    ):
    location = CharField(max_length=64, validators=[<UniqueValidator(queryset=RabbitHole.objects.all())>])
    bunnies = PrimaryKeyRelatedField(
        many=True, queryset=<QuerySet [
            <Bunny: Bunny object (1)>, 
            <Bunny: Bunny object (2)>, 
            <Bunny: Bunny object (3)>, 
            <Bunny: Bunny object (4)>
            ]>)
    bunny_count = SerializerMethodField()
    owner = HiddenField(default=CurrentUserDefault())