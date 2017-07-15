#!/usr/local/bin/ruby
# coding: utf-8
require 'sequel'
require 'cgi'

print <<EOH
content-type: text/html

<head>
<meta charset="utf-8">
<link rel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
crossorigin="anonymous">
<style>
input.s {width: 2em;}
</style>
</head>
<body>
<div class="container">
<h1>Rollbook</h1>
EOH

begin
  DB = if true
        Sequel.sqlite("rollbook.db")
       else
	Sequel.connect("mysql2://rollbook:#{ENV['APASS']}@localhost/admin")
       end
  cgi = CGI.new

  MARK = %w{ ⚫  ◯  }
  def mark(n)
    if n.nil?

      ""
    else
      MARK[n]
    end
  end

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
      puts "<p>"
      print <<EOF2
<input type="radio" name="user" value="#{user}">#{user}
EOF2
    end
    puts "</p>"
  print <<EOF3
<p><input type="submit" value="check" class="btn btn-primary"></p>
</form>
EOF3

  now = Time.now
  m = now.month
  d = now.day

  print <<EOF4
<form method="post">
<input type="hidden" name="cmd" value="all-zero">
<p>
<input class="s" name="month" value="#{m}">月
<input class="s" name="day" value="#{d}">日
</p>
<p><input type="submit" value="danger" class="btn btn-danger"></p>
</form>
EOF4
  end

  def all_zero(month, day)
    users_all.each do |user|
      DB[:rollbook].insert(user: user, date: "#{month}/#{day}", hour: 0, message: "fake")
    end
  end

  def show(user)
    puts "<h2>#{user} records</h2>"

    attends = Hash.new()
    DB.fetch("select distinct date, hour from rollbook where user=? order by date, hour", user).each do |row|
      if attends.has_key?(row[:date])
        attends[row[:date]][row[:hour]] = 1
      else
        attends[row[:date]] = [0,0,0,0,0,0]
        attends[row[:date]][row[:hour]] = 1
      end
    end

    dates = Array.new
    DB.fetch("select distinct date from rollbook order by date").each do |date|
      dates.push date[:date]
    end

    puts "<table class='table'>"
    puts "<tbody>"
    dates.each do |date|
      puts "<tr><th>#{date}</th>"
      (1..5).each do |hour|
        puts "<td>#{mark(attends[date][hour])}</td>"
      end
      puts "</tr>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "<p>back to <a href='attends.cgi'>Rollbook</a></p>"
  end

  #
  # main starts here
  #
  if (cgi['cmd'] =~ /show/ and cgi['user'])
    show(cgi['user'])
  elsif cgi['cmd'] =~ /all-zero/
    all_zero(cgi['month'], cgi['day'])
  else
    index()
  end

rescue
  puts "<p style='color: red;'>#{$!}</p>"

ensure
  print <<EOF
<hr>
hkimura, using Racket 6.9 and Ruby #{RUBY_VERSION}.
</div>
</body>
</html>
EOF
end
