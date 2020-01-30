# CORS API Proxy

Just one more simple proxy that remove CORS restrictions for API requests 

## Usage

Dev mode (use Flask server):
```
python cors_api_proxy
```

Prod mode (use WSGI server):
```
python cors_api_proxy prod
```

*Watch Requests* option:
```
python cors_api_proxy watch_reqs
python cors_api_proxy prod watch_reqs
```
The option is used for checking if long requests are still in processing.
Specifically, it's the only way to know when uploading a file to the
server have been finished.

To use this function just add uniq *reqid* key to your request. E.g.:
```
http://proxy_url:port/your_api_link?reqid=<uuid>
```
Then you may check if the request is still in processing:
```
http://proxy_url:port/your_api_link?reqid=<uuid>&test=true
```
If it is still in, you'll get the response with the status code **204**.
Otherwise, you'll get the status **404**.
