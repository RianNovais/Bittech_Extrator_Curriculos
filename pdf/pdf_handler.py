import pymupdf  # Este é o módulo PyMuPDF

def extract_curriculum_texts_from_pdf(pdf_path):
    """
    Extrai currículos de um único arquivo PDF usando PyMuPDF.

    Args:
        pdf_path (str): Caminho do arquivo PDF.

    Returns:
        list: Lista de strings, onde cada string contém o texto completo de um currículo.
    """
    curriculum_texts = []

    try:
        # Abre o arquivo PDF com PyMuPDF
        with pymupdf.open(pdf_path) as pdf:
            # Variáveis para controlar a extração dos currículos
            current_curriculum_text = ""
            in_curriculum = False
            total_pages = len(pdf)

            for page_num in range(total_pages):
                # Extrai o texto da página atual com PyMuPDF
                page = pdf[page_num]
                page_text = page.get_text()

                if not page_text:
                    continue

                # Verifica se a página contém "Resumo do CV"
                if "Resumo do CV" in page_text:
                    # Se já estávamos em um currículo, salva o currículo anterior
                    if in_curriculum and current_curriculum_text:
                        curriculum_texts.append(current_curriculum_text.strip())

                    # Inicia um novo currículo
                    current_curriculum_text = page_text
                    in_curriculum = True
                elif in_curriculum:
                    # Continua o currículo atual
                    current_curriculum_text += "\n" + page_text

            # Adiciona o último currículo do PDF se existir
            if in_curriculum and current_curriculum_text:
                curriculum_texts.append(current_curriculum_text.strip())

    except Exception as e:
        print(f"Erro ao processar o arquivo {pdf_path}: {e}")

    return curriculum_texts



# Exemplo de uso
if __name__ == "__main__":
    pdf_path = "C:\\Users\\Rian Novais\\Downloads\\Curriculos\\Recepcionista 32.pdf"
    curriculum_texts = extract_curriculum_texts_from_pdf(pdf_path)

    for i, cv in enumerate(curriculum_texts, 1):
        print(f"=== Currículo {i} ===")
        print(cv) # Mostra apenas os primeiros 200 caracteres
        print()