from klein import run, route, Klein
app = Klein()
import json
import treq
import xmltodict
from twisted.internet import reactor, defer

def get_ceneo_availability(x):
    d = {'1':'in-stock','3':'in-stock','7':'in-stock','90':'pre-sale','99':'no-info'}
    return d.get(x,None)

def read_ceneo_v2(d):
    results = []
    for x in d['offers']['o']:
        p = {
            'title':x.get('name',None),
            'image':x['imgs']['main'] if 'imgs' in x else None,
            'description':x.get('desc',None),
            'price':x.get('@price',None),
            'availability': get_ceneo_availability(x.get('@avail',None)),
            'quantity':x.get('@stock',None),
            'link':x.get('@url',None)
        }
        results.append(p)
    return results

def read_google_shopping(d):
    results = []
    for x in d['rss']['channel']['item']:
        p = {
            'title':x.get('title',None),
            'description':x.get('description',None),
            'link': x.get('link',None),
            'image':x.get('g:image_link',None),
            'price':x.get('g:price',None),
            'brand':x.get('g:brand',None),
            'availability':x.get('g:availability',None),
            'condition':x.get('g:condition',None),
            'quantity':x.get('g:quantity',None)
        }
        results.append(p)
    return results

# def read_atom(d):
#     results = []
#         for x in d['feed']['entry']:
#             p = {
#                 'name':x.get('title',None),
#                 'description':x.get('summary',None),
#                 'link': x['link'].get('@href',None) if isinstance(x['link'],dict) else None 
#                 'image':x.get('g:image_link',None),
#                 'price':x.get('g:price',None),
#             }
#             results.append(p)
#         return results    


def read_csv(content, delim=','):
    import csv
    content = content.decode('utf-8').split('\n')
    reader = csv.DictReader(content,delimiter = delim)
    header = reader.fieldnames
    columns = ['title','description','price','condition','link','availability']
    results = []
    if set(columns).issubset(set(header)):
        for row in reader:
            p = {
                'title': row.get('title',None),
                'description':row.get('description',None),
                'price': row.get('price',None),
                'condition':row.get('condition',None),
                'link': row.get('link',None),
                'availability': row.get('availability',None),
                'image': row.get('image link',row.get('image_link',None))
            }
            results.append(p)
        return results
    else:
        return []


def read_any_feed(content, url):
    content = content.decode('utf-8')
    if content[0] == '<' or url.endswith('xml'):
        d = xmltodict.parse(content)
        if 'offers' in  d:
            return read_ceneo_v2(d)
        else:
            return read_google_shopping(d)
    elif url.endswith('.csv'):
        return read_csv(content,delim=',')
    else:
        return read_csv(content,delim='\t')


@defer.inlineCallbacks
def return_info(response):
    text = yield response.content()
    v = read_any_feed(text, response.request.absoluteURI.decode('utf-8')) 
    return json.dumps(v)


@app.route("/read", methods=['POST'])
def get_category(request):
    content = json.loads(request.content.read())
    url = content['url']
    d = treq.get(url)
    d.addCallback(return_info)
    return d

resource = app.resource

app.run("0.0.0.0", 5007)
