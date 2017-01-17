from __future__ import absolute_import

import json

from django.db import models
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, FieldRowPanel,
                                                InlinePanel, MultiFieldPanel,
                                                ObjectList, TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import PageManager

from jobmanager.models.django import JobCategory, JobRegion
from v1.models import CFGOVPage


class JobListingPage(CFGOVPage):
    description = RichTextField('Description')
    open_date = models.DateField('Open date')
    close_date = models.DateField('Close date')
    salary_min = models.DecimalField('Minimum salary', max_digits=11,
                                     decimal_places=2)
    salary_max = models.DecimalField('Maximum salary', max_digits=11,
                                     decimal_places=2)
    division = models.ForeignKey(JobCategory, on_delete=models.PROTECT,
                                 null=True)
    region = models.ForeignKey(JobRegion, related_name='job_listings',
                               on_delete=models.PROTECT)

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('division', classname='full'),
            InlinePanel('grades', label='Grades'),
            FieldPanel('region', classname='full'),
            FieldRowPanel([
                FieldPanel('open_date', classname='col6'),
                FieldPanel('close_date', classname='col6'),
            ]),
            FieldRowPanel([
                FieldPanel('salary_min', classname='col6'),
                FieldPanel('salary_max', classname='col6'),
            ]),
        ], heading='Details'),
        FieldPanel('description', classname='full'),
        InlinePanel(
            'usajobs_application_links',
            label='USAJobs application links'
        ),
        InlinePanel(
            'email_application_links',
            label='Email application links'
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'job-description-page/index.html'

    objects = PageManager()

    @property
    def ordered_grades(self):
        """Return a list of job grades in numerical order.

        Non-numeric grades are sorted alphabetically after numeric grades.
        """
        grades = set(g.grade.grade for g in self.grades.all())
        return sorted(grades, key=lambda g: int(g) if g.isdigit() else g)

    @property
    def json_ld(self):
        """Generate valid JSON-LD for this job posting.

        For reference:

            http://json-ld.org/spec/latest/json-ld/
            https://schema.org/JobPosting

        """
        return json.dumps({
            '@context': 'http://schema.org',
            '@type': 'JobPosting',
            'url': self.full_url,
            'title': self.title,
            'description': self.description,
            'baseSalary': {
                '@type': 'PriceSpecification',
                'minPrice': int(self.salary_min),
                'maxPrice': int(self.salary_max),
                'priceCurrency': 'USD',
            },
            'salaryCurrency': 'USD',
            'jobLocation': {
                '@type': 'Place',
                'name': self.region.name,
            },
        })
