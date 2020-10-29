from fastapi import APIRouter
from db import db_client
import json

router = APIRouter()


@router.get('/api_calls_count')
async def get_count(filter=None):
    # try except any error because
    # the app will crash if:
    # 1. filter is invalid on the db end
    # 2. filter is not a json
    # could exclude filter but feel that
    # it adds functionality to keep it
    try:
        if filter is None:
            filter = {}
        else:
            filter = json.loads(filter)
        call_count = await db_client['logs']['api_calls'].count_documents(filter)
        return call_count
    except Exception as e:
        return str(e)