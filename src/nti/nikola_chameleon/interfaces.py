# -*- coding: utf-8 -*-
"""
Interfaces for rendering Nikola with chameleon.

The most important interface in this package for themes is
:class:`IPageKind` and its various subclasses. These function
similarly to `IBrowserLayer` in a Zope 3 application, in that they are
applied to the ``request`` variable when a template is rendered, and
more specific templates or macros can be registered for the request
based on that layer. Each request will only have one such interface
applied to it.


Similarly, the :class:`ICommentKind` (with its subclasses
:class:`ICommentKindNone` and :class:`ICommentKindAllowed` and *its*
various system types markers) will be applied to the ``view`` variable.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from nikola.post import Post
from zope import interface
from zope.viewlet.interfaces import IViewletManager

class IPost(interface.Interface):
    """
    A post.
    """

interface.classImplements(Post, IPost)

class IPageKind(interface.Interface):
    """
    The type of page being rendered.

    Specific types of pages will have a more specific
    interface.

    This is similar to IBrowserLayer concept in Zope 3.
    """

    interface.taggedValue('__pagekinds__', ())

class IListPageKind(IPageKind):
    "A page that is a list"
    # 'list' in pagekind
    interface.taggedValue('__pagekinds__', (u'list',))

# It turns out inheriting from IListPageKind is not a good idea,
# there are some pages that are *just* lists and nothing else, and
# if we try to register for them we pick up all the subclasses.
# Archives are the one exception.

class IAuthorsPageKind(IPageKind):
    "The page for listing authors"

    # 'list' and 'authors_page' in pagekind
    interface.taggedValue('__pagekinds__', (u'list', u'authors_page'))

class IAuthorPageKind(IPageKind):
    "The page for listing an author"

    # 'list' and 'author_page' in pagkeind
    interface.taggedValue('__pagekinds__', (u'list', u'author_page'))

class ITagsPageKind(IPageKind):
    "The page for listing tags"

    # 'list' and 'tags_page' in pagekind
    interface.taggedValue('__pagekinds__', (u'list', u'tags_page'))

class ITagPageKind(IPageKind):
    """The page for listing a tag"""

    # 'list' and 'tag_page' in pagkeind
    interface.taggedValue('__pagekinds__', (u'list', u'tag_page'))

class IGalleryPageKind(IPageKind):
    """A gallery page"""

    # 'gallery_page' in pagkeind
    interface.taggedValue('__pagekinds__', (u'gallery_page',))

class IListingPageKind(IPageKind):
    """A listing page"""

    # 'listing' in pagkeind
    interface.taggedValue('__pagekinds__', (u'listing',))

class IArchivePageKind(IListPageKind):
    """An archive page"""

    # 'list' and 'archive_page' in pagekind
    interface.taggedValue('__pagekinds__', (u'list', u'archive_page'))

class IIndexPageKind(IPageKind):
    """An index page"""

    # 'index' in pagkekind
    interface.taggedValue('__pagekinds__', (u'index',))

class IMainIndexPageKind(IIndexPageKind):
    """The main index"""

    # 'index' and 'main_index' in pagkeind
    interface.taggedValue('__pagekinds__', (u'index', u'main_index'))

class IArchiveIndexPageKind(IIndexPageKind,
                            IArchivePageKind):
    """
    When archives are indexes.

    ARCHIVES_ARE_INDEXES = True
    """

    interface.taggedValue('__pagekinds__', (u'index', u'archive_page'))

class IPostPageKind(IPageKind):
    """A blog post"""

    # 'post_page' in pagekind
    interface.taggedValue('__pagekinds__', (u'post_page',))

class IPagePageKind(IPageKind):
    """A page"""

    # 'page_page' in pagekind
    interface.taggedValue('__pagekinds__', (u'page_page',))

class IStoryPageKind(IPagePageKind):
    """A story page"""

    # 'story_page' and 'page_page' in pagekind
    interface.taggedValue('__pagekinds__', (u'page_page', u'story_page',))

class IBookPageKind(IStoryPageKind):
    """
    A book page. Note that this doesn't actually have
    its own pagekinds value, it's specified by
    setting 'template:book.tmpl' in the post metadata.
    """
    interface.taggedValue('__pagekinds__', (u'page_page',
                                            u'story_page',
                                            u'book_page'))

class IPostPage(IPost, IPageKind):
    """
    A page being rendered by a post.
    """

    interface.taggedValue('__pagekinds__', ())

def _build(iface, result, tag='__pagekinds__', tx=lambda x: x):
    __traceback_info__ = iface, tag
    kinds = iface.getTaggedValue(tag)
    kinds = tx(kinds)
    if kinds in result and kinds: # pragma: no cover
        if result[kinds] is iface:
            # Multiple inheritance
            return
        raise ValueError("Duplicate %s" % tag, kinds, iface)

    if kinds not in result:
        result[kinds] = iface

    for sub in iface.dependents.keys():
        _build(sub, result, tag, tx)

    return result


PAGEKINDS = {}


class ICommentKind(interface.Interface):
    """
    The type of comments for a given view.
    """

class ICommentKindNone(interface.Interface):
    """
    No comments are allowed on this view.
    """

class ICommentKindAllowed(interface.Interface):
    """
    Comments are allowed on this view.
    """

    interface.taggedValue('__comment_system__', None)

class ICommentKindDisqus(ICommentKindAllowed):
    """
    Use disqus comments.
    """
    interface.taggedValue('__comment_system__', 'disqus')

COMMENTSYSTEMS = {}


###
# Viewlet managers. We can't specify a specific viewlet manager type
# for every possible part of the page, but we can specify some common ones.
# This should help avoid name clashes.
###

class IHtmlHeadViewletManager(IViewletManager):
    """
    A viewlet manager meant to be used in the <head>.
    """

class IHtmlBodyContentViewletManager(IViewletManager):
    """
    A viewlet that operates anywhere within the main content of the
    body.
    """

class IHtmlBodyContentHeaderViewletManager(IViewletManager):
    """
    A viewlet that operates within a header in the main content
    of the body (before the main content).
    """

class IHtmlBodyContentFooterViewletManager(IViewletManager):
    """
    A viewlet that operates within a footer in the main content
    of the body (after the main content).
    """

class IHtmlBodyFooterViewletManager(IViewletManager):
    """
    A viewlet that operates after the main body content, near the very end of
    the html <body> tag.
    """

def _cleanUp():
    PAGEKINDS.clear()
    PAGEKINDS.update(_build(IPageKind, {}, tx=frozenset))
    COMMENTSYSTEMS.clear()
    COMMENTSYSTEMS.update(_build(ICommentKindAllowed,
                                 {}, '__comment_system__'))


_cleanUp()

try:
    from zope.testing import cleanup
except ImportError:
    pass
else:
    cleanup.addCleanUp(_cleanUp)
