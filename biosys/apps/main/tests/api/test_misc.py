from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from main.models import Project, Form

from main.tests import factories
from main.tests.api import helpers


class TestWhoAmI(helpers.BaseUserTestCase):
    def setUp(self):
        super(TestWhoAmI, self).setUp()
        self.url = reverse('api:whoami')

    def test_get(self):
        client = self.anonymous_client
        self.assertEqual(
            client.get(self.url).status_code,
            status.HTTP_200_OK
        )

        user = factories.UserFactory()
        user.set_password('password')
        user.save()
        client = APIClient()
        self.assertTrue(client.login(username=user.username, password='password'))
        resp = client.get(self.url)
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK
        )
        # test that the response contains username, first and last name and email at least and the id
        data = resp.json()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.id, data['id'])

        # test that the password is not in the returned fields
        self.assertFalse('password' in data)

    def test_not_allowed_methods(self):
        client = self.readonly_client
        self.assertEqual(
            client.post(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(
            client.put(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(
            client.patch(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


class TestStatistics(TestCase):
    def setUp(self):
        self.url = reverse('api:statistics')

    def test_get(self):
        anonymous = APIClient()
        client = anonymous
        self.assertIn(
            client.get(self.url).status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

        user = factories.UserFactory.create()
        user.set_password('password')
        user.save()
        client = APIClient()
        self.assertTrue(client.login(username=user.username, password='password'))
        resp = client.get(self.url)
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK
        )
        # expected response with no data
        expected = {
            'projects': {'total': 0},
            'datasets': {
                'total': 0,
                'generic': {'total': 0},
                'observation': {'total': 0},
                'speciesObservation': {'total': 0},
            },
            'records': {
                'total': 0,
                'generic': {'total': 0},
                'observation': {'total': 0},
                'speciesObservation': {'total': 0},
            },
            'sites': {'total': 0},
        }
        self.assertEqual(expected, resp.json())

        # create one project
        program = factories.ProgramFactory.create()
        project = factories.ProjectFactory.create(program=program)
        expected['projects']['total'] = 1
        resp = client.get(self.url)
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(expected, resp.json())

        # create some sites
        count = 3
        factories.SiteFactory.create_batch(
            count,
            project=project
        )
        expected['sites']['total'] = count
        resp = client.get(self.url)
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(expected, resp.json())

    def test_not_allowed_methods(self):
        user = factories.UserFactory.create()
        user.set_password('password')
        user.save()
        client = APIClient()
        self.assertTrue(client.login(username=user.username, password='password'))
        self.assertEqual(
            client.post(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(
            client.put(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(
            client.patch(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


class TestFormEndpoint(helpers.BaseUserTestCase):
    schema_fields = [
        {
            "name": "What",
            "type": "string",
            "constraints": helpers.REQUIRED_CONSTRAINTS
        },
        {
            "name": "When",
            "type": "date",
            "constraints": helpers.NOT_REQUIRED_CONSTRAINTS,
            "format": "any",
            "biosys": {
                'type': 'observationDate'
            }
        },
        {
            "name": "Where",
            "type": "string",
            "constraints": helpers.REQUIRED_CONSTRAINTS
        },
        {
            "name": "Who",
            "type": "string",
            "constraints": helpers.REQUIRED_CONSTRAINTS
        },
    ]

    def setUp(self):
        super(TestFormEndpoint, self).setUp()
        self.site_1 = factories.SiteFactory.create(project=self.project_1)
        self.site_2 = factories.SiteFactory.create(project=self.project_2)
        self.project = self.project_1
        self.client = self.data_engineer_1_client
        self.dataset = self._create_dataset_with_schema(self.project, self.client, self.schema_fields)
        self.form = Form.objects.create(layout={'test':'test1'}, name='testymctestface', dataset=self.dataset)

    def test_happy_path(self):
        url = reverse('api:form-hierarchy')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_sites = response.data['sites']
        expected_site_response = {
            self.project_1.pk: [{self.site_1.pk:(self.site_1.name+' ('+self.site_1.code+')')}],
            self.project_2.pk: [{self.site_2.pk:(self.site_2.name+' ('+self.site_2.code+')')}]
        }
        self.assertEqual(response_sites, expected_site_response)

        form_response = response.data[self.project.pk]
        self.assertEqual(form_response['name'], self.form.name)
        self.assertEqual(form_response['layout'], self.form.layout)
        self.assertEqual(form_response['table_schema'], self.dataset.data_package['resources'][0]['schema'])


class TestSpecies(TestCase):
    # set the species list to be the testing one
    species_facade_class = helpers.LightSpeciesFacade

    def setUp(self):
        from main.api.views import SpeciesMixin
        SpeciesMixin.species_facade_class = self.species_facade_class

        self.url = reverse('api:species')

    def test_get(self):
        anonymous = APIClient()
        client = anonymous
        self.assertEqual(
            client.get(self.url).status_code,
            status.HTTP_200_OK
        )

        user = factories.UserFactory.create()
        user.set_password('password')
        user.save()
        client = APIClient()
        self.assertTrue(client.login(username=user.username, password='password'))
        resp = client.get(self.url)
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK
        )

    def test_not_allowed_methods(self):
        user = factories.UserFactory.create()
        user.set_password('password')
        user.save()
        client = APIClient()
        self.assertTrue(client.login(username=user.username, password='password'))
        self.assertEqual(
            client.post(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(
            client.put(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(
            client.patch(self.url, {}).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
