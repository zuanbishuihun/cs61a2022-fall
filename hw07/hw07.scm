(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cdr (cdr s))))

(define (ascending? asc-lst)  (cond ((or (null? asc-lst) (null? (cdr asc-lst))) #t)
                                    ((> (car asc-lst) (cadr asc-lst)) #f)
                                    (else (ascending? (cdr asc-lst)))))

(define (square n) (* n n))

; 注意不能超过时间限制，根据提示进行递归的优化处理，分为奇数和偶数两种情况
(define (pow base exp) (cond ((= exp 0) 1)
                             ((= exp 1) base)
                             ((even? exp) (square (pow base (/ exp 2))))
                             (else (* base (pow base (- exp 1))))))
