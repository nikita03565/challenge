import asyncio

import click
from aiohttp import ClientSession

from utils import (
    parse_table, get_dict_data, get_next_link, pretty_print, get_page, get_safe, get_all_found_names, filter_none
)

help_string = """
\b
Searches for given terms and prints results as json in console.
Terms a given as space separated list of strings. 
If string contains spaces it must be in double quotes (").
Usage example: python collect_data.py "Form W-2" "Form 1095-C"
"""


async def process_term(term, session):
    res = []
    page = await get_page(term, session)
    while True:
        res.extend(parse_table(page))
        next_link = get_next_link(page)
        if next_link is None:
            break
        page = await get_safe(next_link, session)

    filtered = [d for d in res if d['form_number'].lower() == term.lower()]
    found_names = get_all_found_names(res)
    print(f'Found {len(res)} matches for term \"{term}\"')
    if found_names:
        print(f'Names of these matches are: {", ".join(found_names)}')
        print(f'{len(filtered)} matches left after filtering by name\n')
    if filtered:
        data = get_dict_data(filtered)
        return data


async def process_terms(search_terms):
    async with ClientSession() as session:
        tasks = [asyncio.create_task(process_term(term, session)) for term in search_terms]
        return await asyncio.gather(*tasks)


@click.command(context_settings=dict(help_option_names=['-h', '--help']), help=help_string)
@click.argument('search_terms', type=str, nargs=-1)
def execute(search_terms):
    print('Started...')
    result = filter_none(asyncio.run(process_terms(search_terms)))
    print('Done!\nResult is:')
    pretty_print(result)


if __name__ == '__main__':
    execute()
