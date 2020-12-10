from unittest import mock
from django.utils import timezone

from django.contrib.auth.models import User

# Create your tests here.
from rest_framework.test import APITestCase
import datetime
import pytz

from analytics.models import UserVisit


class UserVisitLoggingTests(APITestCase):

    def test_helloworld_works(self):
        """
        We can make a basic request to /helloworld/
        """
        response = self.client.get('/helloworld/')
        assert response.data.get('version') == 1.0

    def test_helloworld_returns_the_current_time(self):
        """
        The /helloworld/ endpoint shows the current time
        """
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime.datetime(2020, 6, 6, 9, tzinfo=pytz.UTC)
            response = self.client.get('/helloworld/')
        self.assertEqual(response.data.get('time'), datetime.datetime(2020, 6, 6, 9, tzinfo=pytz.UTC))

    def test_helloworld_logs_last_logins(self):
        """
        When we visit /helloworld/ as a logged-in user, then the system logs a UserVisit for us
        """
        user = User.objects.create_user(username='bob', password='bob')
        self.client.login(username='bob', password='bob')
        self.client.get('/helloworld/')
        self.assertEqual(UserVisit.objects.count(), 1)
        self.assertEqual(UserVisit.objects.first().user, user)

    def test_other_views_log_last_logins(self):
        """
        When we visit any other url as a logged in user, then a visit is also logged there
        """
        user = User.objects.create_user(username='bob', password='bob')
        self.client.login(username='bob', password='bob')
        self.client.get('/bunnies/')
        self.assertEqual(UserVisit.objects.count(), 1)
        self.assertEqual(UserVisit.objects.first().user, user)

    def test_only_one_UserVisit_created_per_user(self):
        '''
        Only one UserVisit is created for each user, but the time and number of visits is updated
        '''
        user = User.objects.create_user(username='bob', password='bob')
        self.client.login(username='bob', password='bob')
        self.client.get('/bunnies/')
        self.assertEqual(UserVisit.objects.count(), 1)

        with mock.patch('django.utils.timezone.now') as mock_tz:
            mock_tz.return_value = datetime.datetime(2020, 6, 6, 9, tzinfo=pytz.UTC)
            self.client.get('/bunnies/')
        self.assertEqual(UserVisit.objects.count(), 1)
        visit = UserVisit.objects.get(user=user)

        assert visit.last_seen == datetime.datetime(2020, 6, 6, 9, tzinfo=pytz.UTC)
        assert visit.visits == 2

    def test_show_number_of_visitors_and_visits(self):
        '''
        The /helloworld/ endpoint shows the correct number of recent visitors and the correct number of
        all visitors and visits, including the current visit to /helloworld/
        '''
        current_user = User.objects.create_user(username='bob', password='bob')
        now = datetime.datetime(2020, 6, 6, 9, tzinfo=pytz.UTC)
        with mock.patch('django.utils.timezone.now') as mock_now:
            for i in range(1, 6):
                mock_now.return_value = now - timezone.timedelta(minutes=i)
                recent_user = User.objects.create_user(username=f'user{i}', password=f'password{i}')
                UserVisit.objects.create(user=recent_user, visits=i)

            mock_now.return_value = now - datetime.timedelta(hours=3)
            old_user = User.objects.create_user(username='jamie', password='jamie')
            UserVisit.objects.create(user=old_user, visits=1)

            mock_now.return_value = now
            self.client.login(username='bob', password='bob')
            response = self.client.get('/helloworld/')

        self.assertEqual(response.data.get('time'), now)
        self.assertEqual(response.data.get('recent_visitors'), 6)
        self.assertEqual(response.data.get('all_visitors'), 7)
        self.assertEqual(response.data.get('all_visits'), 17)




