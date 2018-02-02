from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Page


def run():

    print "# Groups "
    for group in Group.objects.all():
        user_q = group.user_set.filter(is_active=True)

        if user_q.count() == 0:
            continue

        print "## " + group.name

        print "### members"

        for user in user_q:
            print "- " + user.username

        for page in Page.objects.filter(group_permissions__group=group
                                        ).distinct():
            print "###   under page %s (%s):" % (page.title, page.url_path)
            permissions = group.page_permissions.filter(page=page)

            for perm in permissions:
                print "- " + perm.get_permission_type_display()

        print "### model permissions"
        for ctype in ContentType.objects.filter(permission__group=group
                                                ).distinct():
            ct_perms = group.permissions.filter(content_type=ctype)
            compact_names = [perm.codename.split('_')[0] for perm in ct_perms]
            print "- %s.%s (%s)" % (ctype.app_label,
                                    ctype.model,
                                    ','.join(compact_names))

    print "# Users"
    users = User.objects.filter(is_active=True)

    for user in users:
        if not (user.is_superuser or user.user_permissions.all().exists()):
            # nothing to say about users without extra privs
            continue
        print "## " + user.username

        if user.is_superuser:
            print user.username + " is an administrator"

        if user.user_permissions.all().count() > 0:
            print "### model permissions:"

            for ctype in ContentType.objects.filter(permission__user=user
                                                    ).distinct():
                ct_perms = user.user_permissions.filter(content_type=ctype)
                compact_names = [perm.codename.split('_')[0] for perm in ct_perms]
                print "- %s.%s (%s)" % (ctype.app_label,
                                        ctype.model,
                                        ','.join(compact_names))
