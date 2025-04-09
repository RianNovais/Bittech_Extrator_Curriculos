from flet.core.file_picker import FilePickerFile
from pdf.pdf_handler import extract_curriculum_texts_from_pdf
from regexs.regexs import extract_data_from_curriculum_text
from models.curriculum import Curriculum
from excel.excel_handler import ExcelHandler


class Controller:
    def __init__(self, list_files: list[FilePickerFile], output_path: str, on_progress=None):
        self.output_path = output_path
        self.excel_handler = ExcelHandler()
        self.list_files = list_files
        self.list_objects_curriculum = []
        self.on_progress = on_progress  # Função de callback para reportar progresso

    # Processa PDFs com relatório de progresso
    def process_pdfs(self):
        total_files = len(self.list_files)

        for index, file in enumerate(self.list_files):
            # Reporta o progresso atual antes de processar cada arquivo
            if self.on_progress:
                progress_percent = (index / total_files) * 100
                self.on_progress(index, total_files, progress_percent)

            cv_texts = extract_curriculum_texts_from_pdf(file.path)
            for cv_text in cv_texts:
                data_cv = extract_data_from_curriculum_text(cv_text)
                cv_object = Curriculum(data_cv)
                self.list_objects_curriculum.append(cv_object)

        # Reporta 100% antes de gerar o Excel
        if self.on_progress:
            self.on_progress(total_files-1, total_files, 100)

        self.excel_handler.generate_excel(self.list_objects_curriculum, output_path=self.output_path)




    # #Extrai textos de cada PDF e insere em cada Objeto PDFFile no atributo text_extracted
    # def extract_text_pdfs(self):
    #     for pdf in self.list_pdf_files_objects:


# p = Controller([FilePickerFile(name='Recepcionista 31.pdf', path='C:\\Users\\Rian Novais\\Downloads\\Curriculos\\Recepcionista 30.pdf', size=10)])
# p.process_pdfs()

