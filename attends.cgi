#!/usr/local/bin/ruby
# coding: utf-8

require 'sequel'
require 'cgi'
require './common.rb'

VERSION = "0.5.6"
REDMINE = "https://redmine.melt.kyutech.ac.jp"

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
.we { background: lightgray; }
</style>
</head>
<body>
<div class="container">
<h1>Rollbook</h1>
<p>
「出席取ればいいんだろう」か？ やってることはそれでいいの？
</p>
EOH

begin
  DB = if DEBUG
         Sequel.sqlite("rollbook.db")
       else
         Sequel.connect("mysql2://#{USER}:#{PASSWORD}@localhost/admin")
       end

  MARK = %w{ ⚫ ◯ ▲ △ }

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
    print <<BROWSE
<div class="form-group">
<form method="post">
<input type="hidden" name="cmd" value="show">
<input class="btn btn-primary" type="submit" name="user" value="#{user}">
</form>
</div>
BROWSE
    end
    puts "</div>"
    print <<DOWNLOAD
<h3>Download client</h3>
<p>macOS only. 最新は #{VERSION}。</p>
<ul>
<li><a href="bin/6.10.1/attend">for Racket 6.10.1 users</a></li>
<li><a href="bin/6.10/attend">for Racket 6.10 users</a></li>
<li><a href="bin/6.9/attend">for Racket 6.9 users</a></li>
<li><a href="bin/6.8/attend">for Racket 6.8 users</a></li>
</ul>
DOWNLOAD

    puts "<h3>Create empty entries (not for students)</h3>"
    now = Time.now
    m = now.month
    d = now.day
    print <<CREATE
<div class="form-inline">
<form method="post">
<input type="hidden" name="cmd" value="all-zero">
<p>
<input class="s" name="month" value="#{m}">月
<input class="s" name="day" value="#{d}">日
<input type="submit" value="create" class="btn btn-danger"></p>
</form>
</div>
CREATE
  end

  def all_zero(month, day)
    users_all.each do |user|
      DB[:rollbook].insert(user: user, date: "#{month}/#{day}", hour: 0, message: "", status: 0)
    end
  end

  # Timezone of mysql is vm2017's timezone, JST.
  # in sqlite3, UTC.
  def adjust(time)
    time += 9*60*60 if DEBUG
    time.to_s.sub(/ \+0900/,"")
  end

  def redmine_tag(s)
    s.gsub(/#(\d+)/, "<a href='#{REDMINE}/issues/\\1'>#\\1</a>")
  end

  def show_messages(user,date)
    puts "<h3>#{user} on #{date}</h3>"
    DB[:rollbook].where(user: user, date:date).order(:utc).each do |row|
      unless (row[:message].empty? or row[:message] =~ /fake/)
        print <<EOL
<p>
#{row[:hour]} #{adjust(row[:utc])} #{redmine_tag(row[:message])}
</p>
EOL
      end
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

  # FIXME if 2018 comes, no good.
  def weekend?(md)
    m, d = md.split(/\//)
    d = Date.new(2017, m.to_i, d.to_i).wday
    d == 6 || d == 0
  end

  def show(user)
    puts "<h2>#{user} records</h2>"
    stats = Hash.new()
    DB[:rollbook].distinct.select(:date,:hour,:status).
      where(Sequel.lit("user = ?", user)).each do |row|
    if stats.has_key?(row[:date])
        stats[row[:date]][row[:hour]] = row[:status]
      else
        stats[row[:date]] = [0,0,0,0,0,0]
        stats[row[:date]][row[:hour]] = row[:status]
      end
    end

    dates = Array.new
    DB[:rollbook].distinct.select(:date).each do |date|
      dates.push date[:date]
    end

    puts "<table class='table'>"
    puts "<tbody>"
    dates.sort_by{|md| m,d = md.split(/\//);
      -m.to_i*100-d.to_i}.each do |date|
      unless stats[date].nil?
        print <<EOH
<tr class=#{if weekend?(date); "we"; else "wd"; end}>
<th>
<a href='attends.cgi?cmd=date&user=#{user}&date=#{date}'>#{date}</a>
</th>
EOH
        (1..5).each do |hour|
          puts "<td>#{mark(stats[date][hour])}</td>"
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
    puts "<p>go to <a href='attends.cgi'>Rollbook</a>"
    puts "|"
    puts "<a href='https://redmine.melt.kyutech.ac.jp'>redmine</a>"
  end

  #
  # main starts here. dispatch.
  #
  cgi = CGI.new
  if (cgi['cmd'] =~ /show/ and cgi['user'])
    show(cgi['user'])
  elsif cgi['cmd'] =~ /all-zero/
    all_zero(cgi['month'], cgi['day'])
  elsif cgi['cmd'] =~ /assess/
    upsert_assess(cgi['user'], cgi['date'], cgi['assess'])
  elsif cgi['cmd'] =~ /date/
    show_messages(cgi['user'], cgi['date'])
  else
    index()
  end

rescue
  puts "<p style='color: red;'>#{$!}</p>"

ensure
  print <<EOF
<hr>
hkimura, version #{VERSION},
<a href="https://github.com/hkim0331/rollbook.git">
https://github.com/hkim0331/rollbook.git
</a>
</div>
</body>
</html>
EOF
end
