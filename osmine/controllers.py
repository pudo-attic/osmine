import logging
import json
import math

from pylons.controllers.util import redirect
from pylons import request, tmpl_context as c
from pylons.i18n import _

from openspending.ui.lib import helpers as h
from openspending.ui.lib.base import BaseController, render
from openspending.ui.lib.base import require, abort
from openspending.ui.lib.views import handle_request

from osmine.tasks import mine

CODE_SAMPLE = """
var cursor = this.entries();
var sum = 0;
while (true) {
    var entry = cursor.next();
    if (entry === null) {
        break;
    }
    sum += entry.amount;
}

console.log("Total " + dimensions.amount.label + ": " + sum + " " + dataset.currency);
"""

log = logging.getLogger(__name__)

class MiningController(BaseController):

    def index(self, dataset, code=None, format='html'):
        self._get_dataset(dataset)
        require.dataset.update(c.dataset)
        handle_request(request, c, c.dataset)
        if code is None:
            code = CODE_SAMPLE
        c.code = code
        return render('mining/index.html')

    def run(self, dataset, format='html'):
        self._get_dataset(dataset)
        require.dataset.update(c.dataset)
        code = request.params.get('code', '')
        mine.delay(c.dataset.name, code)
        h.flash_success(_("Your task has been initiated.."))
        return self.index(dataset, code=code)


