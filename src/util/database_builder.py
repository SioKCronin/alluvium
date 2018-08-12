import rethinkdb as r

conn = r.connect(host="10.0.0.11")
r.db_create('alluvium').run(conn)
r.db('alluvium').table_create('queries').run(conn)
r.db('alluvium').table('queries').index_create('query_id').run(conn)

