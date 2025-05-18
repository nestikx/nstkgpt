import flet as ft

error_text = """
    A problem has been detected on the website.
    Website closed to prevent damage.

    Unknown_Problem_Error.null
    STOP: 0x00e0null
"""

def main(page: ft.Page):
    page.title = "error"
    page.bgcolor = ft.Colors.BLUE_ACCENT_700
    page.fonts = {"PollyRounded-Bold": "fonts/PollyRounded-Bold.ttf"}
    page.theme = ft.Theme(font_family = "PollyRounded-Bold")

    page.add(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        value = " :(",
                        size = 148,
                        color = "white"
                    ),
                    ft.Text(
                        value = error_text,
                        size = 20,
                        color = "white"
                    )
                ],
                spacing = 80,
                alignment = ft.MainAxisAlignment.CENTER
            ),
            margin = 20
        )
    )