from marvin import ui
from marvin.app import App
from marvin.adb import ADBError

def parser():
    pass
 
def main():
    parser()

    try:
        application = App()
        ui.run(application.run)
        print('Quiting')

    except KeyboardInterrupt:
        print('Quiting')

    """ Overprotecting error handling (for release)
    except NameError:
        pass
    except ADBError as e:
        print('Adb error: {}'.format(e))

    except ui.UIError:
        print('A UI error occurd')

    except Exception as e:
        print('Unexpected error occurd: {}'.format(e));
    """