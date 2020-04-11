import argparse
import yaml

class ConvertService(object):

    __inverted = None
    __level = 1

    def __init__(self, inverted):
        self.__inverted = inverted

    def process(self, input):
        if self.__inverted:
            print("inverted: confluence -> yml")
            print("not working yet")
        else:
            self.__convert_yml_to_confluence(input)

    def __convert_yml_to_confluence(self, input):
        with open(input, 'r') as stream:
            try:
                documents = yaml.full_load(stream)
                self.__step_into_yml(documents.items())

            except yaml.YAMLError as exc:
                print(exc)

    def __repeat_to_length(seelf, string_to_expand, length):
        return (string_to_expand * (int(length / len(string_to_expand)) + 1))[:length]

    def __down(self):
        self.__level = self.__level + 1

    def __up(self):
        self.__level = self.__level - 1

    def __step_into_yml(self, items):
        for key, value in items:
            print(self.__repeat_to_length("*", self.__level), end="")
            if isinstance(value, list):
                print(" {}:".format(key))
                self.__down()
                for i in range(len(value)):
                    print(self.__repeat_to_length("*", self.__level), end="")
                    print(" {}-{}:".format(key, i))
                    self.__down()
                    self.__step_into_yml(value[i].items())
                    self.__up()
                self.__up()
            elif isinstance(value, dict):
                print(" {}:".format(key))
                self.__down()
                self.__step_into_yml(value.items())
                self.__up()
            else:
                print(" {}: {}".format(key, value))


parser = argparse.ArgumentParser(description='Script to convert YML to Confluence format')
parser.add_argument('-i', '--invert', action="store_true", help='convert Confluence to YML (Default False)')
parser.add_argument('input', default=None, type=str, help='input file')

args = parser.parse_args()

if __name__ == "__main__":
    invert = (hasattr(args, 'invert'))
    invert = args.invert if invert else False

    convert = ConvertService(invert)
    convert.process(args.input)