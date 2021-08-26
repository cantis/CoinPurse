from web import create_app, clear_filters

application = create_app()

clear_filters()

if __name__ == '__main__':
    application.run()
