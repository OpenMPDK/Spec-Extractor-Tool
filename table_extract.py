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
import os
import re
import camelot
import numpy as np
import pandas as pd
from zipfile import ZipFile
from fig_page_num import get_fig_page
from styleframe import Styler, StyleFrame, utils
from get_page_numbers import get_chapter_page_range, get_chapter_number
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def generate_html_files(pdf_file_loc, excel_file_loc, chapternumber):
	"""
	Args:
		pdf_file_loc: pdf file path
		excel_file_loc: Excel file path to collect the tables
		chapternumber: chapter number(s) or range of chapters
	"""
	page_range_list = list()
	start_end_page_info = get_chapter_page_range(pdf_file_loc, chapternumber)
	for start_end_page in start_end_page_info:
		page_range_format = "{}-{}".format(start_end_page[0],
		                                   start_end_page[1])
		page_range_list.append(page_range_format)
	extract_page_range = ",".join(page_range for page_range in page_range_list)

	tables = camelot.read_pdf(pdf_file_loc, pages=extract_page_range, line_scale=35,
	                          suppress_stdout=True)

	file_name = os.path.basename(excel_file_loc)
	dir_path = os.path.dirname(excel_file_loc)
	file_name = os.path.splitext(file_name)[0]
	html_file = f'{dir_path}\\{file_name}.html'
	tables.export(html_file, f='html', compress=True)

	root_path = dir_path + r"\{}.zip".format(file_name)
	extract_dir = None
	if os.path.exists(root_path):
		extract_dir = os.path.splitext(root_path)[0]

	with ZipFile(root_path, "r") as zp:
		zp.extractall(path=extract_dir)
	files = os.listdir(extract_dir)
	files.sort(key=lambda x: int(re.sub(r'\D', '', x)))
	return extract_dir, files


def get_tables(pdf_file_path, output_path, chapternumber):
	"""
	Args:
		pdf_file_path:pdf file path
		output_path: Excel file path to collect the tables
		chapternumber:chapter number(s) or range of chapters
	"""
	print("\n ######--- Tables Extraction Started ----############# \n")
	html_files_dir, html_files = generate_html_files(pdf_file_path, output_path,
	                                                 chapternumber)
	fig_page_num = get_fig_page(pdf_file_path)
	start_row = 1
	i = 0

	writer = StyleFrame.ExcelWriter(output_path)
	book = writer.book
	sheet = book.create_sheet("Table")
	prev_pg_num = None
	for filepath in html_files:
		page_num = int(re.search(r"\d+", filepath).group())
		if page_num != prev_pg_num:
			i = 0
		html_path = r"{}\{}".format(html_files_dir, filepath)

		table = pd.read_html(html_path, encoding="utf-8")[0]

		df = pd.DataFrame(table)
		df = df.drop(columns=df.columns[0])
		df = df.replace(np.nan, "  ")
		df = df.replace(r"\\n", " ", regex=True)

		if df.empty:
			continue

		default_style = Styler(border_type=utils.borders.thin,
		                       bold=False, shrink_to_fit=True, font_size=10)
		sf = StyleFrame(df, styler_obj=default_style)
		sf.set_column_width(df.columns, 30)

		if page_num in fig_page_num:
			if len(fig_page_num[page_num]) == 1:
				sheet.cell(start_row, 2, fig_page_num[page_num][0])
				i = 0
			else:
				if i != len(fig_page_num[page_num]):
					sheet.cell(start_row, 2, fig_page_num[page_num][i])
					i += 1

		sf.to_excel(writer, sheet_name='Table', header=False, startrow=start_row, startcol=1, index=False)
		start_row = start_row + len(table.index) + 3
		prev_pg_num = page_num

	print("\n ######## Table Extraction completed Successfully ###### \n")

	writer.close()


def get_user_args():
	"""
	To get and parse the command line arguments given by user
	"""
	cur_work_dir = os.getcwd()
	def_table_out = cur_work_dir + "\data_table_extract.xlsx"
	args_parser = ArgumentParser(description='PDF Data Extraction', formatter_class=ArgumentDefaultsHelpFormatter)
	args_parser.add_argument("-f", "--filepath", help="PDF file location")
	args_parser.add_argument("-t", "--table_output_filepath",
	                         help="output Excel file location for Table",
	                         default=def_table_out)
	user_input = args_parser.parse_args()
	return user_input


if __name__ == "__main__":
	args = get_user_args()
	file_path = args.filepath
	excel_path = args.table_output_filepath
	chapter = args.chapter_name
	chapter_number = get_chapter_number(file_path)
	get_tables(file_path, excel_path, chapter_number)
