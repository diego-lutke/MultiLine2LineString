from tqdm import tqdm
from shapely import wkt
from MultiLine2Line import Multi2Line
import pandas as pd


if __name__ == '__main__':
    print("Transforming MultiLineStrings to LineStrings...")

    # specify your csv file in here
    df = pd.read_csv('file.csv', delimiter=';')
    df['lines'] = ""

    for i, row in tqdm(df.iterrows()):
        transformer = Multi2Line(5)
        multiline = wkt.loads(row['wkt']) # pyright: ignore

        if multiline.geom_type == 'MultiLineString':
            line = transformer.run(multiline)
            if len(line) == 1:
                df.loc[i, 'lines'] = line[0]
            else:
                df.loc[i, 'lines'] = row['wkt']
        else:
            df.loc[i, 'lines'] = row['wkt']

    # specify the name of the output file in here
    df.to_csv('file_converted.csv', sep=";")
    print(f"Finished")

