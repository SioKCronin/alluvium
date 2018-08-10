import rethinkdb as r

conn = r.connect(host='localhost', port='28015', db='alluvium')
feed = r.table("queries").changes().run(conn)
#new_chat = r.table("chats").insert([ data ]).run(g.db_conn)

for x in feed:
    print(x)
