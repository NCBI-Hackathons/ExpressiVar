import sys

input_filename = str(sys.argv[1])

file_in = open(input_filename, 'r')
file_out = open(input_filename + '.promoter.ann', 'w')

file_prompter = open('Promoter_Library_hg19.txt', 'r')
chr_promoter_ranges_dict = dict()
chr_promoter_ranges_gene_dict = dict()
for eachpromoter in file_prompter:
    component = eachpromoter.strip().split('\t')
	CHROM = component[0]
	START = component[1]
	END = component[2]
	RANGE = START + '-' + END
	GENE = component[4]

	if CHROM not in chr_promoter_ranges_dict.keys():
		chr_promoter_ranges_dict[CHROM] = set()
		chr_promoter_ranges_dict[CHROM].add(RANGE)
		chr_promoter_ranges_gene_dict[CHROM] = dict()
		chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE
	else:
		chr_promoter_ranges_dict[CHROM].add(RANGE)
		chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE

match_line = 0
match_promoter = 0
if input_filename.endswith('vcf'):
	for eachline in file_in:
		if not eachline.startswith('#'):
			component = eachline.strip().split('\t')
			CHROM = component[0]
			POS = int(component[1])
			ID = component[2]
			REF = component[3]
			ALT = component[4]
			START = POS
			END = POS + len(REF) - 1
			if not CHROM.startswith('chr'):
				CHROM = 'chr' + CHROM

			OUTPUT_set = set()
			if CHROM in chr_promoter_ranges_dict.keys():
				for each_RANGE in chr_promoter_ranges_dict[CHROM]:
					each_RANGE_INFO = each_RANGE.split('-')
					promoter_START = int(each_RANGE_INFO[0])
					promoter_END = int(each_RANGE_INFO[1])
					MESSAGE = ''
					if START <= promoter_START and END >= promoter_END:
						MESSAGE = 'complete_hit'
					elif START >= promoter_START and END <= promoter_END:
						MESSAGE = 'internal_hit'
					elif (promoter_START <= START <= promoter_END) and END > promoter_END:
						MESSAGE = 'down_hit'
					elif START < promoter_START and (promoter_START <= END <= promoter_END):
						MESSAGE = 'up_hit'

					if MESSAGE != '':
						promoter_RANGE = str(promoter_START) + '-' + str(promoter_END)
						promoter_GENE = chr_promoter_ranges_gene_dict[CHROM][promoter_RANGE]
						promoter_OUTPUT = promoter_GENE + ':' + MESSAGE
						OUTPUT_set.add(promoter_OUTPUT)
						match_promoter += 1

				if OUTPUT_set:
					OUTPUT = ''
					for eachOUTPUT in OUTPUT_set:
						OUTPUT += eachOUTPUT + ','
					match_line += 1
					file_out.write(CHROM+'\t'+str(POS)+'\t'+ID+'\t'+REF+'\t'+ALT+'\t'+OUTPUT+'\n')

print('match_line:\t' + str(match_line))
print('match_promoter:\t' + str(match_promoter))
