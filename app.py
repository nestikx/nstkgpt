import flet as ft
import asyncio
import os
import gpt

messages = []

class Message(ft.Row):
    def __init__(self, message: str, person: str):
        super().__init__()
        variants = [
            { # position
                "me": ft.MainAxisAlignment.END,
                "bot": ft.MainAxisAlignment.START,
                "system": ft.MainAxisAlignment.CENTER
            },
            { # color
                "me": [ft.Colors.PRIMARY_CONTAINER, ft.Colors.ON_PRIMARY_CONTAINER],
                "bot": [ft.Colors.SURFACE, ft.Colors.ON_SURFACE],
                "system": [ft.Colors.INVERSE_SURFACE, ft.Colors.ON_INVERSE_SURFACE]
            },
            { # size
                "me": 15,
                "bot": 15,
                "system": 12
            },
            { # align
                "me": ft.TextAlign.LEFT,
                "bot": ft.TextAlign.LEFT,
                "system": ft.TextAlign.CENTER
            }
        ]
        self.controls = [
            ft.Container(
                ft.Text(
                    value = message,
                    size = variants[2][person],
                    color = variants[1][person][1],
                    text_align = variants[3][person]
                ),
                padding = 10,
                border_radius = 20,
                bgcolor = variants[1][person][0],
                expand = True,
                expand_loose = True
            )
        ]
        self.alignment = variants[0][person]

async def main(page: ft.Page):
    page.title = "nstk gpt"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"PollyRounded-Bold": "fonts/PollyRounded-Bold.ttf"}
    page.theme = ft.Theme(font_family = "PollyRounded-Bold")

    async def gpt_question(message: str):
        answer = await asyncio.to_thread(gpt.question, message, messages)

        chat.content.controls.append(Message(answer, "bot"))
        chat.content.scroll_to(offset = -1, duration = 200, curve = ft.AnimationCurve.EASE)

        page.update()

    async def click_send(event):
        send_button.content.scale = 1
        page.update()

        await asyncio.sleep(0.1)

        send_button.content.scale = 1.4
        page.update()

        if message_field.value != "":
            chat.content.controls.append(Message(message_field.value, "me"))
            chat.content.scroll_to(offset = -1, duration = 200, curve = ft.AnimationCurve.EASE)

            message = message_field.value
            message_field.value = ""
            
            page.update()
            await gpt_question(message)

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            mode_swich.icon = ft.Icons.SUNNY
        
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            mode_swich.icon = ft.Icons.NIGHTLIGHT_ROUNDED
        
        page.update()
    
    title_text = ft.Text(
        value = "nstk gpt",
        size = 32
    )

    creator_name = ft.Text(
        value = "by nestik",
        size = 16
    )
    
    mode_swich = ft.IconButton(
        icon = ft.Icons.SUNNY,
        icon_size = 30,
        icon_color = ft.Colors.ON_PRIMARY_CONTAINER,
        animate_scale = ft.Animation(duration = 5000, curve = ft.AnimationCurve.EASE),
        on_click = toggle_theme
    )

    send_button = ft.Container(
        ft.Image(
            src = "image/send_duotone.svg",
            scale = 1.4,
            color = ft.Colors.ON_PRIMARY_CONTAINER,
            animate_scale = ft.Animation(duration = 200, curve = ft.AnimationCurve.EASE)
        ),
        ink = True,
        padding = 12,
        border_radius = 40,
        bgcolor = ft.Colors.SURFACE,
        on_click = click_send
    )

    message_field = ft.TextField(
        hint_text = "Enter message",
        border_color = "transparent",
        bgcolor = ft.Colors.SURFACE,
        border_radius = 50,
        multiline = True,
        expand = True
    )

    chat = ft.Container(
        ft.Column(
            [
                Message("active model gpt-4o\napp is unstable!", "system")
            ],
            scroll = ft.ScrollMode.AUTO
        ),
        margin = 10,
        padding = 20,
        border_radius = 25,
        expand = True
    )

    panel = ft.Container(
        ft.Row(
            [
                message_field,
                send_button
            ],
            width = 350
        ),
        margin = 20,
        padding = 20,
        border_radius = 50,
        bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        title_text,
                        ft.Row(
                            [
                                creator_name,
                                mode_swich
                            ],
                            alignment = ft.MainAxisAlignment.END
                        )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                chat,
                panel
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True
        )
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2496))
    ft.app(target = main, view = ft.WEB_BROWSER, port = port)
