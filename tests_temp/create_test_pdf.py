# Script para criar PDF de teste usando fpdf2 (alternativa ao reportlab)
from fpdf import FPDF

# Criar PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

# Adicionar conteúdo
pdf.cell(0, 10, 'Email de Teste - Relatório Mensal', 0, 1, 'C')
pdf.ln(10)

pdf.set_font('Arial', '', 12)
pdf.cell(0, 8, 'Prezados,', 0, 1)
pdf.ln(5)

pdf.cell(0, 8, 'Segue em anexo o relatório mensal de vendas conforme solicitado na reunião de ontem.', 0, 1)
pdf.ln(5)

pdf.cell(0, 8, 'O documento contém:', 0, 1)
pdf.cell(0, 8, '- Análise de performance por região', 0, 1)
pdf.cell(0, 8, '- Comparativo com mês anterior', 0, 1)
pdf.cell(0, 8, '- Projeções para o próximo trimestre', 0, 1)
pdf.ln(10)

pdf.cell(0, 8, 'Favor revisar e me informar se precisam de algum esclarecimento adicional.', 0, 1)
pdf.ln(10)

pdf.cell(0, 8, 'Atenciosamente,', 0, 1)
pdf.cell(0, 8, 'João Silva', 0, 1)
pdf.cell(0, 8, 'Gerente Comercial', 0, 1)

# Salvar PDF
pdf.output('test_email.pdf')
print('PDF criado com sucesso: test_email.pdf')