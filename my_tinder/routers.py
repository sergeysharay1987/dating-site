from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class CustomRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/update{trailing_slash}$',
            mapping={'put': 'update'},
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Update'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/delete{trailing_slash}$',
            mapping={'delete': 'delete'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Delete'}
        ),
    ]
