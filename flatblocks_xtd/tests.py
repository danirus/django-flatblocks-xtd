#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from django import db

from flatblocks_xtd.models import FlatBlockXtd
from flatblocks_xtd import settings


class BasicTests(TestCase):
    urls = 'flatblocks_xtd.urls'

    def setUp(self):
        self.testblock = FlatBlockXtd.objects.create(
             slug='block',
             header='HEADER',
             content='CONTENT'
        )
        self.admin = User.objects.create_superuser(
            'admin2', 'admin@localhost', 'adminpwd')

    def testURLConf(self):
        # We have to support two different APIs here (1.1 and 1.2)
        def get_tmpl(resp):
            if hasattr(resp, 'template') and isinstance(resp.template, list):
                return resp.template[0]
            elif hasattr(resp, 'templates'):
                return resp.templates[0]
            return resp.template
        self.assertEqual(get_tmpl(self.client.get('/edit/1/')).name, 
                          'admin/login.html')
        self.client.login(username='admin2', password='adminpwd')
        self.assertEqual(get_tmpl(self.client.get('/edit/1/')).name, 
                          'flatblocks_xtd/edit.html')

    def testCacheReset(self):
        """
        Tests if FlatBlockXtd.save() resets the cache.
        """
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" 60 %}')
        tpl.render(template.Context({}))
        name = '%sblock' % settings.CACHE_PREFIX
        self.assertNotEqual(None, cache.get(name))
        block = FlatBlockXtd.objects.get(slug='block')
        block.header = 'UPDATED'
        block.save()
        self.assertEqual(None, cache.get(name))

    def testSaveKwargs(self):
        block = FlatBlockXtd(slug='missing')
#        block.slug = 'missing'
        self.assertRaises(ValueError, block.save, force_update=True)
        block = FlatBlockXtd.objects.get(slug='block')
        self.assertRaises(db.IntegrityError, block.save, force_insert=True)


class TagTests(TestCase):
    def setUp(self):
        self.testblock = FlatBlockXtd.objects.create(
             slug='block',
             header='HEADER',
             content='CONTENT'
        )

    def testLoadingTaglib(self):
        """Tests if the taglib defined in this app can be loaded"""
        tpl = template.Template('{% load flatblock_xtd_tags %}')
        tpl.render(template.Context({}))

    def testExistingPlain(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% plain_flatblock_xtd "block" %}')
        self.assertEqual('CONTENT', tpl.render(template.Context({})).strip())

    def testExistingTemplate(self):
        expected = """<div class="flatblock-xtd block-block">

    <h2 class="title">HEADER</h2>

    <div class="content">CONTENT</div>
</div>
"""
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})))

    def testUsingMissingTemplate(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" using "missing_template.html" %}')
        exception = template.TemplateSyntaxError
        self.assertRaises(exception, tpl.render, template.Context({}))

    def testSyntax(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" %}')
        tpl.render(template.Context({}))
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" 123 %}')
        tpl.render(template.Context({}))
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" '
            'using "flatblocks_xtd/flatblock_xtd.html" %}')
        tpl.render(template.Context({}))
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}'
            '{% flatblock_xtd "block" 123 '
            'using "flatblocks_xtd/flatblock_xtd.html" %}')
        tpl.render(template.Context({}))

    def testBlockAsVariable(self):
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd blockvar %}')
        tpl.render(template.Context({'blockvar': 'block'}))


class AutoCreationTest(TestCase):
    """ Test case for block autcreation """

    def testMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name will be auto-created"""
        expected = """<div class="flatblock-xtd block-foo">

    <div class="content">foo</div>
</div>"""
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "foo" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlockXtd.objects.count(), 1)
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlockXtd.objects.count(), 1)

    def testNotAutocreatedMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name won't be auto-created if feature is disabled"""
        expected = ""
        settings.AUTOCREATE_STATIC_BLOCKS = False
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlockXtd.objects.filter(slug='block').count(), 0)

    def testMissingVariableBlock(self):
        settings.AUTOCREATE_STATIC_BLOCKS = True
        """Tests if a missing block with variable name will simply return an empty string"""
        tpl = template.Template(
            '{% load flatblock_xtd_tags %}{% flatblock_xtd name %}')
        self.assertEqual('', 
                         tpl.render(template.Context({'name': 'foo'})).strip())
