#lang racket
(require racket/gui/base racket/date db)

(define DEBUG #t)

(define db #f)

(if DEBUG
    (set!
     db
     (sqlite3-connect #:database "rollbook.db"))
    (set!
     db
     (mysql-connect #:user "user"
                    #:password "pass"
                    #:database "db"
                    #:server "vm2017.local")))

;;can not use DATABASE CURRENT_TIMESTAMP. is it JST?
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
  (new dialog% [label "error"][style '(close-button)]))

(new message% [parent dialog]
     [label "it's not a working time."])

(define attend?
  (λ (user date hour)
    (let ((answers
           (query-rows
            db
            "select * from rollbook
where user=? and date =? and hour =?" user date hour)))
      (not (null? answers)))))

;;debug mode?
(define attend!
  (λ (user date hour message)
    (cond
     ((and (not DEBUG) (zero? hour)) (send dialog show #t)) ;;dialog1
     ((and (not DEBUG) (attend? user date hour)) (send dialog show #t)) ;;dialog2
     (else (query-exec
            db
            "insert into rollbook (user, date, hour, message) values (?, ?, ?, ?)"
            user date hour message)))))

(define frame (new frame% [label "roolbook"]))

(define vp (new vertical-pane% [parent frame]))
  
(define text-field (new text-field% [parent vp]
                        [label ""]
                        [min-width 400]
                        [min-height 50]))
  
(new button% [parent vp]
     [label "on"]
     [callback
      (λ (btn evt)
        (attend! (get-user) (get-date) (get-hour) (get-message)))])

(define start
  (λ ()
    (send frame show #t)))
    
