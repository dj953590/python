import fitz
import re


class Redactor:
    def __init__(self, pdf_path, redactor_path, words):
        self.pdf_path = pdf_path
        self.redacted_path = redacted_path
        self.words = words

    # static methods work independent of class object
    @staticmethod
    def get_sensitive_data(lines, words):

        # Create a regex pattern from the list of words
        word_pattern = '|'.join(re.escape(word) for word in words)
        WORD_REG: str = rf"({word_pattern})"

        for line in lines:
            # matching the regex to each line
            # Find all matches of the regex in the line
            matches = re.findall(WORD_REG, line, re.IGNORECASE)
            for match in matches:
                # Yield each match found
                yield match

    # Function to redact words in a PDF document
    def redact_words(self):
        # Open the PDF document
        doc = fitz.open(self.pdf_path)

        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            lines = text.split('\n')

            # Get sensitive data using the regex pattern
            sensitive_data = self.get_sensitive_data(lines, self.words)

            for word in sensitive_data:
                # Redact the word in the PDF
                areas = page.search_for(word)
                for area in areas:
                    page.add_redact_annot(area, fill=(1, 1, 1))
                page.apply_redactions()

        # Save the redacted PDF
        doc.save(self.redacted_path)

if __name__ == "__main__":
    # replace it with name of the pdf file
    pdf_path = "C:/DJ/docs/query/Tesla.pdf"
    redacted_path = "C:/DJ/docs/query/Redacted_Tesla.pdf"
    word_to_redact = ["Tesla", "TSLA.O"]
    redactor = Redactor(pdf_path, redacted_path, word_to_redact)
    redactor.redact_words()
