DB = rollbook.db

all:
	@echo make create  -- define database
	@echo make drop    -- drop table
	@echo make exe     -- create standalone app, attend
	@echo make app     -- create attend.app
	@echo make server  -- start local web server
	@echo make clean   -- read as is.
	@echo install      -- install attends.cgi

install:
	install -m 0700 attends.cgi server /srv/rollbook
	sed -i.bak 's|/usr/local/bin/ruby|/usr/bin/env ruby|' /srv/rollbook/attends.cgi
	ln -sf /srv/rollbook/attends.cgi /srv/rollbook/index.cgi

server:
	./server --root . --port 3000

clean:
	${RM} attend test-thread
	${RM} -r *.app
	${RM} *.bak

# develop only
create:
	sqlite3 ${DB} < create.sql

drop:
	sqlite3 ${DB} < drop.sql

exe:
	raco exe attend.rkt

# does not work
app:
	raco exe --gui attend.rkt

