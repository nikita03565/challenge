import asyncio

import click
from aiohttp import ClientSession

from utils import parse_table, get_next_link, get_page, download_pdfs, get_safe, get_all_found_names

help_string = """
\b
Searches for given form in years range and downloads pdf documents.
FORM is a string, must be in double quotes (") if contains spaces.
START and END are two integers representing range of years to search in.
Usage example: python download_pdfs.py "Form W-2" 2015 2021
"""


async def process_term(term):
    async with ClientSession() as session:
        page = await get_page(term, session)
        result = []
        while True:
            result.extend(parse_table(page))
            next_link = get_next_link(page)
            if next_link is None:
                break
            page = await get_safe(next_link, session)
        return result


@click.command(context_settings=dict(help_option_names=['-h', '--help']), help=help_string)
@click.argument('form', type=str, nargs=1)
@click.argument('start', type=int, nargs=1)
@click.argument('end', type=int, nargs=1)
def execute(form, start, end):
    print('Started...')
    result = asyncio.run(process_term(form))
    print(f'Found {len(result)} matches by form name')
    filtered = [rec for rec in result if rec['form_number'].lower() == form.lower() and start <= rec['year'] <= end]
    found_names = get_all_found_names(result)
    if found_names:
        print(f'Names of these matches are: {", ".join(found_names)}')
        print(f'{len(filtered)} matches left after filtering by name and year')
    if filtered:
        print(f'Downloading {len(filtered)} documents...')
        asyncio.run(download_pdfs(filtered))
    else:
        print('No documents to download')
    print('Done!')


if __name__ == '__main__':
    execute()
