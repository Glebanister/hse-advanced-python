#!/usr/bin/env python3

import aiohttp
import aiofiles
import asyncio
import argparse
import sys

from pathlib import Path
from typing import IO


async def download_cat_pics(n_pictures: int, out: Path, log_file: IO):
    def log(*args, **kwargs):
        kwargs['file'] = log_file
        print(*args, **kwargs)

    async with aiohttp.ClientSession() as session:
        out.mkdir(exist_ok=True)
        url = 'https://thiscatdoesnotexist.com'
        for picture_id in range(1, n_pictures + 1):
            async with session.get(url) as response:
                if str(response.status)[0] != '2':
                    log(f'Not success response status: {response.status}')
                    continue

                picture_path = (
                    out / 'cat_{:04d}'.format(picture_id)
                ).with_suffix('.jpg')

                f = await aiofiles.open(picture_path, mode='wb')
                await f.write(await response.read())
                await f.close()
                log(f'Picture downloaded: {picture_path}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('n_pictures', type=int,
                        help='Number of pictures to download')
    parser.add_argument('out', type=Path, help='Path to the output directory')
    return parser.parse_args()


def main():
    args = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_cat_pics(args.n_pictures, args.out, sys.stdout))


if __name__ == '__main__':
    main()
