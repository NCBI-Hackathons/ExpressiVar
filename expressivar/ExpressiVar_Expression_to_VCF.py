import sys

input_filename_Expression = str(sys.argv[1])
input_filename_VCF = str(sys.argv[2])

file_in_Expression = open(input_filename_Expression, 'r')
file_in_VCF = open(input_filename_VCF, 'r')

file_out = open(input_filename_Expression + '.mutations.ann', 'w')

gene_mutatation_dict = dict()
for eachline in file_in_VCF:
	if eachline.startswith('#'):
		pass
	else:
		component = eachline.strip().split('\t')
		CHROM = component[0]
		POS = component[1]
		REF = component[3]
		ALT = component[4]
		MUTATION = CHROM + '-' + POS + '-' + REF + '-' + ALT
		INFO = component[7].split(';')
		gene_set = set()
		for eachINFO in INFO:
			if eachINFO.startswith('ANN'):
				ANN = eachINFO[4:].split(',')
				for eachANN in ANN:
					ANN_field = eachANN.split('|')
					gene = ANN_field[3]
					if gene not in gene_mutatation_dict.keys():
						gene_mutatation_dict[gene] = []
						gene_mutatation_dict[gene].append(MUTATION)
					else:
						if MUTATION not in gene_mutatation_dict[gene]:
							gene_mutatation_dict[gene].append(MUTATION)

for eachline in file_in_Expression:
	component = eachline.strip().split('\t')
	gene = component[0]
	expression = component[1]
	output = ''
	if gene not in gene_mutatation_dict:
		output = '.\t.'
	else:
		output += 'MUTATIONS:' + str(len(gene_mutatation_dict[gene])) + '\t'
		for eachMUTATION in gene_mutatation_dict[gene]:
			output += eachMUTATION + '|'
	file_out.write(eachline.strip() + '\t' + output + '\n')
