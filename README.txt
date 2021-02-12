IRS Programming Exercise
Made with Python 3.8.5

Initial setup steps:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt

Now you can run scripts.

1. "Taking a list of tax form names"
To call help run this command:
$ python collect_data.py -h (or --help)
To run the script use next command:
$ python collect_data.py "Form W-2" "Form 1095-C"
Arguments are space separated. If form name contains space argument must be quoted.
Output will be pretty printed in console. Sample:
$ python collect_data.py "Form W-2" "Form 1095-C"
Started...
Found 7 matches for term "Form 1095-C"
Names of these matches are: Form 1095-C
7 matches left after filtering by name

Found 227 matches for term "Form W-2"
Names of these matches are: Form W-2C, Form W-2G, Form W-2VI, Form W-2, Form W-2 P, Form W-2GU, Form W-2AS
66 matches left after filtering by name

Done!
Result is:
[
    {
        "form_number": "Form W-2",
        "form_title": "Wage and Tax Statement (Info Copy Only)",
        "max_year": 2021,
        "min_year": 1954
    },
    {
        "form_number": "Form 1095-C",
        "form_title": "Employer-Provided Health Insurance Offer and Coverage",
        "max_year": 2020,
        "min_year": 2014
    }
]

2. "Download all PDFs"
To call help run this command:
$ python download_pdfs.py -h (or --help)
To run the script use next command:
$ python download_pdfs.py "Form 11-C" 2013 2016
And the sample output:
Started...
Found 20 matches by form name
Names of these matches are: Form 11-C
2 matches left after filtering by name and year
Downloading 2 documents...
Downloaded file https://www.irs.gov/pub/irs-prior/f11c--2016.pdf
Downloaded file https://www.irs.gov/pub/irs-prior/f11c--2013.pdf
Saved file Form 11-C/Form 11-C - 2016.pdf
Saved file Form 11-C/Form 11-C - 2013.pdf
Done!

Arguments order: Form name, start year, end year. Arguments after the third are ignored.
Arguments are space separated. If form name contains space argument must be quoted.
Output will be saved in a folder accordingly to naming rules from task description and messages "Started..." and "Done!"
will be printed in console as user's feedback.

Assumptions that were made:
- the latest version of title is included in output json,
- strict case insensitive equality is used for form name comparison, i.e. if "Form W-2" is given "Form W-2 P" would be
  ignored.
