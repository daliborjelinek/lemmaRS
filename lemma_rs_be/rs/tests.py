from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory


from rs.models import User, ProjectGroup, Project


class ProjectTests(APITestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.admin = User.objects.get(pk=2)
        cls.common_user = User.objects.get(pk=4)
        cls.common_user2 = User.objects.get(pk=4)
        cls.group_data = {
            "name": "Test group",
            "description": "test group",
            "active": True
        }
        cls.project_data = {
            "name": "Project 1",
            "description": "string",
            "finished": False,
            "group": 1
        }

    def test_create_group(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse('projectgroup-list'), self.group_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_common_user_cant_create_group(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.post(reverse('projectgroup-list'), self.group_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_project(self):
        self.client.force_authenticate(self.common_user)
        group = ProjectGroup.objects.create(name="string", description="string", active=True)
        project1_data = {
            "name": "Project 1",
            "description": "Project 1",
            "finished": False,
            "group": group.id
        }
        response = self.client.post(reverse('project-list'), project1_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_users(self):
        user1 = User.objects.create(username="user1", email="user1@u.cz")
        user2 = User.objects.create(username="user2", email="user2@u.cz")
        user3 = User.objects.create(username="user3", email="user3@u.cz")
        user4 = User.objects.create(username="user4", email="user4@u.cz")
        user5 = User.objects.create(username="user5", email="user5@u.cz")

        group = ProjectGroup.objects.create(name="group 1", description="test", active=True)

        project = Project.objects.create(name="project 1", owner=user1, group=group)

        self.client.force_authenticate(self.common_user)
        response = self.client.get(reverse('project-list')+"?username=user1")
        self.assertEqual(len(response.data), 1)

        project.members.add(user2)

        response = self.client.get(reverse('project-list')+"?username=user2")
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse('project-list'))
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse('project-list')+"?username=user3")
        self.assertEqual(len(response.data), 0)

        project2 = Project.objects.create(name="project 2", owner=user3, group=group)
        project3 = Project.objects.create(name="project 3", owner=user4, group=group)

        response = self.client.get(reverse('project-list')+"?username=user3")
        self.assertEqual(len(response.data), 1)

        project2.members.add(user1)

        response = self.client.get(reverse('project-list')+"?username=user1")
        self.assertEqual(len(response.data), 2)














    # def test_view_posts(self):
    #     """
    #     Ensure we can view all objects.
    #     """
    #     url = reverse('blog_api:listcreate')
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_account(self):
    #     """
    #     Ensure we can create a new Post object and view object.
    #     """
    #     self.test_category = Category.objects.create(name='django')
    #
    #     self.testuser1 = User.objects.create_user(
    #         username='test_user1', password='123456789')
    #
    #     data = {"title": "new", "author": 1,
    #             "excerpt": "new", "content": "new"}
    #     url = reverse('blog_api:listcreate')
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(len(response.data), 6)
    #     root = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
