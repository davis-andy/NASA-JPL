import eel
import backend.globals.expose
from backend.globals import splash_screen
from backend.globals.settings import WINDOW_WIDTH, WINDOW_HEIGHT, logger


def main_program():
    # Set web files folder and optionally specify which file types to check for eel.expose()
    #   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
    eel.init('frontend')

    logger.info('Program Loaded')
    splash_screen.window.destroy()

    eel.start('templates/globals/main.html', size=(WINDOW_WIDTH, WINDOW_HEIGHT), jinja_templates='templates')


if __name__ == '__main__':
    splash_screen.mainloop()
