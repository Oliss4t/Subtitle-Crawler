import os
import click
from openSubtitleCrawler import OpenSubtitleCrawler

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
                click.secho(f"Login credentials could be retrieved", fg="green", bold=True)
    except IndexError:
        click.secho(f"No login credentials could be retrieved", fg="red", bold=True)


    ctx.obj = {
        'username': username,
        'password': password,
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
        cfg.write(password)

@main.command()
@click.pass_context
@click.option('--movielist', '-ml', default="", help='the name of the movielist', type=str)
@click.option('--movie', '-m', default="", help='the name of the movie', type=str)
def download(ctx, movielist, movie):
    """
    download a movie or a movielist from OpenSubtitle.
    """
    if not movielist or not movie:
        click.secho(f"Provide a movie or movielist via '--movie' or '--movielist'", fg="red", bold=True)
    else:
        _crawler = OpenSubtitleCrawler(ctx.obj.get('username'), ctx.obj.get('password'))
        if movie:
            # TODO
            pass
        if movielist:
            # TODO
            pass
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
        # TODO

@main.command()
def files():
    """
    list all downloaded files.
    """
    pass


if __name__ == '__main__':
    main()



