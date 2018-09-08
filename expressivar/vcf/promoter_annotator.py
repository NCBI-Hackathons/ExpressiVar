import csv

from expressivar.db import DEFAULT_PROMOTER_DB
from expressivar.dec import file_or_path
import vcf


def annotate_effective_promoters(infile, outfile=None, promoterdb=None):
    if promoterdb is None:
        promoterdb = DEFAULT_PROMOTER_DB

    if outfile is None:
        outfile = infile + '.promoter.ann'

    return _annotate_effective_promoters(infile, outfile, promoterdb)


# TODO(zeroslack): ensure infile.newline == ''
@file_or_path(infile='r', outfile='w', promoterdb='r')
def _annotate_effective_promoters(infile, outfile, promoterdb):
    csv_dialect = 'excel-tab'
    preader = csv.reader(promoterdb, dialect=csv_dialect)
    output = csv.writer(outfile, dialect=csv_dialect)
    chr_promoter_ranges_dict = dict()
    chr_promoter_ranges_gene_dict = dict()
    for promoter in preader:
        # TODO(zeroslack): what is format of this file??
        CHROM, START, END, STRAND, GENE  = promoter
        RANGE = (int(START), int(END))

        if CHROM not in chr_promoter_ranges_dict:
            chr_promoter_ranges_dict[CHROM] = []
            chr_promoter_ranges_dict[CHROM].append(RANGE)
            chr_promoter_ranges_gene_dict[CHROM] = dict()
            chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE
        else:
            chr_promoter_ranges_dict[CHROM].append(RANGE)
            chr_promoter_ranges_gene_dict[CHROM][RANGE] = GENE

    vreader = vcf.Reader(infile)

    def _alt_to_str(x):
        return str(x) if x else ''

    for record in vreader:
        CHROM = record.CHROM
        POS = record.POS
        ID = record.ID or '.'
        REF = record.REF
        ALT = ''.join(map(_alt_to_str, record.ALT))
        START = POS
        END = POS + len(REF) - 1
        # FIXME
        if not CHROM.startswith('chr'):
            CHROM = 'chr' + CHROM

            OUTPUT_set = []
            if CHROM in chr_promoter_ranges_dict:
                for pstart, pend in chr_promoter_ranges_dict[CHROM]:
                    MESSAGE = ''
                    if START <= pstart and END >= pend:
                        MESSAGE = 'complete_hit'
                    elif START >= pstart and END <= pend:
                        MESSAGE = 'internal_hit'
                    elif (
                        pstart <= START <= pend
                    ) and END > pend:
                        MESSAGE = 'down_hit'
                    elif START < pstart and (
                        pstart <= END <= pend
                    ):
                        MESSAGE = 'up_hit'

                    if MESSAGE != '':
                        range_ = (pstart, pend)
                        promoter_GENE = chr_promoter_ranges_gene_dict[
                            CHROM
                        ][range_]
                        promoter_OUTPUT = promoter_GENE + ':' + MESSAGE
                        OUTPUT_set.append(promoter_OUTPUT)

                if OUTPUT_set:
                    OUTPUT = ','.join(OUTPUT_set)
                    fields = [CHROM, str(POS), ID, REF, ALT, OUTPUT]
                    output.writerow(fields)


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
