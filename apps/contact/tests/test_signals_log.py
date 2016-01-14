from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.contact.models import Owner, ModelsChangesLog


class ModelsChangesLoger(TestCase):
    """Test models actions(create/edit/delete) signals."""
    def test_signlas_log(self):
        """Test site and contact.html content."""
        # test create action
        def clear(log):
            try:
                log.objects.all().delete()
                self.assertEqual(ModelsChangesLog.objects.count(), 0)
                return True
            except AssertionError as err:
                print 'Assertion Error: ', err

        if clear(ModelsChangesLog):
            response = self.client.get(reverse('contact'))
            self.assertEqual(response.status_code, 200)
            obj = ModelsChangesLog.objects.first()
            self.assertEqual(obj.model_name, 'UsersRequest')
            self.assertEqual(obj.action, 'create')
        # test edit action
        owner = Owner.objects.create(
            first_name='Vasja',
            last_name='Pupkin',
            birthday='1965-12-02',
            bio='Nurilsk',
            email='rdb@yans.com',
            skype='lock_lom',
            jabber='vasja@nurilsk.com'
        )
        owner.save()
        if clear(ModelsChangesLog):
            owner.first_name = 'NotVasja'
            owner.save()
            obj = ModelsChangesLog.objects.first()
            self.assertEqual(obj.model_name, 'Owner')
            self.assertEqual(obj.action, 'edit')
        # test delete action
        if clear(ModelsChangesLog):
            owner.delete()
            obj = ModelsChangesLog.objects.first()
            self.assertEqual(obj.model_name, 'Owner')
            self.assertEqual(obj.action, 'delete')
