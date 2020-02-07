import argparse
import json
from pathlib import Path


def main(args):
    indir = Path(args.input)
    outfile = Path(args.output)
    subset_file = Path(args.list)

    subset = set()
    with subset_file.open(mode='r') as f:
        for line in f:
            id, title = line.strip().split(', ', 1)
            subset.add((id, title))

    infiles = indir.glob('**/wiki*')
    outlines = []
    for infile in infiles:
        with infile.open(mode='r') as f:
            for line in f:
                jline = json.loads(line.strip())
                element = (jline['id'], jline['title'])
                if element in subset:
                    print(element)
                    outlines.append(jline)

    with outfile.open(mode='w') as f:
        for jline in outlines:
            print('<doc id="{id}" url="{url}" title="{title}>'.format(
                id=jline['id'], url=jline['url'], title=jline['title']), file=f)
            print(jline['text'], file=f)
            print('</doc>', file=f)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extract subset document from source corpus according to list')
    parser.add_argument('-i', '--input', help='input directory')
    parser.add_argument('-o', '--output', help='output file name')
    parser.add_argument('-l', '--list', help='subset list')

    args = parser.parse_args()

    main(args)

    
