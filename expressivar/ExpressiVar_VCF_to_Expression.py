import sys

input_filename_VCF = str(sys.argv[1])
input_filename_Expression = str(sys.argv[2])

file_in_VCF = open(input_filename_VCF, 'r')
file_in_Expression = open(input_filename_Expression, 'r')

file_out = open(input_filename_VCF + '.expression.ann', 'w')

gene_expression_zeroset = set()
gene_expression = dict()
for eachline in file_in_RNAseq:
	component = eachline.strip().split('\t')
	gene = component[0]
	expression = component[1]
	if float(expression) == 0:
		gene_expression_zeroset.add(gene)
	else:
		gene_expression[gene] = expression

for eachline in file_in_VCF:
	if eachline.startswith('#'):
		file_out.write(eachline)
		pass
	else:
		component = eachline.strip().split('\t')
		INFO = component[7].split(';')
		gene_set = set()
		for eachINFO in INFO:
			if eachINFO.startswith('ANN'):
				ANN = eachINFO[4:].split(',')
				for eachANN in ANN:
					ANN_field = eachANN.split('|')
					gene = ANN_field[3]
					gene_set.add(gene)

		expression_annotation = ''
		if len(gene_set) == 0:
			expression_annotation = '.'
		else:
			for eachgene in gene_set:
				if eachgene in gene_expression_zeroset:
					expression_annotation += eachgene + ':0|'
				elif eachgene in gene_expression.keys():
					expression_annotation += eachgene + ':' + gene_expression[eachgene] + '|'
				else:
					expression_annotation += eachgene + ':0|'

		file_out.write(eachline.strip() + '\t' + expression_annotation + '\n')
