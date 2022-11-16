from rest_framework.routers import DefaultRouter, Route


class CustomRouter(DefaultRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^list$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/update$',
            mapping={'put': 'update'},
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Update'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/delete$',
            mapping={'delete': 'destroy'},
            name='{basename}-delete',
            detail=True,
            initkwargs={'suffix': 'Delete'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/match$',
            mapping={'post' or 'put': 'add-liked-user'},
            name='{basename}-add_liked_user',
            detail=True,
            initkwargs={}
        )
    ]
