DB = rollbook.db

create:
	sqlite3 ${DB} < create.sql

drop:
	sqlite3 ${DB} < drop.sql

exe:
	raco exe attend.rkt

app:
	raco exe --gui attend.rkt

debug:
	./server --root .

clean:
	${RM} attend
	${RM} -rattend.app

