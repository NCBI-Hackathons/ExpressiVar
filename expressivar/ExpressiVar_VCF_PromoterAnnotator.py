DEFAULT_PROMOTER_DB = 'Promoter_Library_hg19.txt'


def annotate_effective_promoters(infile, outfile=None,
                                 promoterdb=DEFAULT_PROMOTER_DB):
    if outfile is None:
        outfile = infile + '.promoter.ann'

    # validate filename extension
    if not infile.endswith('vcf'):
        raise ArgumentError(input_filename)

    with open(input_filename, 'r') as file_in,\
        open(outfile, 'w') as file_out,\
            open(promoterdb) as file_prompter:

        chr_promoter_ranges_dict = dict()
        chr_promoter_ranges_gene_dict = dict()
        for eachpromoter in file_prompter:
            component = eachpromoter.strip().split('\t')
            CHROM = component[0]
            START = component[1]
            END = component[2]
            RANGE = START + '-' + END
            GENE = component[4]

            if CHROM not in chr_promoter_ranges_dict:
                chr_promoter_ranges_dict[CHROM] = set()
                chr_promoter_ranges_dict[CHROM].add(RANGE)
                chr_promoter_ranges_gene_dict[CHROM] = dict()
                chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE
            else:
                chr_promoter_ranges_dict[CHROM].add(RANGE)
                chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE

        match_line = 0
        match_promoter = 0
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
                            elif START >= promoter_START and\
                                    END <= promoter_END:
                                    MESSAGE = 'internal_hit'
                            elif (promoter_START <= START <= promoter_END) and\
                                    END > promoter_END:
                                    MESSAGE = 'down_hit'
                            elif START < promoter_START and \
                                    (promoter_START <= END <= promoter_END):
                                    MESSAGE = 'up_hit'

                            if MESSAGE != '':
                                promoter_RANGE = str(promoter_START) + \
                                    '-' + str(promoter_END)
                                promoter_GENE = chr_promoter_ranges_gene_dict[CHROM][promoter_RANGE]
                                promoter_OUTPUT = promoter_GENE + ':' + MESSAGE
                                OUTPUT_set.add(promoter_OUTPUT)
                                match_promoter += 1

                        if OUTPUT_set:
                            OUTPUT = ''
                            for eachOUTPUT in OUTPUT_set:
                                    OUTPUT += eachOUTPUT + ','
                            match_line += 1
                            fields = [CHROM, str(POS), ID, REF, ALT, OUTPUT]
                            out_line = '\t'.join(fields) + '\n'
                            file_out.write(out_line)


if __name__ == '__main__':
    import sys
    try:
        input_filename = str(sys.argv[1])
    except IndexError:
        sys.exit('Supply input-file, output-file')

    annotate_effective_promoters(input_filename)
