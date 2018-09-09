from enum import Enum
import csv

from expressivar.db import DEFAULT_PROMOTER_DB
from expressivar.dec import file_or_path
import vcf


class MatchState(Enum):
    UP = 'up_hit'
    DOWN = 'down_hit'
    COMPLETE = 'complete_hit'
    INTERNAL = 'internal_hit'

    def __format__(self, format_spec):
        return self.value.__format__(format_spec)


def annotate_effective_promoters(infile, outfile=None, promoterdb=None):
    if promoterdb is None:
        promoterdb = DEFAULT_PROMOTER_DB

    if outfile is None:
        outfile = infile + '.promoter.ann'

    return _annotate_effective_promoters(infile, outfile, promoterdb)


@file_or_path(
    infile=dict(mode='r', newline=''),
    outfile=dict(mode='w'),
    promoterdb=dict(mode='r'),
    strictparams=True,
)
def _annotate_effective_promoters(infile, outfile, promoterdb):
    csv_dialect = 'excel-tab'
    preader = csv.reader(promoterdb, dialect=csv_dialect)
    output = csv.writer(outfile, dialect=csv_dialect)
    chr_promoter_ranges_dict = dict()
    chr_promoter_ranges_gene_dict = dict()

    def init_caches(key):
        chr_promoter_ranges_dict[key] = []
        chr_promoter_ranges_gene_dict[key] = dict()

    def add_record(chr_, range_, gene):
        chr_promoter_ranges_dict[chr_].append(range_)
        chr_promoter_ranges_gene_dict[chr_][range_] = gene

    for promoter in preader:
        # TODO(zeroslack): what is format of this file??
        chrom, start, end, strand, gene = promoter
        range_ = (int(start), int(end))

        if chrom not in chr_promoter_ranges_dict:
            init_caches(chrom)

        add_record(chrom, range_, gene)

    vreader = vcf.Reader(infile)

    def _alt_to_str(x):
        return str(x) if x else ''

    for record in vreader:
        chrom = record.CHROM
        pos = record.POS
        id_ = record.ID or '.'
        ref = record.REF
        alt = ''.join(map(_alt_to_str, record.ALT))
        start = pos
        end = pos + len(ref) - 1
        # FIXME
        if not chrom.startswith('chr'):
            chrom = 'chr' + chrom

            matches = []
            if chrom in chr_promoter_ranges_dict:
                for pstart, pend in chr_promoter_ranges_dict[chrom]:
                    match_type = None
                    if start <= pstart and end >= pend:
                        match_type = MatchState.COMPLETE
                    elif start >= pstart and end <= pend:
                        match_type = MatchState.INTERNAL
                    elif (pstart <= start <= pend) and end > pend:
                        match_type = MatchState.DOWN
                    elif start < pstart and (pstart <= end <= pend):
                        match_type = MatchState.UP

                    if match_type is not None:
                        range_ = (pstart, pend)
                        promoter_gene = chr_promoter_ranges_gene_dict[chrom][
                            range_
                        ]
                        promoter_output = '{}:{}'.format(
                            promoter_gene, match_type
                        )
                        matches.append(promoter_output)

                if matches:
                    match_list = ','.join(matches)
                    fields = [chrom, str(pos), id_, ref, alt, match_list]
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
