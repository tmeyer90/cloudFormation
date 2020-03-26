"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
import json
from cfnlint.rules import Match


class BaseFormatter(object):
    """Base Formatter class"""

    def _format(self, match):
        """Format the specific match"""

    def print_matches(self, matches):
        """Output all the matches"""
        if not matches:
            return None

        # Output each match on a separate line by default
        output = []
        for match in matches:
            output.append(self._format(match))

        return '\n'.join(output)


class Formatter(BaseFormatter):
    """Generic Formatter"""

    def _format(self, match):
        """Format output"""
        formatstr = u'{0} {1}\n{2}:{3}:{4}\n'
        return formatstr.format(
            match.rule.id,
            match.message,
            match.filename,
            match.linenumber,
            match.columnnumber
        )


class JsonFormatter(BaseFormatter):
    """Json Formatter"""

    class CustomEncoder(json.JSONEncoder):
        """Custom Encoding for the Match Object"""
        # pylint: disable=E0202

        def default(self, o):
            if isinstance(o, Match):
                if o.rule.id[0] == 'W':
                    level = 'Warning'
                elif o.rule.id[0] == 'I':
                    level = 'Informational'
                else:
                    level = 'Error'

                return {
                    'Rule': {
                        'Id': o.rule.id,
                        'Description': o.rule.description,
                        'ShortDescription': o.rule.shortdesc,
                        'Source': o.rule.source_url
                    },
                    'Location': {
                        'Start': {
                            'ColumnNumber': o.columnnumber,
                            'LineNumber': o.linenumber,
                        },
                        'End': {
                            'ColumnNumber': o.columnnumberend,
                            'LineNumber': o.linenumberend,
                        },
                        'Path': getattr(o, 'path', None),
                    },
                    'Level': level,
                    'Message': o.message,
                    'Filename': o.filename,
                }
            return {'__{}__'.format(o.__class__.__name__): o.__dict__}

    def print_matches(self, matches):
        # JSON formatter outputs a single JSON object
        return json.dumps(
            matches, indent=4, cls=self.CustomEncoder,
            sort_keys=True, separators=(',', ': '))


class QuietFormatter(BaseFormatter):
    """Quiet Formatter"""

    def _format(self, match):
        """Format output"""
        formatstr = u'{0} {1}:{2}'
        return formatstr.format(
            match.rule,
            match.filename,
            match.linenumber
        )


class ParseableFormatter(BaseFormatter):
    """Parseable Formatter"""

    def _format(self, match):
        """Format output"""
        formatstr = u'{0}:{1}:{2}:{3}:{4}:{5}:{6}'
        return formatstr.format(
            match.filename,
            match.linenumber,
            match.columnnumber,
            match.linenumberend,
            match.columnnumberend,
            match.rule.id,
            match.message
        )
