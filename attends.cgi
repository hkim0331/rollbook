#!/usr/local/bin/ruby
require 'sequel'
require 'cgi'

print <<EOH
content-type: text/html

<h1>Rollbook</h1>
EOH

begin
  DB = Sequel.sqlite("rollbook.db")
  cgi = CGI.new

  def users_all()
    ret = []
    DB.fetch("select distinct(user) from rollbook") do |row|
      ret.push row[:user]
    end
    ret
  end

  def index()
    print <<EOF1
<form method="post">
<input type="hidden" name="cmd" value="show">
EOF1
    users_all().each do |user|
      print <<EOF2
<input type="radio" name="user" value="#{user}">#{user}
EOF2
    end
  print <<EOF3
<p><input type="submit" value="check"></p>
</form>
EOF3
  end

  def show(user)
    print <<EOF
<h2>#{user} records</h2>
EOF
    
    DB.fetch("select distinct date, hour from rollbook where user=? order by date, hour", user).each do |row|
      print <<EOD
<p>#{row[:date]}, #{row[:hour]}</p>
EOD
    end
  end

  if (cgi['cmd'] =~/show/ and cgi['user'])
    show(cgi['user'])
  else
    index()
  end

rescue
  puts "<p style='color: red;'>#{$!}</p>"

ensure
  print <<EOF
<hr>
hkimura, using Racket 6.9 and Ruby #{RUBY_VERSION}.
EOF
end


