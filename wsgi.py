from web import create_app, clear_filters

app = create_app()

clear_filters()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
