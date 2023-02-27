import glob
from services.ConverterService import ConverterService

service = ConverterService("./output")
for file in glob.glob("./songs/*.xml"):
    service.addFilePath(file)

service.convert()