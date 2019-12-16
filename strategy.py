import re


class Simple(object):
    def __init__(self, file_name, line_num, text, pattern):
        self.fileName = file_name
        self.lineNum = line_num
        self.text = text
        self.pattern = pattern

    def print_line(self):  # print the filename, line number and matching
        print("FILE: {}, LINE: {}, TEXT: {}".format(self.fileName, self.lineNum, self.get_formatted_text()))

    def get_formatted_text(self):
        return self.text


class Underscore(Simple):    # underscored (not ^) matching text
    def get_formatted_text(self):
        matches = re.findall(self.pattern, self.text)
        matches = list(set(matches))
        formatted_text = self.text
        for match in matches:
            new_match = '\033[4m' + match + '\033[0m'
            formatted_text = formatted_text.replace(match, new_match)
        return formatted_text


class Color(Simple):    # creating class for matching text to be colored with red
    def get_formatted_text(self):
        matches = re.findall(self.pattern, self.text)
        matches = list(set(matches))
        formatted_text = self.text
        for match in matches:
            new_match = '\x1b[31m' + match + '\x1b[0m'
            formatted_text = formatted_text.replace(match, new_match)
        return formatted_text


class Machine(Simple):  # creating a class to find a matching pattern
    def print_line(self):
        for match in re.finditer(self.pattern, self.text):
            print("{}:{}:{}:{}".format(self.fileName, self.lineNum, match.start(), match.group(0)))
