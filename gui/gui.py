import flet as ft
import os
from controller.controller import Controller


def main(page: ft.Page):
    # Configuração da página
    page.title = "I.A Bittech System 1.0.2"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window_width = 800
    page.window_height = 700
    page.window_resizable = True  # Permitir redimensionamento pode ser útil
    page.window.maximizable = False  # Permitir maximizar
    page.window.center()
    page.update()

    # Lista para armazenar os arquivos selecionados
    selected_files = []
    output_path = ""

    # Função para atualizar a lista de arquivos
    def update_file_list():
        file_list.controls.clear()
        if not selected_files:
            file_list.controls.append(
                ft.Text("Nenhum arquivo selecionado",
                        color=ft.colors.GREY_500,
                        size=14)
            )
        else:
            for file in selected_files:
                file_list.controls.append(
                    ft.Row([
                        ft.Icon(ft.icons.DESCRIPTION, color=ft.colors.BLUE_500),
                        ft.Text(os.path.basename(file.path), size=14),
                    ])
                )
        page.update()

    # Callbacks para os seletores de arquivo
    def pick_pdf_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_files.extend(e.files)
            update_file_list()
            process_button.disabled = False if selected_files and output_path else True
            page.update()

    def pick_output_result(e: ft.FilePickerResultEvent):
        nonlocal output_path
        if e.path:
            output_path = e.path
            output_text.value = output_path
            process_button.disabled = False if selected_files and output_path else True
            page.update()

    # Barra de progresso e textos de status
    progress_bar = ft.ProgressBar(width=400, value=0, visible=False)
    progress_text = ft.Text("", visible=False)
    progress_ring = ft.ProgressRing(visible=False)
    status_text = ft.Text("", visible=False, size=14)

    # Função para processar os PDFs
    def process_files(e):
        if not selected_files or not output_path:
            return

        # Mostrar indicador de progresso
        progress_ring.visible = True
        progress_bar.visible = True
        progress_text.visible = True
        status_text.visible = True
        status_text.value = "Processando informações..."
        process_button.disabled = True
        page.update()

        # Função de callback de progresso
        def update_progress(current, total, percent):
            progress_text.value = f"Processando arquivo {current+1} de {total} ({percent:.1f}%)"
            progress_bar.value = percent / 100  # ProgressBar espera valor entre 0-1
            page.update()

        try:
            # Criar e executar o controlador com callback de progresso
            controller = Controller(selected_files, output_path, on_progress=update_progress)
            controller.process_pdfs()

            # Atualizar UI com sucesso
            status_text.value = f"{len(selected_files)} arquivo(s) processados com sucesso!"
            status_text.color = ft.colors.GREEN_500

        except Exception as ex:
            # Atualizar UI com erro
            status_text.value = f"Erro ao processar: {str(ex)}"
            status_text.color = ft.colors.RED_500

        # Restaurar UI
        progress_ring.visible = False
        progress_bar.visible = False
        progress_text.visible = False
        process_button.disabled = False
        page.update()

    def clear_selected_files():
        selected_files.clear()
        update_file_list()
        process_button.disabled = True
        page.update()

    # Seletores de arquivo
    pdf_picker = ft.FilePicker(on_result=pick_pdf_result)
    output_picker = ft.FilePicker(on_result=pick_output_result)
    page.overlay.extend([pdf_picker, output_picker])

    # Criação dos widgets
    header = ft.Container(
        content=ft.Column([
            ft.Text("I.A Bittech System", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Gerador de Leads", size=16, color=ft.colors.GREY_700)
        ]),
        margin=ft.margin.only(bottom=15)  # Reduzido o espaçamento
    )

    # Área de arquivos - altura reduzida para economizar espaço
    file_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        height=120,  # Reduzido de 150 para 120
        spacing=5
    )

    # Atualiza a lista de arquivos inicialmente
    update_file_list()

    # Área de entrada de arquivos
    file_section = ft.Container(
        content=ft.Column([
            ft.Text("Arquivos PDF", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=file_list,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                padding=10,  # Reduzido padding de 15 para 10
                expand=True
            ),
            ft.Row([
                ft.ElevatedButton(
                    "Selecionar Arquivos PDF",
                    icon=ft.icons.PICTURE_AS_PDF,
                    on_click=lambda _: pdf_picker.pick_files(
                        allow_multiple=True,
                        allowed_extensions=["pdf"]
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.GREEN_50,
                        shape=ft.RoundedRectangleBorder(radius=6),
                        padding=ft.padding.only(left=15, right=15, top=10, bottom=10)  # Reduzido padding
                    )
                ),
                ft.ElevatedButton(
                    "Limpar Arquivos",
                    icon=ft.icons.DELETE_SWEEP,
                    on_click=lambda _: clear_selected_files(),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.RED_100,
                        color=ft.colors.RED_700,
                        shape=ft.RoundedRectangleBorder(radius=6),
                        padding=ft.padding.only(left=15, right=15, top=10, bottom=10)  # Reduzido padding
                    )
                )
            ])
        ]),
        margin=ft.margin.only(bottom=15)  # Reduzido o espaçamento
    )

    # Área de saída
    output_text = ft.Text("Nenhum diretório selecionado", size=14, color=ft.colors.GREY_500)
    output_section = ft.Container(
        content=ft.Column([
            ft.Text("Local de Saída", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=output_text,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                padding=10,  # Reduzido padding
                width=page.width - 80
            ),
            ft.ElevatedButton(
                "Selecionar Local",
                icon=ft.icons.OUTPUT,
                on_click=lambda _: output_picker.save_file(
                    file_name="Leads Extraídos.xlsx",
                    allowed_extensions=["xlsx"]
                ),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.only(left=15, right=15, top=10, bottom=10)  # Reduzido padding
                )
            )
        ]),
        margin=ft.margin.only(bottom=15)  # Reduzido o espaçamento
    )

    # Botão de processamento
    process_button = ft.ElevatedButton(
        "Iniciar Processamento da I.A",
        icon=ft.icons.PLAY_ARROW,
        on_click=process_files,
        disabled=True,
        style=ft.ButtonStyle(
            color={
                "": ft.colors.WHITE,
                "disabled": ft.colors.WHITE
            },
            bgcolor={
                "": ft.colors.BLUE,
                "disabled": ft.colors.BLUE_GREY_200
            },
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.only(left=20, right=20, top=15, bottom=15)
        )
    )

    # Área de processamento - centralizada
    process_section = ft.Container(
        content=ft.Column([
            ft.Row([
                process_button,
                progress_ring,
                status_text
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Container(
                content=ft.Column([
                    progress_bar,
                    progress_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5),
                alignment=ft.alignment.center,
                width=page.width - 60  # Definir largura completa
            )
        ]),
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=15)  # Reduzido o espaçamento
    )

    # Montagem da interface - removido o rodapé com "2025"
    page.add(
        header,
        file_section,
        output_section,
        ft.Divider(height=5),  # Reduzido altura do divisor
        process_section
    )