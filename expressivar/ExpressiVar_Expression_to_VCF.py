def expression_to_vcf(expression_file, input_vcf, outfile=None):
    with open(expression_file, 'r') as input_filename_Expression, open(
        outfile, 'w'
    ) as file_out, open(input_vcf) as file_in_VCF:

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


if __name__ == '__name__':
    import sys

    try:
        input_filename_Expression = str(sys.argv[1])
        input_filename_VCF = str(sys.argv[2])
    except IndexError:
        sys.exit('Supply expression-file, input-vcf')

    expression_to_vcf(input_filename_Expression, input_filename_VCF)
