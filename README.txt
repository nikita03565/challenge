IRS Programming Exercise
Made with Python 3.8.5

Initial setup steps:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt

Now you can run scripts.

1. "Taking a list of tax form names"
To run the script use next command:
python collect_data.py "Form W-2" "Form 1095-C"
Arguments are space separated. If form name contains space argument must be quoted.
Output will be pretty printed in console. Sample:
$ python collect_data.py "Form W-2" "Form 1095-C"
Started...
Done!
[
    {
        "form_number": "Form W-2",
        "max_year": 2021,
        "min_year": 1954,
        "title": "Wage and Tax Statement (Info Copy Only)"
    },
    {
        "form_number": "Form 1095-C",
        "max_year": 2020,
        "min_year": 2014,
        "title": "Employer-Provided Health Insurance Offer and Coverage"
    }
]

2. "Download all PDFs"
To run the script use next command:
python download_pdfs.py "Form W-2" 2015 2021
Arguments order: Form name, start year, end year.
Arguments are space separated. If form name contains space argument must be quoted.
Output will be saved in a folder accordingly to naming rules from task description and messages "Started..." and "Done!"
will be printed in console as user's feedback.

Assumptions that were made:
- the latest version of title is included in output json
- strict case insensitive equality is used for form name comparison, i.e. if "Form W-2" is given "Form W-2 P" would be ignored
