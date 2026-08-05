# Impact Earth (Flask Port)

A Flask-based port of the Impact: Earth! calculator, with Jinja templates and static assets for impact effect modelling outputs.

## Quick Start

Requirements:
- Python 3.10+

From the repository root:

1. Create a virtual environment.
	python3 -m venv .venv

2. Activate it.
	source .venv/bin/activate

3. Install dependencies.
	pip install -r requirements.txt

4. Run the Flask app.
	flask --app main run --host=0.0.0.0 --port=5000

5. Open in your browser.
	http://127.0.0.1:5000/

## Tests

Run the test suite from the repository root:

pytest

## Licence

This project is licensed under the Apache License, Version 2.0.
See the LICENSE file for full terms.
