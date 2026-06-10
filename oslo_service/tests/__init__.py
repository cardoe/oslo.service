#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os

# The functional fork-safety tests need native multiprocessing spawn without
# eventlet monkey-patching. Standard unit test jobs do not set this variable.
if not os.environ.get('OSLO_SERVICE_SKIP_EVENTLET'):
    import eventlet

    if os.name == 'nt':
        # eventlet monkey patching the os and thread modules causes
        # subprocess.Popen to fail on Windows when using pipes due
        # to missing non-blocking IO support.
        #
        # bug report on eventlet:
        # https://bitbucket.org/eventlet/eventlet/issue/132/
        #       eventletmonkey_patch-breaks
        eventlet.monkey_patch(os=False, thread=False)
    else:
        eventlet.monkey_patch()

    # The default backend is threading, but the unit tests in this
    # environment run under eventlet monkey-patching and exercise the
    # eventlet backend, so default to it here. Test modules may resolve
    # components at import time, so this must happen before they load.
    #
    # Import under an alias: the name "backend" would be clobbered on this
    # package once the oslo_service.tests.backend subpackage is imported
    # during discovery, which would break the hook's attribute lookup.
    from oslo_service import backend as _oslo_backend

    _oslo_backend.register_backend_default_hook(
        lambda: _oslo_backend.BackendType.EVENTLET)
