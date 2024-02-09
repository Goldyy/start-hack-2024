from nicegui import ui


def start_frontend(*args, **kwargs):
    ui.label("Hello NiceGUI!")

    ui.run()
