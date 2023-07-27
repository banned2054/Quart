import asyncio

from app.utils.net_utils import fetch
from app.utils.parser.mikan_parser import GetAnimeHomeUrlFromMikan, GetBangumiUrlFromMikan


async def main():
    text = await fetch('https://mikanani.me/Home/Episode/09c6270477b8beb19c76693693c74b12e7cf269e',
                       'http://127.0.0.1:7890')
    text = GetAnimeHomeUrlFromMikan(text)
    text = await fetch(text, 'http://127.0.0.1:7890')
    text = GetBangumiUrlFromMikan(text)


asyncio.run(main())
