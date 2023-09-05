import psycopg2
import pandas as pd


db_params = {
    'database': 'DEP',
    'user': 'postgres',
    'password': '',
    'host': 'vichogent.be',
    'port': '40045',
    'options': '-c search_path=dep'
}


df = pd.read_excel('zoektermen_opdracht_sem1_sv.xlsx')
zoektermen = df.stack().tolist()


query = "SELECT * FROM duurzaamheidstabel WHERE "
for zoekterm in zoektermen:
    query += f"to_tsvector('nederlands', tekst) @@ to_tsquery('nederlands', %s) OR "
query = query[:-3]  


with conn.cursor() as cur:
    cur.execute(query, tuple(zoektermen))
    resultaten = cur.fetchall()


scores = {'Environment': 0, 'Social': 0, 'Governance': 0}
domeinen = ['Environment', 'Social', 'Governance']

for resultaat in resultaten:
    tekst = resultaat[1] 
    for domein in domeinen:
        domein_termen = df[domein].dropna().tolist()
        for term in domein_termen:
            if term in tekst:
                scores[domein] += 1


totaalscore = sum(scores.values()) / (len(domeinen) * len(zoektermen))


print(f"Scores per domein: {scores}")
print(f"Totaalscore duurzaamheid: {totaalscore}")


conn.close()
