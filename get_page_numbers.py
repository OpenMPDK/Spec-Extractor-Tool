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
import sys
import fitz

sys.tracebacklimit = 0


def get_chapter_page_info(file_path):
	"""
	:param file_path: Input PDF filepath
	:return: Return a tuple data structure which has total number of pages
			and dictionary of chapters names and start page number of each
			chapter Ex: (100, {"chapter_1": 1})
	"""
	doc_obj = fitz.open(file_path)
	toc = doc_obj.get_toc()
	chapter_names = [item[1] for item in toc if item[0] == 1]
	start_page = [item[2] for item in toc if item[0] == 1]
	return doc_obj.page_count, dict(zip(chapter_names, start_page))


def get_chapter_number(file_path):
	"""
	Args:
		file_path: PDF file path
	"""
	chapter_num_name = {}
	doc_obj = fitz.open(file_path)
	toc = doc_obj.get_toc()
	chapter_names = [item[1] for item in toc if item[0] == 1]

	print("\n\n The available chapter from the file are below.\n\n Chapter_number : Chapter_name \n",)
	for number, name in enumerate(chapter_names, start=1):
		chapter_num_name[number] = name
		print("{} : {}".format(number, name))

	print("""\n Please Enter the Chapter number(s) or range of chapter numbers in the below format : \n
	       . all : To Extract all the chapters
	       . 2 :   To extract only one chapter (To Extract the single chapter)
	       . 1-3 :  To extract the chapters ranges from 1 to 3 (1,2,3)
	       . 3,7 : To extract the chapters 3 and 7
	       . 2-4,8 : To extract the chapters from 2 to 4 and 8 as well""")

	chapter_number = input("\n\n Please enter the chapter number(s) to extract : ")

	return chapter_number


def chapter_number_name(file_path):
	"""
	:param file_path: pdf file path
	:return:
	"""
	chapter_num_name = {}
	doc_obj = fitz.open(file_path)
	toc = doc_obj.get_toc()
	chapter_names = [item[1] for item in toc if item[0] == 1]
	for number, name in enumerate(chapter_names, start=1):
		chapter_num_name[number] = name
	return chapter_num_name


def verify_chapter(file_path, chapter_numbers):
	"""
	To verify the given chapter number(s) or range of chapters are valid
	Args:
		file_path: pdf file path
		chapter_numbers : file chapter numbers
	"""
	chapter_num_name = chapter_number_name(file_path)
	for number in chapter_numbers:
		if number not in list(chapter_num_name.keys()):
			raise Exception("\n\n Invalid chapter number given, please enter the valid chapter(s) number ")


def get_page_range(file_path, chapters):
	"""
	:param file_path: PDF File path
	:param chapters:
	:return: start and end page of the Chapter given.
	         if chapter = "all" (default), it return the start and end page of
	         the whole document.
	"""
	chapter_start_end_page = list()
	chapter_page_info = get_chapter_page_info(file_path)
	chapters_names = list(chapter_page_info[1].keys())
	chapters_start_pages = list(chapter_page_info[1].values())

	if chapters == "all":
		start_page = chapters_start_pages[0]
		end_page = chapter_page_info[0]
		chapter_start_end_page.append([start_page, end_page])
		return chapter_start_end_page

	else:
		verify_chapter(file_path, chapters)
		if isinstance(chapters, list):
			chapter_numbers = sorted(chapters)
			for chapter_number in chapter_numbers:
				start_end_page = list()
				chapter_name = chapters_names[chapter_number-1]
				chapter_start_page = chapter_page_info[1][chapter_name]
				start_end_page.append(chapter_start_page)
				if chapter_number == len(chapters_names):
					chapter_end_page = chapter_page_info[0]
				else:
					chapter_end_page = chapter_page_info[1][chapters_names[chapter_number]] - 1
				start_end_page.append(chapter_end_page)
				chapter_start_end_page.append(start_end_page)

		return chapter_start_end_page


def get_chapter_page_range(file_path, chapter_number):
	"""
	:param file_path: PDF File path
	:param chapter_number: Chapter chapter_number to extract
	       Chapter number can be
	       . "1" or "2" or "10" : To extract only one chapter
	       . "1-3" :  To extract the chapters ranges from 1 to 3
	       . "1,3,4" : To extract the chapters 1, 3, and 4
	       . "1-3,6" : To extract the chapters from 1 to 3 and 6 as well
	:return: start and end page of the Chapter given.
	"""
	chapter_numbers_list = list()

	if chapter_number == "all":
		return get_page_range(file_path, chapter_number)

	elif "," and "-" in chapter_number:
		y = chapter_number.split(",")
		for i in y:
			if "-" in i:
				x, y = i.split("-")
				temp = list(range(int(x), int(y) + 1))
				chapter_numbers_list.extend(temp)
			else:
				chapter_numbers_list.append(int(i))
		return get_page_range(file_path, chapter_numbers_list)

	elif "," in chapter_number:
		chapter_numbers_list.extend(list(map(int, chapter_number.split(","))))
		return get_page_range(file_path, chapter_numbers_list)

	elif "-" in chapter_number:
		first_chapter, last_chapter = chapter_number.split("-")
		temp = list(range(int(first_chapter), int(last_chapter) + 1))
		chapter_numbers_list.extend(temp)
		return get_page_range(file_path, chapter_numbers_list)

	elif re.search(r"^\d+$", chapter_number):
		chapter_numbers_list.append(int(chapter_number))
		return get_page_range(file_path, chapter_numbers_list)

	else:
		raise Exception("Please enter the valid chapter numbers")
