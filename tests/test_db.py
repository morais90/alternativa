import flaskr.db as db

def test_get_db_session_create_tables(capsys):
	session = db.get_db_session(True)
	print(capsys)
