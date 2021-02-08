made with Python 3.8.5

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py "Form W-2" "Form 1095-C"

python download.py "Form W-2" 2015 2021

Assumptions that were made:
- the latest version of title is included in output json
- strict equality is used for form name comparison, i.e.  if "Form W-2" is given "Form W-2 P" would be ignored
