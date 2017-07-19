#lang racket
(require racket/gui/base racket/date db)

(define version "0.4.2")

(define debug #t)
(define db #f)
(define interval 60)


(if debug
    (begin
          (set! db (sqlite3-connect #:database "rollbook.db"))
          (set! debug #t)
          (display "debug mode, sqlite3."))
    (begin
      (set! db (mysql-connect #:user (getenv "USER")
                              #:password (getenv "PASSWORD")
                              #:database (getenv "DATABASE")
                              #:server (getenv "SERVER")))))

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

(define attend?
  (λ (user date hour)
    (let ((answers
           (query-rows
            db
            "select * from rollbook
where user=? and date =? and hour =?" user date hour)))
      (not (null? answers)))))

(define attend!
  (λ (user date hour message)
    (query-exec
       db
       "insert into rollbook (user, date, hour, message) values (?, ?, ?, ?)"
       user date hour message)))

(define frame
  (new frame% [label (string-append "roolbook " version)]))

(define vp (new vertical-pane% [parent frame]))

(define text-field (new text-field% [parent vp]
                        [label ""]
                        [min-width 400]
                        [min-height 50]))

(define too-short?
  (λ (m)
    (< (string-length m) 10)))

(define button
  (new button% [parent vp]
     [label "on"]
     [callback
      (λ (btn evt)
        (let ((message (send text-field get-value)))
          (if (too-short? message)
              (dialog
               "メッセージが短すぎ。
出席は記録されません。
もっと具体的なメッセージを。")
              (begin
                (attend! (get-user) (get-date) (get-hour) message)
                (dialog "記録しました。")
                (send text-field set-value "")
                (send frame iconize #t)))))]))

(define last-hour 0)
(define thd #f)
(define start
  (λ (sec)
    (set! thd
          (thread
           (λ ()
             (let loop ()
               (unless (= last-hour (get-hour))
                       (send frame show #t)
                       (set! last-hour (get-hour)))
               (sleep sec)
               (loop)))))))

(define stop
  (λ ()
    (kill-thread thd)))

;;
;; main starts here
;;
(start interval)
(sleep 3)
