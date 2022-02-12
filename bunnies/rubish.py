# what is inside self __dict__

{'_args': (), 
'_kwargs': 
    {'data': <QueryDict: 
        {'name': ['Harry'], 'home': ['location']}>, 
    'context': {
        'request': <rest_framework.request.Request object at 0x0000025D02A70430>, 
        'format': None, 
        'view': <bunnies.views.BunnyViewSet object at 0x0000025D02A701F0>
        }
    }, 
'instance': <Bunny: Bunny object (4)>, 
'initial_data': <QueryDict: {
    'name': ['Harry'], 'home': ['location']
    }>,
'partial': False, '_context': {
    'request': <rest_framework.request.Request object at 0x0000025D02A70430>,
    'format': None, 
    'view': <bunnies.views.BunnyViewSet object at 0x0000025D02A701F0>}, 
    '_creation_counter': 28, 
    'read_only': False, 
    'write_only': False, 
    'required': True, 
    'default': <class 'rest_framework.fields.empty'>, 
    'source': None, 
    'initial': None, 
    'label': None, 
    'help_text': None, 
    'style': {}, 
    'allow_null': False, 
    'field_name': None, 
    'parent': None, 
    'error_messages': {
        'required': 'This field is required.',
        'null': 'This field may not be null.', 
        'invalid': 'Invalid data. Expected a dictionary, but got {datatype}.'
        },
    'url_field_name': 'url', 
    'fields': {
        'name': CharField(max_length=64), 
        'home': SlugRelatedField(
            queryset=<QuerySet [<RabbitHole: RabbitHole object (1)>]>, 
            slug_field='location'
            ), 
        'family_members': SerializerMethodField()
    }, 
    '_validators': [], 
    '_validated_data': OrderedDict([
        ('name', 'Harry'), 
        ('home', <RabbitHole: RabbitHole object (1)>)
        ]), 
    '_errors': {}
}
