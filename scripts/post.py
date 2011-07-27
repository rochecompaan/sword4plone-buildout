import sys
import os
import httplib
from urlparse import urlparse
from base64 import encodestring

def submitfile(name, url, contenttype):
    fp = open(name, 'r')
    body = fp.read()
    fp.close()

    scheme, netloc, path, params, query, fragment = urlparse(url)
    h = httplib.HTTPConnection(netloc)
    h.putrequest('POST', path)
    h.putheader('Authorization', 'Basic %s' % encodestring('admin:admin'))
    h.putheader('Content-Type', contenttype)
    h.putheader('Content-Length', str(len(body)))
    h.putheader('Content-Disposition', 'attachment; filename=%s' % os.path.basename(name))
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    status = response.status
    response.read()
    if status / 100 != 2:
        return False
    return True

def main():
    try:
        name = sys.argv[1]
        contenttype = sys.argv[2]
        url = sys.argv[3]
    except IndexError:
        print >>sys.stderr, "Usage: %s filename content_type url" % sys.argv[0]
        sys.exit(1)

    print ['Fail', 'Success'][submitfile(name, url, contenttype)]

if __name__ == '__main__':
    main()
