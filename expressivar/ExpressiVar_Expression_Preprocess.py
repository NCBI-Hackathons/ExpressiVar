DEFAULT_ENSEMBLE_DB = 'Ensembl_GeneName.txt'


def preprocess_expressions(infile, outfile=None, ensemble_db=DEFAULT_ENSEMBLE_DB):
    if outfile is None:
        outfile = infile + '.expression.txt'

    with open(input_filename, 'r') as file_in, open(outfile, 'w') as file_out, open(
        ensemble_db
    ) as file_in_Ensembl_Genename:

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
            expr_sum = sum(gene_expression_list)
            gene_expression = expr_sum / len(gene_expression_list)
            file_out.write(eachgene + '\t' + str(round(gene_expression, 3)) + '\n')


if __name__ == '__main__':
    import sys

    try:
        input_filename = str(sys.argv[1])
    except IndexError:
        sys.exit('Supply input-file, output-file')

    preprocess_expressions(input_filename)
