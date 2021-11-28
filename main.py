import os
import click
from src.openSubtitleCrawler import OpenSubtitleCrawler
from src.imdbCrawler import ImdbCrawler
from src.utils import print_method_result_to_user, read_from_xlsx_file, read_ids_from_csv

input_folder = './data/input/'
download_folder = './data/downloads/'


@click.group()
@click.pass_context
@click.option('--config-file', '-c', type=click.Path(), help='the location of your config file, default is "./config.cfg"', default='./config.cfg')
@click.option('--username', '-u', help='your OpenSubtitle username', type=str)
@click.option('--password', '-p', help='your OpenSubtitle password', type=str)
def main(ctx, username, password, config_file):
    """
    A subtitle scraper CLI that lets you download one or several subtitles in different languages.
    Provide the movie name and optionally a language code.
    Here are two examples:
    1. "I Robot",EN
    2. Interstellar
    You need a valid OpenSubtitles account for the tool to work.
    You can register a free account at https://www.opensubtitles.org/de/newuser
    """

    filename = os.path.expanduser(config_file)
    try:
        if (not username or not username) and os.path.exists(filename):
            with open(filename) as cfg:
                _lines = cfg.readlines()
                username = _lines[0]
                password = _lines[1]
                agent = _lines[2]
                click.secho(f"Login credentials could be retrieved", fg="green", bold=True)
    except IndexError:
        click.secho(f"No login credentials could be retrieved", fg="red", bold=True)


    ctx.obj = {
        'username': username,
        'password': password,
        'agent': agent,
        'config_file': filename,
    }


@main.command()
def status():
    """
    checks the status of the OpenSubtitles endpoint
    """
    _up = "is up and running"
    _down = "is down"
    _open_subtitle_status = OpenSubtitleCrawler().server_status()
    if _open_subtitle_status:
        click.secho(f"OpenSubtitle {_up}", fg="green", bold=True)
    else:
        click.secho(f"OpenSubtitle {_down}", fg="red", bold=True)


@main.command()
@click.pass_context
def config(ctx):
    """
    store OpenSubtitle credentials in a file.
    """
    config_file = ctx.obj['config_file']

    username = click.prompt("Please enter your OpenSubtitle username", default=ctx.obj.get('username', ''))
    password = click.prompt("Please enter your OpenSubtitle password", default=ctx.obj.get('password', ''))

    with open(config_file, 'w') as cfg:
        cfg.write(username+"\n")
        cfg.write(password+"\n")
        cfg.write("TemporaryUserAgent")


@main.command()
@click.pass_context
@click.option('--movielist', '-ml', default="", help='the name of the movielist', type=str)
@click.option('--movie', '-m', default="", help='the name of the movie', type=str)
def download(ctx, movielist, movie):
    """
    download a movie or a movielist from OpenSubtitle.
    """
    if not(movielist or movie):
        click.secho(f"Provide a movie or movielist via '--movie' or '--movielist'", fg="red", bold=True)
    else:
        _imdb_ids = read_ids_from_csv(movielist, input_folder)
        _opensubtitle_crawler = OpenSubtitleCrawler(ctx.obj.get('username'), ctx.obj.get('password'), ctx.obj.get('agent'), download_folder)
        _imdb_crawler = ImdbCrawler(download_folder)

        print_method_result_to_user(_opensubtitle_crawler.login())
        _meta_subtitles = _opensubtitle_crawler.search_subtitles_by_id(_imdb_ids)
        _opensubtitle_crawler.download_subtitles(_meta_subtitles)

        _imdb_crawler.download_movie_info_by_ids(_imdb_ids)

        # _crawler = OpenSubtitleCrawler(ctx.obj.get('username'), ctx.obj.get('password'))
        # print_method_result_to_user(_crawler.login())
        # if movie:
        #     _status, _movies_found = _crawler.search_subtitles({"query": movie, "season": "", "episode": ""})
        #
        # if movielist:
        #     _list_of_movies = read_from_xlsx_file(movielist, './input/')
        #     _status, _movies_found = _crawler.search_subtitles(*_list_of_movies)
        #
        # print_method_result_to_user(_status, _movies_found)
        # print_method_result_to_user(_crawler.logout())

@main.command()
@click.pass_context
@click.option('--movie', '-m', default="", help='the name of the movie', type=str)
def search(ctx, movie):
    """
    search a movie on OpenSubtitle.
    """
    if not movie:
        click.secho(f"Provide a movie via '--movie'", fg="red", bold=True)
    else:
        _crawler = OpenSubtitleCrawler(ctx.obj.get('username'), ctx.obj.get('password'))
        print_method_result_to_user(_crawler.login())
        _status, _movies_found = _crawler.search_subtitles({"query": movie, "season": "", "episode": ""})
        print_method_result_to_user(_status, _movies_found)
        print_method_result_to_user(_crawler.logout())

@main.command()
def files():
    """
    list all downloaded files.
    """
    pass


if __name__ == '__main__':
    main()



