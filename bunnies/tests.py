from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APITestCase

from bunnies.models import RabbitHole, Bunny


class RabbitHolesTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse(
            'rabbithole-list'
        )

    def test_authentication_required(self):
        '''
        I can only view the list of rabbitholes if I'm logged in
        '''

        assert self.client.get(self.url).status_code == 403
        User.objects.create_user(username='admin', email='rabbitoverlord@test.com', password='rabbits')
        self.client.login(username='admin', password='rabbits')
        assert self.client.get(self.url).status_code == 200

    def test_can_only_see_my_own_rabbit_holes(self):
        '''
        I can only see rabbitholes that I created
        '''
        user1 = User.objects.create_user(username='user1', email='user1@test.com', password='rabbits')
        user2 = User.objects.create_user(username='user2', email='user2@test.com', password='rabbits')

        RabbitHole.objects.create(owner=user1, location='location1')
        RabbitHole.objects.create(owner=user2, location='location2')

        self.client.login(username='user1', password='rabbits')

        response = self.client.get(self.url)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('location'), 'location1')

    def test_bunny_count_calculated_field(self):
        '''
        The RabbitHole serializer automatically counts the number of bunnies living in the hole
        '''
        user1 = User.objects.create_user(username='user1', email='user1@test.com', password='rabbits')
        hole = RabbitHole.objects.create(owner=user1, location='location1')

        for name in ['Flopsy', 'Mopsy', 'CottonTail']:
            Bunny.objects.create(name=name, home=hole)

        other_rabbit_hole = RabbitHole.objects.create(owner=user1, location='location2')
        other_bunny = Bunny.objects.create(name='Snowball', home=other_rabbit_hole)

        self.client.login(username=user1.username, password='rabbits')

        response = self.client.get(f'/rabbitholes/{hole.id}/')

        assert response.status_code == 200

        self.assertEqual(len(response.data.get('bunnies')), 3)
        self.assertEqual(response.data.get('bunny_count'), 3)

    def test_creating_rabbit_holes_sets_user_from_automatically(self):
        '''
        When we create a rabbithole, the owner is automatically set to the request user
        '''

        correct_user = User.objects.create_user(username='bob', password='bob', email='bob@test.com')
        wrong_user = User.objects.create_user(username='mavis', password='mavis', email='mavis@test.com')

        self.client.login(username='bob', password='bob')

        data = {
            'owner': wrong_user.id,
            'location': 'somewhere',
            'bunnies': []
        }

        response = self.client.post('/rabbitholes/', data=data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(RabbitHole.objects.count(), 1)
        self.assertEqual(RabbitHole.objects.first().owner, correct_user)

    def test_superuser_can_delete_any_rabbithole(self):
        '''
        A superuser can delete any of the rabbitholes
        '''
        user = User.objects.create_user(username='user', email='user@test.com', password='rabbits')
        superuser = User.objects.create_user(username='superuser', email='superuser@test.com', password='rabbits',
                                             is_superuser=True)

        rabbit_hole = RabbitHole.objects.create(owner=user, location='location')
        self.client.login(username='superuser', password='rabbits')
        response = self.client.delete(f'/rabbitholes/{rabbit_hole.id}/')
        self.assertEqual(response.status_code, 204)

    def test_cannot_exceed_bunnies_limit(self):
        '''
        Cannot exceed the limit of bunnies in a rabbithole
        '''
        user = User.objects.create_user(username='user', email='user@test.com', password='rabbits')
        rabbit_hole = RabbitHole.objects.create(owner=user, location='location', bunnies_limit=3)
        for name in ['Flopsy', 'Mopsy', 'CottonTail']:
            Bunny.objects.create(name=name, home=rabbit_hole)
        url = reverse(
            'bunny-list'
        )
        self.client.login(username='user', password='rabbits')
        data = {
            'name': 'Harry',
            'home': rabbit_hole.location
        }
        response = self.client.post(f'/bunnies/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_family_members(self):
        '''
        The family_members field should return the names of all the bunnies that live in the same rabbit hole as the
        one we are looking at
        '''
        user = User.objects.create_user(username='user', email='user@test.com', password='rabbits')
        rabbit_hole = RabbitHole.objects.create(owner=user, location='location')
        other_rabbit_hole = RabbitHole.objects.create(owner=user, location='location2')
        names = ['Flopsy', 'Mopsy', 'CottonTail']
        for name in names:
            Bunny.objects.create(name=name, home=rabbit_hole)
        bunny = Bunny.objects.create(name='Harry', home=rabbit_hole)
        other_bunny = Bunny.objects.create(name='Snowball', home=other_rabbit_hole)

        self.client.login(username='user', password='rabbits')
        response = self.client.get(f'/bunnies/{bunny.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(names), set(response.data['family_members']))
        assert other_bunny.name not in response.data['family_members']




