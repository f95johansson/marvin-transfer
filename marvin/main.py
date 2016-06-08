import ui
from app import App

def parser():
    print('parsing')

def main():
    parser()
    application = App()

    try:
        ui.run(application.run)
    except KeyboardInterrupt:
        print('Quiting')

    """ Overprotecting error handling (for release)    
    except ui.UIError:
        print('A UI error occurd')
    except Exception as e:
        print('Unexpected error occurd: {}'.format(e));
    """