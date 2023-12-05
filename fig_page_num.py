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
import fitz
import re

page_num_fig = {}
prev_page_num = None


def get_fig_page(pdf_file_path):
	pdf_file = fitz.open(pdf_file_path)

	for page in pdf_file.pages():
		page_num = page.number + 1
		data = page.get_text_blocks()
		data_content = [x[4] for x in data]
		for para_data in data_content:
			if re.search(r"^Figure \d+:", para_data.strip()) or re.search(r"Example \d+:", para_data.strip()) or re.search(r"^Table \d+ —", para_data.strip()):
				if page_num not in page_num_fig:
					page_num_fig[page_num] = [para_data.strip()]
				else:
					page_num_fig[page_num].append(para_data.strip())
	return page_num_fig
