import flet as ft
from commands import (
    copy_file,
    delete_path,
    count_files,
    search_files,
    add_date_to_filenames,
    analyse_directory,
)
import os
import re


def main(page: ft.Page):
    page.title = "fileMan1 GUI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.window_min_width = 800
    page.window_min_height = 600

    # File picker control
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    # UI Components
    command_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("copy", "Copy file"),
            ft.dropdown.Option("delete", "Delete path"),
            ft.dropdown.Option("count", "Count files"),
            ft.dropdown.Option("search", "Search files"),
            ft.dropdown.Option("add-date", "Add creation date"),
            ft.dropdown.Option("analyse", "Analyse directory"),
        ],
        label="Select command",
        hint_text="Choose file operation",
        width=300,
        autofocus=True,
    )

    source_path = ft.TextField(
        label="Source path",
        hint_text="Select source file or directory",
        expand=True,
        tooltip="Use button to browse or enter path manually",
    )

    additional_input = ft.TextField(
        label="Additional input",
        hint_text="Enter regex/destination depending on command",
        visible=False,
        expand=True,
    )

    recursive_checkbox = ft.Checkbox(
        label="Recursive processing",
        tooltip="Applies to add-date command",
        visible=False
    )

    result_display = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
    )

    # Dynamic UI Updates
    def update_ui(command):
        additional_input.visible = command in ["copy", "search"]
        recursive_checkbox.visible = command == "add-date"

        source_path.label = "Source path" if command != "analyse" else "Directory path"
        additional_input.label = (
            "Destination path" if command == "copy" else
            "Regex pattern" if command == "search" else
            "Additional input"
        )

        page.update()

    # Handlers
    def command_changed(e):
        update_ui(command_dropdown.value)

    def pick_source(e):
        if command_dropdown.value in ["analyse", "count", "add-date"]:
            file_picker.get_directory_path()
        else:
            file_picker.pick_files()

    def execute_command(e):
        try:
            result_display.controls.clear()
            cmd = command_dropdown.value
            source = source_path.value
            result_text = ""

            if not source or not os.path.exists(source):
                raise FileNotFoundError("Source path is invalid")

            if cmd == "copy":
                dest = additional_input.value
                if not dest:
                    raise ValueError("Destination path is required")
                copy_file(source, dest)
                result_text = f"Copied {source} to {dest}"

            elif cmd == "delete":
                delete_path(source)
                result_text = f"Deleted {source}"

            elif cmd == "count":
                count = count_files(source)
                result_text = f"Total files: {count}"

            elif cmd == "search":
                pattern = additional_input.value
                if not pattern:
                    raise ValueError("Regex pattern is required")
                matches = search_files(source, pattern)
                result_text = "Found files:\n" + "\n".join(matches)

            elif cmd == "add-date":
                add_date_to_filenames(source, recursive_checkbox.value)
                result_text = "Dates added to filenames"

            elif cmd == "analyse":
                analyse_directory(source)
                result_text = "Analysis completed"

            result_display.controls.append(
                ft.Text(result_text, color=ft.colors.GREEN))

        except Exception as e:
            result_display.controls.append(
                ft.Text(f"Error: {str(e)}", color=ft.colors.RED)
            )
        finally:
            page.update()

    # File picker results handling
    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.path:
            source_path.value = e.path
            page.update()
        elif e.files:
            source_path.value = e.files[0].path
            page.update()

    file_picker.on_result = on_dialog_result

    # Layout
    page.add(
        ft.Column([
            ft.Row([
                command_dropdown,
                ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE,
                    tooltip="Select a command from the dropdown",
                )
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Divider(),

            ft.Row([
                ft.ElevatedButton(
                    "Browse source",
                    icon=ft.icons.FOLDER_OPEN,
                    on_click=pick_source,
                ),
                source_path,
            ]),

            ft.Row([
                additional_input,
                ft.Container(recursive_checkbox, padding=10),
            ], visible=additional_input.visible),

            ft.ElevatedButton(
                "Execute Command",
                icon=ft.icons.PLAY_ARROW,
                on_click=execute_command,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_200,
                    color=ft.colors.BLACK
                )
            ),

            ft.Text("Results:", weight=ft.FontWeight.BOLD),
            ft.Container(
                result_display,
                border=ft.border.all(1, ft.colors.GREY_400),
                padding=10,
                expand=True,
            )
        ], expand=True)
    )


if __name__ == "__main__":
    ft.app(target=main)
