from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class FollowListViewTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="123")
        self.bob = User.objects.create_user(username="bob", password="123")
        self.carol = User.objects.create_user(username="carol", password="123")

        self.alice.profile.following.add(self.bob.profile)
        self.carol.profile.following.add(self.alice.profile)

    def test_followers_list_shows_profiles(self):
        response = self.client.get(
            reverse("accounts:follow_list", args=[self.alice.username, "followers"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "carol")
        self.assertNotContains(response, "bob")

    def test_following_list_shows_profiles(self):
        response = self.client.get(
            reverse("accounts:follow_list", args=[self.alice.username, "following"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bob")
        self.assertNotContains(response, "carol")

    def test_own_following_list_shows_unfollow_button(self):
        self.client.login(username="alice", password="123")

        response = self.client.get(
            reverse("accounts:follow_list", args=[self.alice.username, "following"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deixar de seguir")


class DiscoverPeopleTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="123")
        self.bob = User.objects.create_user(username="bob", password="123")
        self.carol = User.objects.create_user(username="carol", password="123")

        self.alice.profile.following.add(self.bob.profile)

    def test_discover_people_shows_follow_button_states(self):
        self.client.login(username="alice", password="123")

        response = self.client.get(reverse("accounts:discover_people"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deixar de seguir")
        self.assertContains(response, "Seguir")

    def test_toggle_follow_redirects_to_next_url(self):
        self.client.login(username="alice", password="123")

        response = self.client.post(
            reverse("accounts:toggle_follow", args=[self.carol.username]),
            {"next": reverse("accounts:discover_people")},
        )

        self.assertRedirects(response, reverse("accounts:discover_people"))
        self.assertIn(self.carol.profile, self.alice.profile.following.all())
