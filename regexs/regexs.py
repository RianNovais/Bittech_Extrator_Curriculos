import re


def extract_name(text):
    nome_match = re.search(r'Nome:([^0-9\n/]+)', text)
    if nome_match and nome_match.group(1).strip():
        return nome_match.group(1).strip()
    return "Não Encontrado"


def extract_email(text):
    email_match = re.search(r'E-mail:\s*([\w.-]+@[\w.-]+\.\w+)', text)
    if email_match:
        return email_match.group(1).strip()
    return "Não Encontrado"


def extract_telephones(text):
    # Procura pelo padrão "Telefone(s):" seguido de números de telefone
    telefone_pattern = re.search(r'Telefone\(s\):(.*?)(?:\n\n|\n[A-Za-z]|$)', text, re.DOTALL)

    if not telefone_pattern:
        return "Não Encontrado"

    telefone_text = telefone_pattern.group(1).strip()

    # Extrair os números de telefone do texto encontrado
    telefones = []
    telefone_matches = re.finditer(r'\((\d+)\)\s*(\d+[-\s]?\d+)', telefone_text)

    for telefone_match in telefone_matches:
        telefones.append(f"({telefone_match.group(1)}) {telefone_match.group(2)}")

    if telefones:
        return " ".join(telefones)
    return "Não Encontrado"


