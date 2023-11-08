from pysondb import db

dbase = db.getDb("local_db/tests.json")

# # add data to db
# dbase.add({"query":"FDX1 is directly targeted by Elesclomol",
#            "sol": "Mitochondrial metabolism promotes adaptation to proteotoxic stress",
#            "year": 2019})

# dbase.add({"query":"Ferroptosis and Apoptosis are interconnected",
#            "sol": "BAX-dependent mitochondrial pathway mediates the crosstalk between ferroptosis and apoptosis",
#            "year": 2020})

# dbase.add({"query":"Copper inhibits FDX1-mediated protein lipoylation",
#            "sol": "Copper induces cell death by targeting lipoylated TCA cycle proteins",
#            "year": 2022})

# # get all items
# dbase.getAll()

# # get items (1 default)
# print(dbase.get())

# # query data
# print(dbase.getBy({"name":"prototype0"}))