import errno
from lxml import etree
from pathlib import Path
import re
import os
from datetime import datetime


class ConverterService:
    VERSE_LABEL = 'Куплет'
    CHORUS_LABEL = 'Приспів'
    __files = list()
    __customOutputFolder = ''
    __chunksCount = 0
    __defaultNamespace = {'ns': 'http://openlyrics.info/namespace/2009/song'}
    __output = ''

    def __init__(self, output) -> None:
        self.output = output
        # current dateTime
        now = datetime.now()
        self.__customOutputFolder = now.strftime("%Y-%m-%d %H:%M")

    def outputFolder(self, folder: str) -> None:
        self.__customOutputFolder = folder

    def setSplitChunks(self, chunks: int) -> None:
        self.__chunksCount = chunks

    def addFilePath(self, filePath: str) -> None:
        self.__files.append(filePath)

    def __checkDirExists(self) -> None:
        dirName = self.output + '/'+self.__customOutputFolder

        print(dirName)
        if not os.path.exists(dirName):
            os.makedirs(dirName)

    def convert(self) -> None:
        self.__checkDirExists()

        for file in self.__files:
            tree = etree.parse(file)
            root = tree.getroot()
            verses = root.xpath(
                '//ns:verse', namespaces=self.__defaultNamespace)
            # songTitles = root.xpath('//ns:title[1]', namespaces=self.__defaultNamespace)
            # title = songTitles[0].text
            title = Path(file).resolve().stem
            output = self.__formatSong(verses, self.__defaultNamespace)
            with open(f'{self.output}/{self.__customOutputFolder}/{title}.txt', 'w') as f:
                f.write(output)
                f.close()

    """
  Generate song part label, Verse or Chorus

  example: v1a, v1b, v1c
  which means: v - prefix, 1 - verse/chorus number, a|b|c... - chunk letter

  """

    def __getSongPartHeading(self, name: str) -> str:
        match = re.match(r'(\w+)(\d+)(\w*)', name)
        if match:
            prefix = match.group(1)
            number = match.group(2)
            if prefix == 'v':
                return f'##({self.VERSE_LABEL} {number})'
            elif prefix == 'c':
                return f'##({self.CHORUS_LABEL} {number})'

        return name

    def __splitChunks(self, list_a, chunk_size):
        for i in range(0, len(list_a), chunk_size):
            yield list_a[i:i + chunk_size]

    def __formatSong(self, verses: list[etree.Element], namespaces) -> str:
        versesList = {}
        pattern = r'[vc]\d+[a-z]*'
        for verse in verses:
            name = verse.attrib['name']
            if re.match(pattern, name):
                key = self.__getSongPartHeading(name)
                if key not in versesList:
                    versesList[key] = []
                versesList[key].append(verse)

        lastHeading = ""
        output = ''
        for key in versesList:
            verse = versesList[key]
            for part in verse:
                lines = part.xpath('.//ns:lines/text()', namespaces=namespaces)
                if (lastHeading != key):
                    lastHeading = key
                    output += lastHeading + '\n'

                if self.__chunksCount and len(lines) > self.__chunksCount:
                    chunks = self.__splitChunks(lines, 2)
                    for chunk in chunks:
                        output += '\n'.join(chunk) + '\n\n'
                else:
                    output += '\n'.join(lines) + '\n'
            output += '\n'
        return output
