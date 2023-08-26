import asyncio

from app.utils.parser.bangumi_parser import get_subject_info


async def main():
    await get_subject_info(373247)


asyncio.run(main())
