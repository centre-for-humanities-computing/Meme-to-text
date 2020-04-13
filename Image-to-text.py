'''
Image-to-text library for text detection and extraction. 
'''
from TextExtractor import TextExtractor
from TextExtractor import ImageLabel
import wordsegment
from optparse import OptionParser
from autocorrect import Speller
import pathlib

class InputError(Exception):
    """Exception raised for errors in the input.
    """
    def __init__(self, message):
        self.message = message

class ImageToText:
    def __init__(self, input_dir="", extract_text=True, correct_spelling = False, extract_meme_context=False, output_dir=""):
        TEX = TextExtractor()
        files = pathlib.Path(input_dir).glob("*")
        files = [x for x in files if x.is_file()]
        image_labels = TEX.extract_text(files)

        if correct_spelling:
            for img in image_labels: 
                if not len(img.ocr) > 0:
                    continue
                check = Speller(lang='en')
                wordsegment.load()
                ocr = wordsegment.segment(img.ocr)
                ocr = " ".join(ocr)
                ocr = check(ocr)
                img.ocr = ocr
        
        for image in image_labels:
            image.save_to(output_dir)
        
def main():
    parser = OptionParser()
    parser.add_option("-i", "--images", dest="input_directory",
                    action="store", type="string",
                    help="directory of input images", metavar="INPUT")
    parser.add_option("-s", "--spelling", dest="spelling_b",
                    action="store_false",
                    help="Should spelling be corrected", metavar="SPELL")
    parser.add_option("-t", "--text",
                    action="store_false", dest="text_b", default=True,
                    help="output image text")
    parser.add_option("-c", "--memecontext",
                    action="store_false", dest="context_b", default=True,
                    help="output meme context")
    parser.add_option("-o", "--output", dest="output_file", action="store",
                    type="string",
                    help="Output file after processing", metavar="OUTPUT")
    (options, _) = parser.parse_args()

    if not options.input_directory:
        raise InputError("Input directory must be specified.")

    #Instantiate ImageToText 
    ITT = ImageToText(options.input_directory, options.text_b, options.context_b, options.output_file)

if __name__ == "__main__":
    main()