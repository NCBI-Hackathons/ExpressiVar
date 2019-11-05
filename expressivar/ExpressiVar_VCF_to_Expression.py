def vcf_to_expression(rnaseq_file, input_vcf, outfile=None):
    if outfile is None:
        outfile = input_vcf + '.expression.ann'

    with open(rnaseq_file, 'r') as file_in_RNAseq, open(outfile, 'w') as file_out, open(
        input_vcf
    ) as file_in_VCF:

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
                            expression_annotation += (
                                eachgene + ':' + gene_expression[eachgene] + '|'
                            )
                        else:
                            expression_annotation += eachgene + ':0|'
                file_out.write(eachline.strip() + '\t' + expression_annotation + '\n')


if __name__ == '__main__':
    import sys

    try:
        input_filename_VCF = str(sys.argv[1])
        input_filename_RNAseq = str(sys.argv[2])
    except IndexError:
        sys.exit('Supply input-vcf, rnaseq-file')

    vcf_to_expression(input_filename_RNAseq, input_filename_VCF)
