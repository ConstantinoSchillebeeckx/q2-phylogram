


class SmartFormatter(argparse.HelpFormatter):
    """
    smart option parser, will extend the help string with the values
    for type e.g. {stype: str} and default (default: None)

    adapted from https://bitbucket.org/ruamel/std.argparse/src/cd5e8c944c5793fa9fa16c3af0080ea31f2c6710/__init__.py?fileviewer=file-view-default
    """

    def __init__(self, *args, **kw):
        self._add_defaults = None
        super(SmartFormatter, self).__init__(*args, **kw)

    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        self._add_defaults = True
        text = text
        return argparse.HelpFormatter._split_lines(self, text, width)

    def _get_help_string(self, action):
        help = action.help
        if action.default is not argparse.SUPPRESS:
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                help += ' {type: %(type)s} (default: %(default)s)'
        return help










# SETUP OPTION PARSER
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=SmartFormatter)
        parser.add_argument("newick", type=str,
                            help="Input Newick tree file")
        parser.add_argument("-m", "--mapping", type=str,
                            help="OTU mapping file containing metadata used to format tree")
        parser.add_argument("-o", "--out", default='.', type=str,
                            help="Output directory for all generated files")
        args = parser.parse_args()
        main(args)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
