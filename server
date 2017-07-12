#!/usr/bin/env ruby
# coding: utf-8
# 2006.12.19
# 2007-09-27 changed shell-bang! line from /usr/bin/ruby to /usr/bin/env ruby
# 2011-02-25 chose /opt/local/bin/ruby1.9
# 2012-03-06 changed back again to /usr/bin/env ruby.

require 'webrick'
include WEBrick

def usage()
  print <<EOF
usage:
  server [--port port] [--root documentroot]
EOF
  exit(1)
end

port=2000
root="public"
while (arg=ARGV.shift)
  case arg
  when /--port/
    port=ARGV.shift.to_i
  when /--root/i
    root=ARGV.shift
  else
    usage()
  end
end
s=HTTPServer.new(
	:Port		=> port,
	:DocumentRoot 	=> File.join(Dir.pwd, root)
)
trap("INT") {s.shutdown}
s.start
