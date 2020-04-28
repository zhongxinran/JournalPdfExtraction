import io
import re
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams


def extract_text_by_page(pdf_path):
    # 按页解析pdf
    # Args:
    #   pdf_path: 要解析的pdf的路径
    # Returns:
    #   按需逐页解析
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            # 保留原文件中的空格
            lparam = LAParams()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=lparam)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


def extract_text(pdf_path):
    # 解析pdf
    # Args:
    #   pdf_path: 要解析的pdf的路径
    # Returns:
    #   text: 解析结果，列表，每个元素为一页的文本
    text = []
    for page in extract_text_by_page(pdf_path):
        text.append(re.sub("\x0c", ' ', page))
    return text


if __name__ == '__main__':
    result = extract_text('JMLR/volumn15/Bridging Viterbi and Posterior Decoding: A Generalized Risk Approach to Hidden Path Inference Based on Hidden Markov Models.pdf')
    print(result)
