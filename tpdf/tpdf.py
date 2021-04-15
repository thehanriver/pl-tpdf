#
# tpdf ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp


Gstr_title = r"""

Generate a title from 
http://patorjk.com/software/taag/#p=display&f=Doom&t=tpdf

"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       tpdf.py 

    SYNOPSIS

        python tpdf.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-tpdf tpdf                        \
                /incoming /outgoing

    DESCRIPTION

        `tpdf.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class Tpdf(ChrisApp):
    """
    An app to ...
    """
    PACKAGE                 = __package__
    TITLE                   = 'PDF generation plugin'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = '' # url of an icon image
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin
    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--dir',
        	dest = 'dir',
        	type = str,
        	optional = False,
        	default = 'not specified',
        	help = 'directory')
        self.add_argument('--imagefile', 
            dest         = 'imagefile', 
            type         = str, 
            optional     = False,
            help         = 'Name of image file submitted to the analysis')
        self.add_argument('--patientId', 
            dest         = 'patientId', 
            type         = str, 
            optional     = True,
            default      = 'not specified',
            help         = 'Patient ID')
		
    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        
        
        directory = options.dir
        parent_dir = options.inputdir
        nPath = os.path.join(parent_dir , directory)
        
        # fetch input data
        with open('{}/prediction-default.json'.format(nPath)) as f:
          classification_data = json.load(f)
        try: 
            with open('{}/severity.json'.format(nPath)) as f:
                severityScores = json.load(f)
        except:
            severityScores = None

        template_file = "pdf-covid-positive-template.html" 
        if classification_data['prediction'] != "COVID-19" or severityScores is None:
            template_file = "pdf-covid-negative-template.html"

        txt = files('pdfgeneration').joinpath('template').joinpath(template_file).read_text()
        # replace the values
        txt = txt.replace("${PATIENT_TOKEN}", options.patientId)
        txt = txt.replace("${PREDICTION_CLASSIFICATION}", classification_data['prediction'])
        txt = txt.replace("${COVID-19}", classification_data['COVID-19'])
        txt = txt.replace("${NORMAL}", classification_data['Normal'])
        txt = txt.replace("${PNEUMONIA}", classification_data['Pneumonia'])
        txt = txt.replace("${X-RAY-IMAGE}", options.imagefile)

        time = datetime.datetime.now()
        txt = txt.replace("${month-date}", time.strftime("%c"))
        txt = txt.replace("${year}", time.strftime("%Y"))
        # add the severity value if prediction is covid
        if template_file == "pdf-covid-positive-template.html":
            txt = txt.replace("${GEO_SEVERITY}", severityScores["Geographic severity"])
            txt = txt.replace("${GEO_EXTENT_SCORE}", severityScores["Geographic extent score"])
            txt = txt.replace("${OPC_SEVERITY}", severityScores["Opacity severity"])
            txt = txt.replace("${OPC_EXTENT_SCORE}", severityScores['Opacity extent score'])

        # pdfkit wkhtmltopdf is hard-coded to look in /tmp for assets
        # when input is a string
        for asset_file in files('pdfgeneration').joinpath('template/assets').iterdir():
            os.symlink(asset_file, path.join('/tmp', asset_file.name))
        os.symlink(path.join(nPath, options.imagefile), path.join('/tmp', options.imagefile))

        pdfkit.from_string(txt, path.join(options.outputdir, 'patient_analysis.pdf'))
    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
