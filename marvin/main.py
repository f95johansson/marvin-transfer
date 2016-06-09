from marvin import ui
from marvin.app import App
from marvin.adb import ADBError

def parser():
    print('parsing')

def main():
    parser()

    try:
        application = App()
    except ADBError as e:
        print('Adb error: {}'.format(e))

    try:
        ui.run(application.run)

    except KeyboardInterrupt:
        print('Quiting')

    except NameError:
        pass
    """ Overprotecting error handling (for release)    
    except ADBError as e:
        print('Adb error: {}'.format(e))

    except ui.UIError:
        print('A UI error occurd')

    except Exception as e:
        print('Unexpected error occurd: {}'.format(e));
    """