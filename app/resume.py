from .scripts.ResumeProcessor import ResumeProcessor


class ResumeParser:
    def parse(self, file):
        important_keys = ['name', 'emails', 'phones', 'experience', 'years', 'pos_frequencies', 'extracted_keywords', 'keyterms'] 
        processor = ResumeProcessor(file)
        success = processor.process()
        success = {k: v for k, v in success.items() if k in important_keys}
        return success