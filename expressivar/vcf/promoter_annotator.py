from expressivar.db import DEFAULT_PROMOTER_DB
from expressivar.dec import file_or_path


def annotate_effective_promoters(infile, outfile=None, promoterdb=None):
    if promoterdb is None:
        promoterdb = DEFAULT_PROMOTER_DB

    if outfile is None:
        outfile = infile + '.promoter.ann'

    # validate filename extension
    if not infile.endswith('vcf'):
        raise RuntimeError('{infile} not a vcf file.'.format(infile=infile))

    return _annotate_effective_promoters(infile, outfile, promoterdb)


@file_or_path(infile='r', outfile='w', promoterdb='r')
def _annotate_effective_promoters(infile, outfile, promoterdb):
    chr_promoter_ranges_dict = dict()
    chr_promoter_ranges_gene_dict = dict()
    for promoter in promoterdb:
        component = promoter.strip().split('\t')
        CHROM = component[0]
        START = component[1]
        END = component[2]
        RANGE = START + '-' + END
        GENE = component[4]

        if CHROM not in chr_promoter_ranges_dict:
            chr_promoter_ranges_dict[CHROM] = []
            chr_promoter_ranges_dict[CHROM].append(RANGE)
            chr_promoter_ranges_gene_dict[CHROM] = dict()
            chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE
        else:
            chr_promoter_ranges_dict[CHROM].append(RANGE)
            chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE

    match_line = 0
    match_promoter = 0
    for line in infile:
        if not line.startswith('#'):
            component = line.strip().split('\t')
            CHROM = component[0]
            POS = int(component[1])
            ID = component[2]
            REF = component[3]
            ALT = component[4]
            START = POS
            END = POS + len(REF) - 1
            if not CHROM.startswith('chr'):
                CHROM = 'chr' + CHROM

                OUTPUT_set = []
                if CHROM in chr_promoter_ranges_dict:
                    for each_RANGE in chr_promoter_ranges_dict[CHROM]:
                        promoter_START, promoter_END = map(
                            int, each_RANGE.split('-')
                        )
                        MESSAGE = ''
                        if START <= promoter_START and END >= promoter_END:
                            MESSAGE = 'complete_hit'
                        elif START >= promoter_START and END <= promoter_END:
                            MESSAGE = 'internal_hit'
                        elif (
                            promoter_START <= START <= promoter_END
                        ) and END > promoter_END:
                            MESSAGE = 'down_hit'
                        elif START < promoter_START and (
                            promoter_START <= END <= promoter_END
                        ):
                            MESSAGE = 'up_hit'

                        if MESSAGE != '':
                            promoter_RANGE = (
                                str(promoter_START) + '-' + str(promoter_END)
                            )
                            promoter_GENE = chr_promoter_ranges_gene_dict[
                                CHROM
                            ][promoter_RANGE]
                            promoter_OUTPUT = promoter_GENE + ':' + MESSAGE
                            OUTPUT_set.append(promoter_OUTPUT)
                            match_promoter += 1

                    if OUTPUT_set:
                        OUTPUT = ','.join(OUTPUT_set)
                        match_line += 1
                        fields = [CHROM, str(POS), ID, REF, ALT, OUTPUT]
                        out_line = '\t'.join(fields) + '\n'
                        outfile.write(out_line)


if __name__ == '__main__':
    import sys

    try:
        input_filename = sys.argv[1]
    except IndexError:
        sys.exit('Supply input-file [output-file] [promoter_database]')

    mapping = {2: 'outfile', 3: 'promoterdb'}
    kwargs = {}
    for i, v in mapping.items():
        try:
            kwargs[v] = sys.argv[i]
        except IndexError:
            kwargs[v] = None

    annotate_effective_promoters(input_filename, **kwargs)
