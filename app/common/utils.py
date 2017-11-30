# coding: utf-8

import functools
import importlib


class SiteLocator:

	factories = {}
	module_dic = {'jira': ('sites.jira', 'Jira'),
				  'jenkins': ('sites.jenkins', 'Jenkins')}

	@classmethod
	def get_factory(cls, name):

		if name not in cls.factories:
			module_path = cls.module_dic.get(name)[0]
			module = importlib.import_module(module_path)
			if not module:
				return None
			client_cls = getattr(module, cls.module_dic.get(name)[1])
			if not client_cls:
				return None
			cls.factories[name] = wraps_client_factory(client_cls)

		return cls.factories[name]()


class ClientWrapper:

	def __init__(self, client):
		self.client = client

	def open(self):
		pass

	def close(self):
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def __getattr__(self, attr):
		return getattr(self.client, attr)


def wraps_client_factory(client_cls):

	@functools.wraps(client_cls)
	def _func():

		client = client_cls()
		return ClientWrapper(client)

	return _func

