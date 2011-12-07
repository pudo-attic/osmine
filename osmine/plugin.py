import os

from openspending.plugins.core import SingletonPlugin, implements
from openspending.plugins.interfaces import IConfigurer, IRoutes

here = os.path.dirname(__file__)
template_dir = os.path.join(here, 'templates')

class MiningPlugin(SingletonPlugin):

    implements(IConfigurer, inherit=True)
    implements(IRoutes, inherit=True)

    def before_map(self, map):
        controller = 'osmine.controllers:MiningController'
        map.connect('/{dataset}/meta/mining', controller=controller, action='run',
            conditions=dict(method=['POST']))
        map.connect('/{dataset}/meta/mining', controller=controller,
                action='index')

    def configure(self, config):
        print template_dir
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])
        config['celery.imports'] = config.get('celery.imports', '') + ' osmine.tasks'










