from flags.conditions import RequiredForCondition


def page_primary_key_condition(primary_key, request=None, **kwargs):
    """ Does the requested page match the given primary key? """
    if request is None:
        raise RequiredForCondition(
            "request is required for condition 'page primary key'"
        )

    try:
        pk = int(primary_key)
    except ValueError:
        return False

    path = request.path
    path_components = [
        component for component in path.split('/') if component
    ]
    page, args, kwargs = request.site.root_page.specific.route(
        request, path_components)

    return page.pk == pk
