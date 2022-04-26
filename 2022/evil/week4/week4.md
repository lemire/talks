---
marp: true
theme: base
title: An evil-genius guide to computer programming
description: The six-week course is a playful guide through programming. If you have never programmed before, this course should motivate you to go further. If you are an experienced programmer, this course might help you get excited again. In this course, I will explain how programming can make you smarter. I will show how programming allows you to automate web access and find hidden treasures. I will show how programming can make you more creative and help you change the world.
paginate: true
_paginate: false
---


## <!--fit--> An evil-genius guide to computer programming



Daniel Lemire 
Montreal :canada: 

blog: https://lemire.me 
twitter: [@lemire](https://twitter.com/lemire)
GitHub: [https://github.com/lemire/](https://github.com/lemire/)



---
# Passing values to templates in flask

https://replit.com/@lemire/LikelyBisqueServices#main.py

---

- main.py
- images/static/football.jpog
- templates/base.html
- templates/final.html
- templates/leagus.html


---

```Python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  pic1 = "static/images/football.jpg"
  return render_template("base.html", user_image=pic1)

app.run(host='0.0.0.0', port=8080)

```


---
```html
<body>

<h3>What's Your Name?</h3>
  
<p>  <a href="daniel">maybe it is daniel?</a></p>

<img src="{{ user_image }}" height="500px" width="500px">

</body>
</html>
```


---


```Python
@app.route('/<name>')
def name_output(name):
	pic1 = "static/images/football.jpg"
	return  render_template("leagus.html", user_image=pic1, username = name)
```
---
```html
<html>
<body>
<p>Hello  {{username}}. Which football league do you support?</p>
<p>Maybe it is <a href="league/dong">dong</a>?</p>

  <img src="/{{ user_image }}" height="750px" width="750px">

</body>
</html>
````

---


```Python
@app.route('/league/<League>')
def league_inquiry(League):
  pic1 = "static/images/football.jpg
  return render_template("final.html", user_image=pic1, league = League)
```



---
```html
<html>
<body>
    <h2>{{ league }}</h2>

    <img src="/{{ user_image }}" height="750px" width="750px">

</body>
</html>
```

---
# Week 4

Dig For Treasure

---

```Python
import sqlite3

with sqlite3.connect("img.db") as con:
    print(con.execute("SELECT 1 + 2").fetchall())
```

will print `3`

---

```Python
with sqlite3.connect("img.db") as con:
    con.execute("CREATE TABLE IF NOT EXISTS accounts (account_number INTEGER, amount DECIMAL, PRIMARY KEY(account_number))")
    try: 
        print(con.execute("INSERT INTO accounts (account_number, amount) values (12334, 1.50)").fetchall())
    except:
        pass
    print(con.execute("SELECT * FROM accounts").fetchall())
```

Prints `[(12334, 1.5)]`

---

```Python
with sqlite3.connect("img.db") as con:
    con.execute("CREATE TABLE IF NOT EXISTS accounts (account_number INTEGER, amount DECIMAL, PRIMARY KEY(account_number))")
    print(con.execute("UPDATE accounts SET amount = amount + 10 WHERE account_number = 12334").fetchall())
    print(con.execute("SELECT * FROM accounts").fetchall())
```

Prints `[(12334, 11.5)]`


---

```Python
import pandas as pd 
 
with sqlite3.connect("img.db") as con:
    df = pd.read_sql_query('SELECT * FROM accounts',con)
    print(df)
    print(df.keys())
    print(sum(df["amount"]))
```

Prints `11.5`

---


```Python
dataset = pd.read_csv("tbs-pssd-compendium-salary-disclosed-2021-en-utf-8-2022-03-25.csv")
print(dataset.head(5))
```
---

```
     Sector Last Name First Name     Salary  Benefits                                           Employer                                       Job Title  Year  _docID
0  Colleges     Aarts      Cheri  115618.46     74.25    Fanshawe College Of Applied Arts and Technology                                       Professor  2021       0
1  Colleges   Aaslepp       Drew  114506.79    124.66  Humber College Institute Of Technology and Adv...                                       Professor  2021       1
2  Colleges      Abba    Corinne  106770.74    124.45  George Brown College Of Applied Arts and Techn...                                       Librarian  2021       2
3  Colleges    Abbott      Brian  107378.44    124.61  Conestoga College Institute Of Technology and ...                                       Professor  2021       3
4  Colleges    Abbott   Kathleen  162873.26    428.40  George Brown College Of Applied Arts and Techn...  Associate Dean, Centre for Continuous Learning  2021       4
```
---

```Python
print(dataset.shape)
```
(244390, 9)

---
```Python
print(dataset.keys())
```

```
Index(['Sector', 'Last Name', 'First Name', 'Salary', 'Benefits', 'Employer',
       'Job Title', 'Year', '_docID'],
      dtype='object')
```

---


```Python
dataset["total"] = dataset['Salary'].astype(float) + dataset['Benefits'].astype(float)
print(dataset.head(5))
```
---

```
     Sector Last Name First Name     Salary  ...                                       Job Title  Year _docID      total
0  Colleges     Aarts      Cheri  115618.46  ...                                       Professor  2021      0  115692.71
1  Colleges   Aaslepp       Drew  114506.79  ...                                       Professor  2021      1  114631.45
2  Colleges      Abba    Corinne  106770.74  ...                                       Librarian  2021      2  106895.19
3  Colleges    Abbott      Brian  107378.44  ...                                       Professor  2021      3  107503.05
4  Colleges    Abbott   Kathleen  162873.26  ...  Associate Dean, Centre for Continuous Learning  2021      4  163301.66
```
---


```Python
pd.options.display.float_format = '${:,.2f}'.format
print(dataset.head(5))
```
---
```Python
     Sector Last Name First Name      Salary  ...                                       Job Title  Year _docID       total
0  Colleges     Aarts      Cheri $115,618.46  ...                                       Professor  2021      0 $115,692.71
1  Colleges   Aaslepp       Drew $114,506.79  ...                                       Professor  2021      1 $114,631.45
2  Colleges      Abba    Corinne $106,770.74  ...                                       Librarian  2021      2 $106,895.19
3  Colleges    Abbott      Brian $107,378.44  ...                                       Professor  2021      3 $107,503.05
4  Colleges    Abbott   Kathleen $162,873.26  ...  Associate Dean, Centre for Continuous Learning  2021      4 $163,301.66
```
---


```Python
import numpy as np
salarypertitle = dataset.groupby("Job Title").agg({'total':[np.size,np.mean]})
```

---

```
                       total            
                        size        mean
Job Title                               
1st Class Constable       43 $113,120.93
1st Class Engineer         1 $104,608.40
1st Class Fire Fighter   120 $115,750.01
1st Class Firefighter    167 $116,845.78
2nd Class Constable        1 $104,615.46
```

---

```
largecount = salarypertitle[salarypertitle[("total","size")]>200]
```

---
``` 
                                      total            
                                       size        mean
Job Title                                              
Advanced Care Paramedic                 790 $114,485.29
Assistant Crown Attorney                814 $184,286.98
Assistant Curriculum Leader Secondary   880 $108,051.92
Assistant Professor                    1652 $129,952.33
Associate Professor                    3252 $158,353.72
````

---

```Python
largecount.sort_values(("total","mean"),ascending=False)
```

---

```
                                         total            
                                          size        mean
Job Title                                                 
Judge                                      347 $307,699.57
Physician                                  322 $212,869.29
Counsel                                    623 $190,756.19
Chief Administrative Officer               276 $186,512.74
```

---

```
salarypertitle = dataset.groupby("Job Title").agg({'total':[np.size,np.mean]})
salarypertitle = salarypertitle[salarypertitle[("total","size")]>200].sort_values(("total","mean"),ascending=False)
print(salarypertitle.head(10))
```

```
---


```Python
salarypertitle = dataset.groupby("Job Title").agg({'total':[np.size,np.max]})
salarypertitle = salarypertitle[salarypertitle[("total","size")]>200].sort_values(("total","amax"),ascending=False)
print(salarypertitle.head(10))
```
---

```
                             total            
                              size        amax
Job Title                                     
Chief Executive Officer        324 $654,613.06
Associate Professor           3252 $623,459.23
Professor                     7761 $522,836.98
Director                       585 $513,101.52
Physician                      322 $443,749.84
Chief Administrative Officer   276 $413,910.21
Judge                          347 $378,378.95
Lecturer                       285 $342,357.20
Faculty                        565 $338,497.96
Operator                       766 $324,161.05
```

---


```Python
profsalary = dataset[dataset['Job Title'].str.contains("Prof")]
print(profsalary.sort_values("total",ascending=False)[["Last Name", "First Name", "Employer", "total"]].head(10))
```

---

```
       Last Name    First Name                       Employer       total
227267   Emerson       Claudia            McMaster University $623,459.23
235490  Mitchell       William          University Of Toronto $564,065.02
228799    Golden         Brian          University Of Toronto $549,803.80
243963       Yoo          John  University Of Western Ontario $542,466.59
225824     Dacin          Tina             Queen’s University $541,461.96
226617    Doidge  Craig Andrew          University Of Toronto $540,645.34
238535   Reznick       Richard             Queen’s University $522,836.98
237592  Philpott          Jane             Queen’s University $508,008.62
228517   Gertler         Meric          University Of Toronto $497,751.20
233084    Lenton    Rhonda, L.                York University $494,683.14
```

---

```Python
genderstat =  pd.read_csv("us-likelihood-of-gender-by-name-in-2014.csv")
print(genderstat[["sex","name"]].head())
```

---

```
  sex     name
0   F   Elaine
1   F    Cathy
2   F    Heidi
3   F    Vicki
4   F  Melinda
````

---


```Python
datasetwithgender = pd.merge(dataset,genderstat,left_on="First Name", right_on="name")
print(datasetwithgender.groupby(["sex"]).agg({'total':[np.mean,np.max,np.median]}))
```

---

```
          total                          
           mean          amax      median
sex                                      
F   $118,530.40 $1,527,441.40 $107,026.77
M   $129,955.95 $1,635,785.84 $117,675.63
```

---


```Python
waterlooprof = datasetwithgender[datasetwithgender['Employer'] == "University Of Waterloo"]
print(waterlooprof.groupby(["sex"]).agg({'total':[np.mean,np.max,np.median]}))
```

---

```
          total                        
           mean        amax      median
sex                                    
F   $148,057.31 $340,825.95 $135,983.78
M   $160,769.90 $343,058.80 $154,489.34
```

---

https://replit.com/@lemire/ProperMagentaCosmos#main.py

---
# Homework

Use pandas to do some analysis.
