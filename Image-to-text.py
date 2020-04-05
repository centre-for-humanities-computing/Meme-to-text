'''
Image-to-text library for text detection and extraction. 
'''
#import TextExtractor
#import MemeEstimator
from optparse import OptionParser
import pathlib

class InputError(Exception):
    """Exception raised for errors in the input.
    """
    def __init__(self, message):
        self.message = message

class ImageToText:
    def __init__(self, input_dir="", extract_text=True, extract_meme_context=False, output_dir=""):
        pass

def main():
    parser = OptionParser()
    parser.add_option("-i", "--images", dest="input_directory",
                    action="store", type="string",
                    help="directory of input images", metavar="INPUT")
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