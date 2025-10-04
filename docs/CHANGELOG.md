# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Adicionado
- Toast/notificação reposicionado para canto inferior direito
- Otimizações específicas para mobile PWA
- Responsividade inteligente para dispositivos móveis
- Classe CSS `.toast-mobile` para melhor UX em dispositivos móveis
- Ajustes para modo standalone (PWA instalado)
- Documentação completa das melhorias UX em `docs/MELHORIAS_UX.md`

### Melhorado
- Sistema de classificação de intenções expandido de 6 para 16 tipos
- Detecção híbrida (IA + palavras-chave) para maior precisão
- Templates contextuais específicos para cada tipo de intenção
- Categorização refinada entre emails produtivos e improdutivos
- Interface mais intuitiva seguindo convenções mobile nativas

### Corrigido
- Erro de sintaxe em `app/responders.py` (caracteres de escape inválidos)
- Posicionamento inadequado de notificações em dispositivos móveis

### Documentação
- Criado `docs/MELHORIAS_UX.md` com detalhes das melhorias de interface
- Atualizado `README.md` com novas funcionalidades
- Atualizado índice de documentação em `docs/INDICE_DOCUMENTACAO.md`
- Criado `CHANGELOG.md` para rastreamento de mudanças

## [1.0.0] - 03 de Outubro de 2025

### Adicionado
- Sistema de classificação de emails com IA
- Interface web moderna com dark mode
- Progressive Web App (PWA) com instalação offline
- Persistência local de dados
- Auto-refresh inteligente
- Sistema de templates de resposta
- Gráficos de confiança visuais
- Otimizações de memória para deployment
- Documentação técnica completa