def extract_work_experiences(texto):
    # Encontrar a seção de experiência profissional
    if "Experiência Profissional" in texto:
        texto_exp = texto.split("Experiência Profissional")[1]
        if "Formação" in texto_exp:
            texto_exp = texto_exp.split("Formação")[0]
    else:
        texto_exp = texto

    # ADICIONANDO NOVA SEÇÃO NO INÍCIO PARA CASOS ESPECÍFICOS COM "ÚLTIMO CARGO"
    padrao_ultimo_cargo = r'([^\n]+?)[\n\r]+Cargo:\s*([^-\n]+?)\s*-\s*Último cargo\s*-\s*(\d{2}/\d{4})\s*-\s*(Atual|atual)(?:\s*-\s*([^\n]*?))?'
    matches_ultimo_cargo = re.finditer(padrao_ultimo_cargo, texto_exp, re.MULTILINE)

    experiencias = []
    for match in matches_ultimo_cargo:
        empresa = match.group(1).strip()
        cargo = match.group(2).strip()
        data_inicio = match.group(3).strip()
        atual = match.group(4).strip()
        duracao = match.group(5).strip() if match.group(5) else ""

        periodo_completo = f"{data_inicio} - {atual}"
        if duracao:
            periodo_completo = f"{data_inicio} - {atual} - {duracao}"

        experiencias.append({
            'empresa': empresa,
            'cargo': cargo,
            'periodo': periodo_completo
        })

    # Primeiro, vamos tentar uma abordagem que identifica blocos completos
    if not experiencias:  # Só processa se ainda não encontrou experiências
        padrao_bloco = r'([^\n]+?)(?:\n|\r\n)Cargo:\s*([^-\n]+?)\s*-\s*(\d{2}/\d{4}(?:\s*(?:até|-|a)?\s*(?:\d{2}/\d{4}|Atual|atual))?)(?:\s*-\s*([^\n]*?))?(?=\s*\n)'

        matches = re.finditer(padrao_bloco, texto_exp, re.MULTILINE)

        for match in matches:
            empresa = match.group(1).strip()
            cargo = match.group(2).strip()
            periodo_datas = match.group(3).strip()
            duracao = match.group(4).strip() if match.group(4) else ""

            # Verificar se a empresa parece válida
            if not empresa.lower().startswith(('principais atividades', 'funções', 'período')):
                # Combinar período e duração
                periodo_completo = periodo_datas
                if duracao:
                    periodo_completo = f"{periodo_datas} - {duracao}"

                experiencias.append({
                    'empresa': empresa,
                    'cargo': cargo,
                    'periodo': periodo_completo
                })

    # Se não encontrou experiências com o primeiro método, tente o método original
    if not experiencias:
        # Dividir o texto em possíveis blocos de experiência
        blocos = re.split(r'\n(?=[A-Z][^\n]{3,}\n)', texto_exp)

        for bloco in blocos:
            if not bloco.strip():
                continue

            # Primeira linha não vazia deve ser a empresa
            linhas = bloco.strip().split('\n')
            empresa = linhas[0].strip()

            # Verificar se é uma empresa válida
            if len(empresa) < 150 and not empresa.lower().startswith(('principais atividades', 'funções', 'período')):
                # Buscar cargo
                cargo_match = re.search(r'Cargo:\s*([^-\n]+)', bloco)
                cargo = cargo_match.group(1).strip() if cargo_match else "Cargo Não Encontrado"

                # Buscar período
                periodo_match = re.search(
                    r'(\d{2}/\d{4}(?:\s*(?:até|-|a)?\s*(?:\d{2}/\d{4}|Atual|atual))?)(?:\s*-\s*([^\n]*?))?', bloco)

                if periodo_match:
                    periodo_datas = periodo_match.group(1).strip()
                    duracao = periodo_match.group(2).strip() if periodo_match.group(2) else ""

                    periodo_completo = periodo_datas
                    if duracao:
                        periodo_completo = f"{periodo_datas} - {duracao}"
                else:
                    periodo_completo = "Período Não Encontrado"

                experiencias.append({
                    'empresa': empresa,
                    'cargo': cargo,
                    'periodo': periodo_completo
                })

    # Se ainda não encontrou nada, usar o método mais genérico
    if not experiencias:
        # Tentar o método completo do código original
        empresas = re.findall(r'([^\n]+?)[\r\n]+(?:Cargo:|Período:|Função:)', texto_exp)

        for empresa in empresas:
            empresa = empresa.strip()

            # Buscar cargo para esta empresa
            padrao_cargo = rf'{re.escape(empresa)}[\r\n]+Cargo:\s*([^-\n]+?)(?:\s*-|\n)'
            cargo_match = re.search(padrao_cargo, texto_exp)
            cargo = cargo_match.group(1).strip() if cargo_match else "Cargo Não Encontrado"

            # Buscar período para esta empresa
            padrao_periodo = rf'{re.escape(empresa)}[\r\n]+.*?(?:Cargo:|Período:).*?(\d{{2}}/\d{{4}}(?:\s*(?:até|-|a)?\s*(?:\d{{2}}/\d{{4}}|Atual|atual))?)(?:\s*-\s*([^\n]*?))?(?=\s*\n)'
            periodo_match = re.search(padrao_periodo, texto_exp, re.DOTALL)

            if not periodo_match:
                padrao_periodo_generico = rf'{re.escape(empresa)}[\r\n]+.*?(\d{{2}}/\d{{4}}(?:\s*(?:até|-|a)?\s*(?:\d{{2}}/\d{{4}}|Atual|atual))?)(?:\s*-\s*([^\n]*?))?(?=\s*\n)'
                periodo_match = re.search(padrao_periodo_generico, texto_exp, re.DOTALL)

            if periodo_match:
                periodo_datas = periodo_match.group(1).strip()
                duracao = periodo_match.group(2).strip() if periodo_match.group(2) else ""

                periodo_completo = periodo_datas
                if duracao:
                    periodo_completo = f"{periodo_datas} - {duracao}"
            else:
                periodo_completo = "Período Não Encontrado"

            experiencias.append({
                'empresa': empresa,
                'cargo': cargo,
                'periodo': periodo_completo
            })

    # E se ainda não encontrou nada, usar os últimos recursos conforme o código original
    if not experiencias:
        # O código completo dos métodos de último recurso aqui
        padrao_cargo_primeiro = r'Cargo:\s*([^\n]+?)[\r\n]+.*?(?:Último salário|Principais atividades)'
        cargos = re.finditer(padrao_cargo_primeiro, texto_exp, re.DOTALL)

        for match in cargos:
            cargo_bloco = match.group(0)
            cargo = match.group(1).strip()

            # Tentar encontrar a empresa olhando para as linhas anteriores ao cargo
            linhas = texto_exp.split('\n')
            empresa_encontrada = False
            for i, linha in enumerate(linhas):
                if f"Cargo: {cargo}" in linha and i > 0:
                    empresa = linhas[i - 1].strip()
                    empresa_encontrada = True
                    break

            if not empresa_encontrada:
                empresa = "Empresa Não Encontrada"

            # Tentar encontrar o período no bloco do cargo
            padrao_periodo = r'(\d{2}/\d{4}(?:\s*(?:até|-|a)?\s*(?:\d{2}/\d{4}|Atual|atual))?)(?:\s*-\s*([^\n]*?))?'
            periodo_match = re.search(padrao_periodo, cargo_bloco)

            if periodo_match:
                periodo_datas = periodo_match.group(1).strip()
                duracao = periodo_match.group(2).strip() if periodo_match.group(2) else ""

                periodo_completo = periodo_datas
                if duracao:
                    periodo_completo = f"{periodo_datas} - {duracao}"
            else:
                periodo_completo = "Período Não Encontrado"

            experiencias.append({
                'empresa': empresa,
                'cargo': cargo,
                'periodo': periodo_completo
            })

        # E o método de último recurso
        if not experiencias:
            padrao_simples = r'([A-Z][^\n]{3,}?)[\r\n]+(?:.*?Cargo:\s*([^\n]+))?'
            matches = re.finditer(padrao_simples, texto_exp)

            for match in matches:
                empresa = match.group(1).strip()
                cargo = match.group(2).strip() if match.group(2) else "Cargo Não Encontrado"

                experiencias.append({
                    'empresa': empresa,
                    'cargo': cargo,
                    'periodo': "Período Não Encontrado"
                })

    # Retornar as 2 experiências mais recentes
    return experiencias[:2]


def extract_data_from_curriculum_text(text):
    # Inicializa o dicionário de resultado
    result = {
        "nome": extract_name(text),
        "email": extract_email(text),
        "telefone": extract_telephones(text),
        "experiencias": extract_work_experiences(text)
    }

    return result