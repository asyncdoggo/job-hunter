from .scripts.ResumeProcessor import ResumeProcessor


class ResumeParser:
    def parse(self, file):
        processor = ResumeProcessor(file)
        success = processor.process()
        return success