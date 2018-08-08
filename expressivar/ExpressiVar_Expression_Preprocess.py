import sys

input_filename = str(sys.argv[1])

file_in_Ensembl_Genename = open('Ensembl_GeneName.txt', 'r')

file_in = open(input_filename, 'r')
file_out = open(input_filename + '.expression.txt', 'w')

Ensembl_Gene = dict()
Ensembl_set = set()
for eachline in file_in_Ensembl_Genename:
	component = eachline.strip().split('\t')
	ensembl = component[0]
	gene = component[1]
	Ensembl_Gene[ensembl] = gene
	Ensembl_set.add(ensembl)

file_in.readline()
file_in.readline()
gene_expression_dict_list = dict()
gene_set = set()
for eachline in file_in:
	component = eachline.strip().split('\t')
	ID = component[0].split('.')[0]
	reads = float(component[6])

	if ID in Ensembl_set:
		gene = Ensembl_Gene[ID]
		gene_set.add(gene)
		if gene not in gene_expression_dict_list.keys():
			gene_expression_dict_list[gene] = []
			gene_expression_dict_list[gene].append(reads)
		else:
			gene_expression_dict_list[gene].append(reads)

gene_list = list(gene_set)
gene_list.sort()
for eachgene in gene_list:
	gene_expression_list = gene_expression_dict_list[eachgene]
	gene_expression = sum(gene_expression_list) / len(gene_expression_list)
	file_out.write(eachgene + '\t' + str(round(gene_expression, 3)) + '\n')
