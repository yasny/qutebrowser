# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2016-2017 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

import logging
import re

import pytest_bdd as bdd

bdd.scenarios('history.feature')


@bdd.then(bdd.parsers.parse("the history should contain:\n{expected}"))
def check_history(quteproc, httpbin, tmpdir, expected):
    path = tmpdir / 'history'
    quteproc.send_cmd(':debug-dump-history "{}"'.format(path))
    quteproc.wait_for(category='message', loglevel=logging.INFO,
                      message='Dumped history to {}'.format(path))

    with path.open('r', encoding='utf-8') as f:
        # ignore access times, they will differ in each run
        actual = '\n'.join(re.sub('^\\d+-?', '', line).strip() for line in f)

    expected = expected.replace('(port)', str(httpbin.port))
    assert actual == expected


@bdd.then("the history should be empty")
def check_history_empty(quteproc, httpbin, tmpdir):
    check_history(quteproc, httpbin, tmpdir, '')
