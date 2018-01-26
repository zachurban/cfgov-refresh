from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Page


def run():
    users = User.objects.filter(is_active=True)

    for user in users:
        print user.username
        if user.is_superuser:
            print " no restrictions"
            continue

        if user.user_permissions.all().count() > 0:
            print " user-specific permissions:"
            for permission in user.user_permissions.all():
                print permission

        for group in user.groups.all():
            print " as a member of " + group.name

            for page in Page.objects.filter(group_permissions__group=group).distinct():
                print "   under page %s (%s):" % (page.title, page.url_path)
                permissions = group.page_permissions.filter(page=page)

                for perm in permissions:
                    print "    " + perm.get_permission_type_display()

            print "    has these model permissions:"
            for ct in ContentType.objects.filter(permission__group=group).distinct():
                print "     %s.%s:" % (ct.app_label, ct.model)
                for permission in group.permissions.filter(content_type=ct):
                    print "      " + permission.name
