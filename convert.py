import glob
import sys

from services.ConverterService import ConverterService


outputDir = ''

if (len(sys.argv) > 1):
    outputDir = sys.argv[1]

service = ConverterService("./output")
# service.setSplitChunks(2)
for file in glob.glob("./songs/*.xml"):
    service.addFilePath(file)


if outputDir:
    print("Output folder:", outputDir)
    service.outputFolder(outputDir)

service.convert()
