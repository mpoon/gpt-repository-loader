#!/bin/bash

# Remember you'll need to manually update the version in setup.py
# Also TWINE_USERNAME and TWINE_PASSWORD env variables should be set
python setup.py sdist bdist_wheel
twine upload dist/* --verbose