#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init, task, Author
from plantuml import PlantUML
from os.path import abspath

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")



name = "python_subtitle_crawler"
version = "1.0"

summary = "Subtitle Crawler"
url     = "https://github.com/Oliss4t/Subtitle-Crawler"

description = """    A subtitle scraper CLI that lets you download one or several subtitles in different languages.
    Provide the movie imdbid and optionally a language code, default "eng".
    Here are three examples:
    1) python main.py download -i 816692 -lang
    2) python main.py download -i 343818 -lang "ger"
    3) python main.py download -li "imdb_ids"

    You need a valid OpenSubtitles account for the tool to work.
    You can register a free account at https://www.opensubtitles.org/de/newuser"""

authors      = [Author("Tassilo Henninger", "tassilo.henninger@gmail.com")]

default_task = ["create_umls", "publish"]


@init
def set_properties(project):
    project.depends_on('imdbpy', version=">=2021.4")
    project.depends_on('jsonpickle', version=">=2.0")
    project.depends_on('plantuml')
    project.depends_on('click')
    project.depends_on('openpyxl')

    project.build_depends_on("flake8")

    project.set_property('coverage_threshold_warn', 50)
    project.set_property('coverage_break_build', False)
    project.set_property('flake8_break_build', False)
    project.set_property('flake8_max_line_length', 200)
    project.set_property('flake8_include_test_sources', True)

#create UML documentation
@task("create_umls", description="create the umls pngs based of the plant uml code")
def create_umls():
    # create a server object to call for your computations
    server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                      basic_auth={},
                      form_auth={}, http_opts={}, request_opts={})

    # Send and compile your diagram files to/with the PlantUML server
    server.processes_file(abspath('docs/uml/deploymentDiagram'))
    server.processes_file(abspath('docs/uml/useCaseDiagram'))
    server.processes_file(abspath('docs/uml/activity_diagram'))

