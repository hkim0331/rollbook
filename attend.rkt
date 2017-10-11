#lang racket
(require "common.rkt")
(require racket/gui/base racket/date db)

(define version "0.5.8")

(define db #f)

(define *debug* false)

(if *debug*
    (begin
      (display "debug mode, sqlite3.")
      (set! db (sqlite3-connect #:database "rollbook.db")))
    (begin
      (set! db (mysql-connect #:user *user*
                              #:password *password*
                              #:database *database*
                              #:server *server*))))

(define get-date
  (λ ()
    (let ((today (current-date)))
      (format "~a/~a" (date-month today) (date-day today)))))

(define to-min
  (λ (h m)
    (+ (* 60 h) m)))

(define between
  (λ (x from to)
    (and (<= from x) (<= x to))))

;; how to debug?
;; 2017-10-11T09:43:21.808+09:00
;; このコードはクライアントではなく、サーバ側にあるべき。
(define get-hour
  (λ ()
    (let* ((now (seconds->date (current-seconds)))
           (h (date-hour now))
           (m (date-minute now))
           (time (to-min h m)))
      (cond
        ((between time (to-min 8 50) (to-min 10 20)) 1)
        ((between time (to-min 10 30) (to-min 12 0)) 2)
        ((between time (to-min 13 00) (to-min 14 30)) 3)
        ((between time (to-min 14 40) (to-min 16 10)) 4)
        ((between time (to-min 16 20) (to-min 17 50)) 5)
        (else 0)))))

(define get-user
  (λ ()
    (getenv "USER")))

(define dialog
  (λ (message)
    (let* ((D (new dialog% [label "rollbook"][style '(close-button)]))
           (M (new message% [parent D][label message])))
      (send D show #t))))

;; 遅刻判定のロジックを入れるならここ。
;; でも1時間に2度クリックとして、2度目は30分過ぎてから。
(define attend!
  (λ (user date hour message)
    (query-exec
     db
     "insert into rollbook (user, date, hour, message, status)
values (?, ?, ?, ?, 2)"
     user date hour message)))

;;sqlite mysql differs. use concat in mysql.
(define update-status!
  (λ (user date hour message)
    (query-exec
     db
     "update rollbook set status=1, message= ?
where user=? and date=? and hour=?" message user date hour)))

(define exists?
  (λ (user date hour)
    (not (null? (query-rows db "select * from rollbook
where user=? and date=? and hour=?" user date hour)))))

(define status-time-message?
  (λ (user date hour)
    (let ((answers
           (query-rows
            db
            "select status, utc, message from rollbook
where user=? and date =? and hour =?" user date hour)))
      (first answers))))

;; MySQL OK? CURRENT_TIMESTAMP-utc?
(define status!
  (λ (user date hour message)
    (let ((result
           (query-maybe-row
            db
            "select status, message, CURRENT_TIMESTAMP - utc from rollbook where user=? and date=? and hour=?" user date hour)))
      (if result
          (let* ((st (vector-ref result 0))
                 (msg (vector-ref result 1))
                 (min (vector-ref result 2)))
            (when (and (= st 2) (or (= 0 min) (< 3600 min))) ; = 0 for sqlite3
              (update-status! user date hour (string-append msg " " message))))
        (attend! user date hour message)))))

;; GUI parts
(define frame
  (new frame% [label (string-append "roolbook " version " " (get-user))]))

(define vp (new vertical-pane% [parent frame]))


(define text-field (new text-field% [parent vp]
                        [label ""]
                        [min-width 300]
                        [min-height 50]))

;(define redmine (new text-field% [parent vp]
;                        [label "redmine ticket#"]))

(define too-short?
  (λ (m)
    (< (string-length m) 10)))

(define redmine?
  (λ (m)
    (regexp-match #rx"#[0-9]" m)))

(define button
  (new button% [parent vp]
     [label "send"]
     [callback
      (λ (btn evt)
        (let ((message (send text-field get-value)))
          (if (not (redmine? message))
              (dialog
               "redmine のチケット番号を # に続いて入力すること。
何回か連続して同じチケット番号だったら、
下らんヤツとして受け付けないようになる。")
              (begin
                (status! (get-user) (get-date) (get-hour) message)
                (dialog "記録しました。")
                (send frame show #f)))))]))


;;
;; main starts here
;;
(send frame show #t)
