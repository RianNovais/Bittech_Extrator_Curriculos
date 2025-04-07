

class Curriculum:
    def __init__(self, data_cv: dict[str, str]):
        # Informações básicas
        self.nome = data_cv.get('nome', 'Nome Não Encontrado')
        self.email = data_cv.get('email', 'Email Não Encontrado')
        self.telefones = data_cv.get('telefone', 'Telefone Não Encontrado')

        # Obter experiências
        experiencias = data_cv.get('experiencias', [])

        # Primeira experiência
        if len(experiencias) > 0:
            self.primeiraempresa = experiencias[0].get('empresa', 'Empresa Não Encontrada')
            self.primeirocargo = experiencias[0].get('cargo', 'Cargo Não Encontrado')
            self.primeiroperiodo = experiencias[0].get('periodo', 'Período Não Encontrado')
        else:
            self.primeiraempresa = 'Empresa Não Encontrada'
            self.primeirocargo = 'Cargo Não Encontrado'
            self.primeiroperiodo = 'Período Não Encontrado'

        # Segunda experiência
        if len(experiencias) > 1:
            self.segundaempresa = experiencias[1].get('empresa', 'Empresa Não Encontrada')
            self.segundocargo = experiencias[1].get('cargo', 'Cargo Não Encontrado')
            self.segundoperiodo = experiencias[1].get('periodo', 'Período Não Encontrado')
        else:
            self.segundaempresa = 'Empresa Não Encontrada'
            self.segundocargo = 'Cargo Não Encontrado'
            self.segundoperiodo = 'Período Não Encontrado'