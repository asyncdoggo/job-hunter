
import json
import os.path
import pathlib

from pypdf import PdfReader

from .parsers import ParseJobDesc, ParseResume
from .ReadPdf import read_single_pdf


class ResumeProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        # self.input_file_name = os.path.join(self.input_file)

    def process(self) -> bool:
        try:
            resume_dict = self._read_resumes()
            return resume_dict
            # self._write_json_file(resume_dict)
            # return True
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def _read_resumes(self) -> dict:
        # data = read_single_pdf(self.input_file_name)
        data = self.read_single_pdf(self.input_file)
        output = ParseResume(data).get_JSON()
        return output
    
    def read_single_pdf(self, file_obj) -> str:
        output = []
        try:
            pdf_reader = PdfReader(file_obj)
            count = len(pdf_reader.pages)
            for i in range(count):
                page = pdf_reader.pages[i]
                output.append(page.extract_text())
        except Exception as e:
            print(f"Error reading file '': {str(e)}")
        return str(" ".join(output))



    def _read_job_desc(self) -> dict:
        data = read_single_pdf(self.input_file_name)
        output = ParseJobDesc(data).get_JSON()
        return output

    def _write_json_file(self, resume_dictionary: dict):
        file_name = str(
            "Resume-" + self.input_file + resume_dictionary["unique_id"] + ".json"
        )
        save_directory_name = file_name
        json_object = json.dumps(resume_dictionary, sort_keys=True, indent=14)
        with open(save_directory_name, "w+") as outfile:
            outfile.write(json_object)
