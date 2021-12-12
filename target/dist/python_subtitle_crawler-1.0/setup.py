#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'python_subtitle_crawler',
        version = '1.0',
        description = 'Subtitle Crawler',
        long_description = '    A subtitle scraper CLI that lets you download one or several subtitles in different languages.\n    Provide the movie imdbid and optionally a language code, default "eng".\n    Here are three examples:\n    1) python main.py download -i 816692 -lang\n    2) python main.py download -i 343818 -lang "ger"\n    3) python main.py download -li "imdb_ids"\n\n    You need a valid OpenSubtitles account for the tool to work.\n    You can register a free account at https://www.opensubtitles.org/de/newuser',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Tassilo Henninger',
        author_email = 'tassilo.henninger@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = '',

        url = 'https://github.com/Oliss4t/Subtitle-Crawler',
        project_urls = {},

        scripts = [],
        packages = [
            '.',
            'abstract_classes',
            'dto_classes',
            'error_classes',
            'media_crawler',
            'subtitle_crawler',
            'utils'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'click',
            'imdbpy>=2021.4',
            'jsonpickle>=2.0',
            'openpyxl',
            'plantuml'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
