from fastapi import APIRouter
from private import secret_endpoints
import aiohttp

router = APIRouter()

# HTTP responses
# Informational responses (100–199)
# Successful responses (200–299)
# Redirects (300–399)
# Client errors (400–499)
# and Server errors (500–599)


async def get_url_status_code(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                # print(await resp.text())
                return resp.status
        except aiohttp.ClientConnectorError:
            return 600  # the code does not exist but will do


@router.get("/gateway_status")
async def gateway_status():
    url = 'https://namespy-api-mu7u3ykctq-lz.a.run.app'
    status_code = await get_url_status_code(url)
    return {'status_code': status_code, 'is_up': status_code < 500}


@router.get("/webscore_status")
async def webscore_status():
    url = secret_endpoints['web_score']
    status_code = await get_url_status_code(url)
    return {'status_code': status_code, 'is_up': status_code < 500}


@router.get("/jobtitle_status")
async def jobtitle_status():
    url = secret_endpoints['job_title']
    status_code = await get_url_status_code(url)
    return {'status_code': status_code, 'is_up': status_code < 500}
