import flet as ft
import asyncio
import os
import gpt


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
                    font_family = "PollyRounded-Bold",
                    color = variants[1][person][1],
                    text_align = variants[3][person]
                ),
                padding = 10,
                border_radius = 10,
                bgcolor = variants[1][person][0],
                expand = True,
                expand_loose = True
            )
        ]
        self.alignment = variants[0][person]

async def main(page: ft.Page):
    page.title = "nstk gpt"
    page.favicon = "favicon.ico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"PollyRounded-Bold": "fonts/PollyRounded-Bold.ttf"}

    async def gpt_question(message: str):
        answer = await asyncio.to_thread(gpt.question, message)

        chat.content.scroll_to(offset = -1, duration = 200, curve = ft.AnimationCurve.EASE)
        chat.content.controls.append(Message(answer, "bot"))

        page.update()

    async def click_send(event: ft.ContainerTapEvent):
        send_icon.scale = 1
        page.update()

        await asyncio.sleep(0.1)

        send_icon.scale = 1.4
        page.update()

        if message_field.value != "":
            chat.content.scroll_to(offset = -1, duration = 200, curve = ft.AnimationCurve.EASE)
            chat.content.controls.append(Message(message_field.value, "me"))
            
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
        size = 32,
        font_family = "PollyRounded-Bold"
    )

    creator_name = ft.Text(
        value = "by nestik",
        size = 16,
        font_family = "PollyRounded-Bold"
    )
    
    mode_swich = ft.IconButton(
        icon = ft.Icons.SUNNY,
        icon_size = 30,
        icon_color = ft.Colors.ON_PRIMARY_CONTAINER,
        animate_scale = ft.Animation(duration = 5000, curve = ft.AnimationCurve.EASE),
        on_click = toggle_theme
    )

    send_icon = ft.Image(
        src = "image/send_duotone.svg",
        scale = 1.4,
        color = ft.Colors.ON_PRIMARY_CONTAINER,
        animate_scale = ft.Animation(duration = 200, curve = ft.AnimationCurve.EASE)
    )

    message_field = ft.TextField(
        hint_text = "Enter message",
        border_radius = 50,
        multiline = True,
        border_color = "transparent",
        bgcolor = ft.Colors.SURFACE
    )

    chat = ft.Container(
        ft.Column(
            [
                Message("active model gpt-4o\nthis version of the program is unstable!", "system")
            ],
            scroll = ft.ScrollMode.AUTO
        ),
        margin = 20,
        padding = 20,
        border_radius = 25,
        bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST,
        expand = True
    )

    panel = ft.Container(
        ft.Row(
            [
                message_field,
                ft.Container(
                    send_icon,
                    ink = True,
                    padding = 12,
                    border_radius = 40,
                    bgcolor = ft.Colors.SURFACE,
                    on_click = click_send
                )
            ]
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

                ft.Row(
                    [
                        panel
                    ],
                    alignment = ft.MainAxisAlignment.CENTER
                )
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            expand = True
        )
    )

port = int(os.environ.get("PORT", 8000))
ft.app(target = main, assets_dir = "assets", view = ft.WEB_BROWSER, port = port)
