import os
import pickle
import pandas as pd
from bs4 import BeautifulSoup


def txt_io(file, action='r', write_lines=None):

    if action == 'r':
        with open(file, action) as f:
            lines = f.read().splitlines()
        return lines

    elif action == 'w':
        with open(file, action) as f:
            for line in write_lines:
                f.write(line.strip() + '\n')
    else:
        print(f"Action {action} not supported")


def excel_io(file, action='r', write_df=None, columns=["source", "target"]):

    if action == 'r':
        df = pd.read_excel(file)
        return df

    elif action == 'w':
        df = pd.DataFrame(write_df, columns=columns)
        df.to_excel(file, header=True, index=None)

    else:
        print(f"Action {action} not supported")


def save_terms_as_pickle(data, pickle_dir):
    """Serialize data into pickle file."""
    print("Saving terms to pickle file...")
    try:
        file = open(pickle_dir, 'wb')
        pickle.dump(data, file)
        file.close()
    except:
        raise Exception("Failed to save terms in pickle.")
    print("Terms saved.")


def loads_terms_from_pickle(pickle_dir):
    """Load serialized data from pickle file."""
    print("Loading terms from pickle file...")
    try:
        file = open(pickle_dir, 'rb')
        data = pickle.load(file)
        file.close()
    except:
        raise Exception("Failed to load terms from pickle.")
    print("Terms loaded.")

    return data


def writeToTmxFile(outputPath, pairs, srcLang, tgtLang, segType='seg', encoding='utf8'):
    """Write to TMX (XML) file

       Args:
          outputPath (str): The path of the TMX file
          pairs (list): a list of (source_text, target_text) tuples
          segType (str): segment type, e.g., 'phrase'
          srcLang (str): source language code
          tgtLang (str): target language code
          encoding (str): the encoding method
    """

    try:
        soup = BeautifulSoup(features='xml')
        soup.append(soup.new_tag('tmx', version='1.4b'))

        # Write header
        header = soup.new_tag('header')
        header['creationtool'] = 'YappnTmxGenerator'
        header['creationtoolversion'] = '1.0.0.1905'
        header['o-tmf'] = 'TMX'
        header['adminlang'] = 'en'
        header['datatype'] = 'plaintext'
        header['segtype'] = segType
        header['srclang'] = srcLang
        tmx_tuTag = 'tu'
        tmx_tuPieceTag = 'tuv'
        tmx_textTag = 'seg'
        soup.tmx.append(header)

        # Write body
        soup.tmx.append(soup.new_tag('body'))

        for (src, tgt) in pairs:
            tu = soup.new_tag(tmx_tuTag)

            tuvSrc = soup.new_tag(tmx_tuPieceTag)
            tuvSrc['xml:lang'] = srcLang
            seg = soup.new_tag(tmx_textTag)
            seg.string = src
            tuvSrc.append(seg)

            tuvTgt = soup.new_tag(tmx_tuPieceTag)
            tuvTgt['xml:lang'] = tgtLang
            seg = soup.new_tag(tmx_textTag)
            seg.string = tgt
            tuvTgt.append(seg)

            tu.append(tuvSrc)
            tu.append(tuvTgt)

            soup.tmx.body.append(tu)

        with open(outputPath, 'wb') as f:
            f.write(soup.prettify().encode(encoding))

        return True

    except:

        return False


