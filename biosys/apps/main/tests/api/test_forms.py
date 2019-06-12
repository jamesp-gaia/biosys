import json

from django.contrib.gis.geos import GEOSGeometry
from django.core.urlresolvers import reverse
from rest_framework import status

from main.models import Site
from main.tests import factories
from main.tests.api import helpers


class TestFormEndpoint(helpers.BaseUserTestCase):

    def setUp(self):
        super(TestFormEndpoint, self).setUp()
        self.site_1 = factories.SiteFactory.create(project=self.project_1)
        self.site_2 = factories.SiteFactory.create(project=self.project_2)

    def test_happy_path(self):
        urls = [
            reverse('api:site-list'),
            reverse('api:site-detail', kwargs={'pk': self.site_1.pk})
        ]
        access = {
            "forbidden": [self.anonymous_client],
            "allowed": [
                self.readonly_client,
                self.custodian_1_client,
                self.custodian_2_client,
                self.admin_client
            ]
        }
        for client in access['forbidden']:
            for url in urls:
                self.assertIn(
                    client.get(url).status_code,
                    [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
                )
        # authenticated
        for client in access['allowed']:
            for url in urls:
                self.assertEqual(
                    client.get(url).status_code,
                    status.HTTP_200_OK
                )

