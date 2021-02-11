import click

from utils import parse_table, get_next_link, get_page, download_pdfs, get_safe

help_string = """
\b
Searches for given form in years range and downloads pdf documents.
FORM is a string, must be in double quotes (") if contains spaces.
START and END are two integers representing range of years to search in.
Usage example: python download_pdfs.py "Form W-2" 2015 2021
"""


@click.command(context_settings=dict(help_option_names=['-h', '--help']), help=help_string)
@click.argument('form', type=str, nargs=1)
@click.argument('start', type=int, nargs=1)
@click.argument('end', type=int, nargs=1)
def execute(form, start, end):
    print('Started...')
    page = get_page(form)
    result = []
    while True:
        result.extend(parse_table(page))
        next_link = get_next_link(page)
        if next_link is None:
            break
        page = get_safe(next_link).content
    filtered = [rec for rec in result if rec['form_number'].lower() == form.lower() and start <= rec['year'] <= end]
    download_pdfs(filtered)
    print('Done!')


if __name__ == '__main__':
    execute()
