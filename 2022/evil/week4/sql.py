import sqlite3


with sqlite3.connect("img.db") as con:
    print(con.execute("SELECT 1 + 2").fetchall())

with sqlite3.connect("img.db") as con:
    con.execute("CREATE TABLE IF NOT EXISTS accounts (account_number INTEGER, amount DECIMAL, PRIMARY KEY(account_number))")
    try: 
        print(con.execute("INSERT INTO accounts (account_number, amount) values (12334, 1.50)").fetchall())
    except:
        pass
    print(con.execute("SELECT * FROM accounts").fetchall())



with sqlite3.connect("img.db") as con:
    con.execute("CREATE TABLE IF NOT EXISTS accounts (account_number INTEGER, amount DECIMAL, PRIMARY KEY(account_number))")
    print(con.execute("UPDATE accounts SET amount = amount + 10 WHERE account_number = 12334").fetchall())
    print(con.execute("SELECT * FROM accounts").fetchall())

import pandas as pd 
 
with sqlite3.connect("img.db") as con:
    df = pd.read_sql_query('SELECT * FROM accounts',con)
    print(df)
    print(df.keys())
    print(sum(df["amount"]))


dataset = pd.read_csv("tbs-pssd-compendium-salary-disclosed-2021-en-utf-8-2022-03-25.csv")
print(dataset.head(5))
print(dataset.shape)
print(dataset.keys())
dataset["total"] = dataset['Salary'].astype(float) + dataset['Benefits'].astype(float)

print(dataset.keys())
print(dataset.head(5))
pd.options.display.float_format = '${:,.2f}'.format

print(dataset.head(5))
import numpy as np
salarypertitle = dataset.groupby("Job Title").agg({'total':[np.size,np.mean]}).reset_index()
salarypertitle = salarypertitle[salarypertitle[("total","size")]>200].sort_values(("total","mean"),ascending=False)
print(salarypertitle.head(10))


salarypertitle = dataset.groupby("Job Title").agg({'total':[np.size,np.max]}).reset_index()
salarypertitle = salarypertitle[salarypertitle[("total","size")]>200].sort_values(("total","amax"),ascending=False)
print(salarypertitle.head(10))


profsalary = dataset[dataset['Job Title'].str.contains("Prof")]
print(profsalary.sort_values("total",ascending=False)[["Last Name", "First Name", "Employer", "total"]].head(10))


genderstat =  pd.read_csv("us-likelihood-of-gender-by-name-in-2014.csv")
print(genderstat[["sex","name"]].head())


datasetwithgender = pd.merge(dataset,genderstat,left_on="First Name", right_on="name")
print(datasetwithgender.head(1000))

print(datasetwithgender.groupby(["sex"]).agg({'total':[np.mean,np.max,np.median]}))


waterlooprof = datasetwithgender[datasetwithgender['Employer'] == "University Of Waterloo"]

print(waterlooprof.head())

print(waterlooprof.groupby(["sex"]).agg({'total':[np.mean,np.max,np.median]}))