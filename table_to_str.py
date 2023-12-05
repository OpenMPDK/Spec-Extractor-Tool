"""
BSD 3-clause "New" or "Revised" License

Copyright (c) 2023-2032, Arun Bosco J (arun.bosco@samsung.com)
Copyright (c) 2023-2032, Mathi Yugandhararao (yugandhar.m@samsung.com)
All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the following
conditions are met:

	* Redistributions of source code must retain the above copyright
	notice, this list of conditions and the following disclaimer.

	* Redistributions in binary form must reproduce the above
	copyright notice, this list of conditions and the following
	disclaimer in the documentation and/or other materials provided
	with the distribution.

	* Neither the name of the copyright holder nor the names of its
	contributors may be used to endorse or promote products derived
	from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
import re
import numpy as np
import pandas as pd
from fig_page_num import get_fig_page


def convert_table_to_string(path):
	"""
	Args:
		path: html file path
	Return:
		converts the table to string in a Jira upload-able format
	"""
	table = pd.read_html(path, encoding="utf-8")[0]
	df = pd.DataFrame(table)
	df = df.drop(columns=df.columns[0])
	df = df.replace(np.nan, "  ")
	if not df.empty:
		x = df.values
		y = x.tolist()
		str_data = ("||" + "||".join((str(i)) for i in y[0] if i is not None or i != "") + "||" + "\n")
		search = re.search(r"(\d\\n\w/\w)", str_data)
		if search:
			str_data = re.sub(r"(\d)\\n(\w/\w)", r"\2 \1", str_data)

		str_data = str_data.replace("\\n", " ")
		if not re.search(r"\w", str_data):
			return None
		for j in y[1:]:
			x = ("|" + "|".join(str(i) for i in j if i is not None or i != "") + "|").replace("\\n", " ")
			str_data = str_data + x + "\n"

		if re.search(r"\w", str_data):
			return str_data


def get_fig_data(pdffile, parent_dir, html_files):
	"""
	To ge the table name and the table
	Args:
		pdffile: pdf file path
		parent_dir: directory path where html files are saved
		html_files : list of all html files
	Returns:
		return a dictionary of table name and table content
	"""
	prev_pg_num = None
	figure_name_data = {}
	i = 0
	page_fig_dict = get_fig_page(pdffile)
	for file_name in html_files:
		file_path = parent_dir + "\\" + file_name
		page_num = int(re.search(r"page-(\d+)-table", file_name).group(1))
		if page_num != prev_pg_num:
			i = 0
		table_data_str = convert_table_to_string(file_path)
		# print(table_data_str)
		if page_num in page_fig_dict and table_data_str is not None:
			# print(page_fig_dict[page_num])
			if len(page_fig_dict[page_num]) == 1:
				figure_name = page_fig_dict[page_num][0]  # {1: []}
				if figure_name not in figure_name_data:
					figure_name_data[figure_name] = table_data_str
				else:
					figure_name_data[figure_name] += table_data_str
				i = 0
			else:
				if i != len(page_fig_dict[page_num]):
					fig_name = page_fig_dict[page_num][i]
					if fig_name not in figure_name_data:
						figure_name_data[fig_name] = table_data_str
					else:
						figure_name_data[fig_name] += table_data_str
					i += 1

		prev_pg_num = page_num
	return figure_name_data
