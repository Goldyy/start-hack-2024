from nicegui import app, ui

from hackathon.hackathon.frontend.router import Router
from hackathon.hackathon.frontend.src.pages.home import show_home_page


@ui.page("/")
@ui.page("/{_:path}")  # all other pages will be handled by the
# router but must be registered to also show the SPA index page
def main():
    router = Router()

    @router.add("/")
    def show_home():
        show_home_page()

    @router.add("/chat")
    def show_chat():
        ui.label("Content Two").classes("text-2xl")

    @router.add("/three")
    def show_three():
        ui.label("Content Three").classes("text-2xl")

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button("Home", on_click=lambda: router.open(show_home)).classes("w-32")
        ui.button("Chat", on_click=lambda: router.open(show_chat)).classes("w-32")
        ui.button("Three", on_click=lambda: router.open(show_three)).classes("w-32")

    # this places the content which should be displayed
    router.frame().classes("w-full p-4 bg-gray-100")


def start_frontend(*args, **kwargs):

    app.add_static_files(
        url_path="/favicon", local_directory="hackathon/src/frontend/public/favicon"
    )

    ui.run(
        title="Hackathon Template",
        storage_secret="passwort123",
        favicon="favicon-32x32.png",
    )
