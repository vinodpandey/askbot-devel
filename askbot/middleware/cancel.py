from django.http import HttpResponseRedirect
from django.conf import settings

DEFAULT_NEXT = '/' + getattr(settings, 'ASKBOT_URL')
def clean_next(next, default = None):
    if next is None or not next.startswith('/'):
        if default:
            return default
        else:
            return DEFAULT_NEXT
    if isinstance(next, str):
        next = unicode(urllib.unquote(next), 'utf-8', 'replace')
    next = next.strip()
    logging.debug('next url is %s' % next)
    return next

def get_next_url(request, default = None):
    return clean_next(request.REQUEST.get('next'), default)


class CancelActionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'cancel' in request.REQUEST:
            #todo use session messages for the anonymous users
            try:
                msg = getattr(view_func,'CANCEL_MESSAGE')
            except AttributeError:
                msg = 'action canceled'
            request.user.message_set.create(message=unicode(msg))
            return HttpResponseRedirect(get_next_url(request))
        else:
            return None
