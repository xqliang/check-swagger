from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import codecs
import os
import sys
import urllib
import urlparse
from fnmatch import fnmatch

import swagger_spec_validator.util
import yaml
from swagger_spec_validator.common import SwaggerValidationError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--exclude', action='append', metavar='PATTERN')
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args()

    for filename in args.filenames:
        try:
            if any(fnmatch(filename, pat) for pat in args.exclude or ()):
                continue
            with codecs.open(filename, encoding='utf-8') as f:
                path = os.path.abspath(filename)
                url = urlparse.urljoin(u'file:', urllib.pathname2url(path))
                spec = yaml.safe_load(f)
                if not isinstance(spec, dict):
                    raise SwaggerValidationError('root node is not a mapping')
                validator = swagger_spec_validator.util.get_validator(spec, url)
                validator.validate_spec(spec, url)
        except yaml.YAMLError as exc:
            print('{}: invalid YAML'.format(filename))
            print(exc)
            return 1
        except Exception as exc:
            print('{}: invalid Swagger Spec'.format(filename))
            print(exc)
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
