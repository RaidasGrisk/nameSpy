import aiohttp
import asyncio
from log_cofig import logger


def make_async_requests(urls, proxies=None):

    proxy = proxies.get('http') if proxies else ''

    async def fetch(session, url, proxy):

        # setting a timeout for bad proxies
        timeout = aiohttp.ClientTimeout(total=5)

        # setting 5 retries in case of proxy fail
        # sometimes the url (due to proxies) is unreachable
        for i in range(5):
            logger.info(f'Gathering single async request: {i}')
            try:
                async with session.get(url, proxy=proxy, timeout=timeout) as response:
                    logger.info(f'Gathering single async request: successfully received a response')
                    return await response.text()
            except Exception as e:
                # TODO: setting to logger.exception breaks everything !?
                # by not continuing the for loop and stopping just before the below line
                logger.info(f'Single async requests exception: {repr(e)}')

    async def fetch_all(urls, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            logger.info('Gathering async requests')
            results = await asyncio.gather(*[fetch(session, url, proxy) for url in urls], return_exceptions=True)
            return results

    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(fetch_all(urls, loop))

    return responses

# ----------------- #
# testing

# logger.handlers[0].flush()
# make_async_requests(['http://www.dasdasdasdasdasd.asd', 'https://www.namespy.dev'])
# [print(i) for i in logger.handlers[0].log]