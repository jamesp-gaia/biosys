import json

from django.contrib.gis.geos import GEOSGeometry
from django.core.urlresolvers import reverse
from rest_framework import status

from main.models import Form
from main.tests import factories
from main.tests.api import helpers


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



