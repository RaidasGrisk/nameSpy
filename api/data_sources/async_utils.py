import aiohttp
import asyncio


# TODO: if requests fails it returns ClientHttpProxyError object
# TODO: can not pass it further, should fix it here by making the call again and retrieving the response
def make_async_requests(urls, proxies=None):

    proxy = proxies.get('http') if proxies else ''

    async def fetch(session, url, proxy):

        # setting a timeout for bad proxies
        timeout = aiohttp.ClientTimeout(total=5)

        # setting 5 retries in case of proxy fail
        # sometimes the url (due to proxies) is unreachable
        # TODO: should specify the exact exception(s) as this could be due to other reasons
        for _ in range(5):
            try:
                async with session.get(url, proxy=proxy, timeout=timeout) as response:
                    return await response.text()
            except Exception as e:  # TODO: aiohttp.ClientError
                print(str(e))

    async def fetch_all(urls, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            results = await asyncio.gather(*[fetch(session, url, proxy) for url in urls], return_exceptions=True)
            return results

    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(fetch_all(urls, loop))

    return responses

# ----------------- #
#
#
# # ----------- #
# # call APIs to collect data
# # https://stackoverflow.com/questions/51726007/fetching-multiple-urls-with-aiohttp-in-python
# import aiohttp
# import asyncio
#
# proxies = {'http': 'http://f3t0zfun:03qLGKGeOdrkbiTE@proxy.proxy-cheap.com:31112',
#            'https': 'http://f3t0zfun:03qLGKGeOdrkbiTE@proxy.proxy-cheap.com:31112'}
#
# proxy = proxies.get('http')
#
# async def fetch(session, url, proxy):
#     async with session.get(url, proxy=proxy) as response:
#         return await response.json()
#
#
# async def fetch_all(urls, loop):
#     async with aiohttp.ClientSession(loop=loop, proxy=proxy) as session:
#         results = await asyncio.gather(*[fetch(session, url, proxy) for url in urls], return_exceptions=True)
#         return results
#
#
# loop = asyncio.get_event_loop()
# urls = ['http://ip-api.com/json/' for _ in range(3)]
# responses = loop.run_until_complete(fetch_all(urls, loop))
# [print(i) for i in responses]
#
#
# # -------- #
# # https://stackoverflow.com/questions/61537570/how-do-i-make-parallel-async-http-requests-using-httpx-versus-aiohttp-in-pytho
# import asyncio
# import httpx
#
# proxies = {'http': 'http://f3t0zfun:03qLGKGeOdrkbiTE@proxy.proxy-cheap.com:31112',
#            'https': 'http://f3t0zfun:03qLGKGeOdrkbiTE@proxy.proxy-cheap.com:31112'}
#
#
# async def fetch(session, url):
#     response = await session.request(method='GET', url=url)
#     return response
#
#
# async def get_requests_asynch(urls):
#     async with httpx.AsyncClient(proxies=proxies) as session:
#         htmls = await asyncio.gather(*[fetch(session, url) for url in urls])
#     return htmls
#
#
# loop = asyncio.get_event_loop()
# urls = ['http://ip-api.com/json/' for _ in range(3)]
# htmls = loop.run_until_complete(get_requests_asynch(urls))
# [print(i.text) for i in htmls]
#
# # -------- #
# # https://stackoverflow.com/questions/30837839/how-can-i-set-a-single-proxy-for-a-requests-session-object
# import requests
#
# proxies = {'http': 'http://f3t0zfun:03qLGKGeOdrkbiTE@proxy.proxy-cheap.com:31112',
#            'https': 'http://f3t0zfun:03qLGKGeOdrkbiTE@proxy.proxy-cheap.com:31112'}
#
# urls = ['http://ip-api.com/json/' for _ in range(3)]
#
# session = requests.session()
# session.proxies.update(proxies)
# for url in urls:
#     r = session.get(url)
#     print(r.json())

