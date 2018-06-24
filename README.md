# Products Feed Reader

Simple API to parse any products feed

## Currently supported feeds:

XMLs:
* CeneoV2
* GoogleShopping

## Requirement

Python3 or docker machine

## Run API

### Manual 

```bash
git clone git@github.com:digestoo/products-feed-reader.git
cd products-feed-reader
pip install -r requirements.txt
python api.py
```

### Docker

```bash
docker pull mdruzkowski/products-feed-reader
docker run -it -p 5007:5007 mdruzkowski/products-feed-reader
```

##  Details of supported endpoints

### read

```bash
curl -XPOST -H "Content-Type: application/json"  -d '{"url":"link_to_product_feed"}'  http://localhost:5007/read
```

POST params:

- `url` - Product feed url

Returns list of products.
