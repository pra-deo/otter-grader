###############################################
##### In-Notebook Checks for Otter-Grader #####
###############################################

from gofer.ok import check
import inspect
import os
from nb2pdf import convert
from IPython.display import display, HTML
from glob import glob

class Notebook:
	"""Notebook class for in-notebook autograding"""

	def __init__(self, test_dir="./tests"):
		self._path = test_dir
		try:
			__IPYTHON__
		except NameError:
			assert False, "otter.Notebook must be used in a Jupyter Notebook"

	def check(self, question, global_env=None):
		"""Checks question using gofer"""
		test_path = os.path.join(self._path, question + ".py")

		# ensure that desired test exists
		assert os.path.exists(test_path) and \
			os.path.isfile(test_path), "Test {} does not exist".format(question)
		
		# pass the correct global environment
		if global_env is None:
			global_env = inspect.currentframe().f_back.f_globals

		# pass the check to gofer
		return check(test_path, global_env)

	def export(self, nb_path):
		"""Exports notebook to PDF"""
		convert(nb_path)

		# create and display output HTML
		out_html = """
		<p>Your file has been exported. Download it 
		<a href="{}" target="_blank">here</a>!
		""".format(nb_path[:-5] + "pdf")
		
		display(HTML(out_html))

	def check_all(self):
		tests = glob(os.path.join(self._path, "*.py"))
		for file in sorted(tests):
			test_name = os.path.split(file)[1][:-3]
		    check_html = self.check(test_name)._repr_html_()
		    check_html = "<p><strong>{}</strong></p>".format(test_name) + check_html
		    display(HTML(check_html))

