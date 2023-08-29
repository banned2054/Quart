import asyncio

from app.utils.parser.bangumi_parser import get_episode_list


async def main():
    await get_episode_list(105075)


asyncio.run(main())
