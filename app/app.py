import argparse
import os
import sys
import logging
import PDFReader

if __name__ == "__main__":

        try:
                LOG = "./.log/pdf2text.log"

                parser = argparse.ArgumentParser(description='Argument Parser')
                parser.add_argument('pdf', metavar='PDF', type=str, help='input pdf')
                parser.add_argument('-o', dest='OUT', type=str, default="", help='target output file (default: {}'.format(""))
                parser.add_argument('-l', dest='LOGFILE', type=str, default=LOG, help='path for logfile (default: {})'.format(LOG))
                parser.add_argument('-p', dest='PRODUCTION', action='store_const', help="set to production mode", const=True, default=False)

                args = parser.parse_args()

                PRODUCTION = args.PRODUCTION
                os.environ['PRODUCTION'] = str(PRODUCTION)

                LOG = args.LOGFILE
                if not os.path.exists(os.path.abspath(os.path.dirname(LOG))):
                        os.makedirs(os.path.abspath(os.path.dirname(LOG)))

                logging.basicConfig(filename=LOG, level=logging.INFO if PRODUCTION else logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')
                logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

                ################
                # Extract Text
                ################
                logging.info("Extract Text ...")
                file = args.pdf
                output = PDFReader.pdf2text(file)
                print(output)
                logging.info("Text Extracted!")

                ################
                # Save Text if output is enabled
                ################
                if args.OUT:
                        logging.info("Save Result ...")
                        with open(args.OUT, "w+") as f:
                                f.write(output)
                        logging.info(f"Path: [{args.OUT}]")
                        logging.info("Result Saved!")

        except Exception as e:
                logging.error(e)




