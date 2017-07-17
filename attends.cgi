#!/usr/local/bin/ruby
# coding: utf-8
require 'sequel'
require 'cgi'

VERSION = "0.3"

print <<EOH
content-type: text/html

<head>
<meta charset="utf-8">
<link rel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
crossorigin="anonymous">
<style>
input.s {width: 2em; text-align: center;}
input.assess {width: 2em; text-align: center;}
.error {color: red; }
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
    puts "<h3>Browse</h3>"
    puts "<div class='form-inline'>"
    users_all().each do |user|
    print <<EOF1
<div class="form-group">
<form method="post">
<input type="hidden" name="cmd" value="show">
<input class="btn btn-primary" type="submit" name="user" value="#{user}">
</form>
</div>
EOF1
    end
    puts "</div>"

    puts "<h3>Create empty entry</h3>"
    now = Time.now
    m = now.month
    d = now.day
    print <<EOF4
<div class="form-inline">
<form method="post">
<input type="hidden" name="cmd" value="all-zero">
<p>
<input class="s" name="month" value="#{m}">月
<input class="s" name="day" value="#{d}">日
<input type="submit" value="create" class="btn btn-danger"></p>
</form>
</div>
EOF4
  print <<EOF5
<h3>Download client</h3>
<p>macOS only.</p>
<ul>
<li><a href="bin/6.9/attend">for Racket 6.9 users</a></li>
<li><a href="bin/6.8/attend">for Racket 6.8 users</a></li>
</ul>
EOF5
  end

  def all_zero(month, day)
    users_all.each do |user|
      DB[:rollbook].insert(user: user, date: "#{month}/#{day}", hour: 0, message: "fake")
    end
  end

  def assess(user,date)
    row = DB[:assess].where(user: user, date:date).first
    row[:assess]
  rescue
    ' '
  end

  def upsert_assess(user, date, assess)
    assess = assess.strip
    if (DB[:assess].where(user: user, date: date).first)
      DB[:assess].where(user: user, date: date).update(assess: assess)
      puts "updated<br>"
    else
      DB[:assess].insert(user: user, date: date, assess: assess)
      puts "inserted<br>"
    end
    puts "<p><a href='/'>back</a></p>"
  end

  def show(user)
    if user.empty?
      puts "<p class='error'>ユーザを選んでください。</p>"
      return
    end
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
      unless attends[date].nil?
        puts "<tr><th>#{date}</th>"
        (1..5).each do |hour|
          puts "<td>#{mark(attends[date][hour])}</td>"
        end
        print <<EOF
<td>
<form method="post">
<input type="hidden" name="cmd" value="assess">
<input type="hidden" name="user" value="#{user}">
<input type="hidden" name="date" value="#{date}">
<input class="assess" name="assess" value="#{assess(user,date)}">
</form>
</td>
EOF
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
  elsif cgi['cmd'] =~ /assess/
    upsert_assess(cgi['user'], cgi['date'], cgi['assess'])
  else
    index()
  end

rescue
  puts "<p style='color: red;'>#{$!}</p>"

ensure
  print <<EOF
<hr>
hkimura, version #{VERSION}.
</div>
</body>
</html>
EOF
end
