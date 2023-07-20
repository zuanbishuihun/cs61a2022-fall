(define (my-filter pred s) 
  (if (null? s) nil 
    (if (pred (car s)) (cons (car s) (my-filter pred (cdr s)))
      (my-filter pred (cdr s)))))

(define (interleave lst1 lst2) 
  (cond 
        ((null? lst1) lst2)
        ((null? lst2) lst1)
        (else (cons (car lst1) (cons (car lst2) (interleave (cdr lst1) (cdr lst2)))))))

(define (accumulate joiner start n term)
  (if (= n 0) start
    (joiner (term n) (accumulate joiner start (- n 1) term))))

; 需要用到之前的my-filter函数和一个辅助的lambda函数
; 每次传入一个数字后，将其后的数字通过filter排除与其相同的
(define (no-repeats lst) 
  (if (null? lst) nil
    (cons (car lst) (no-repeats (my-filter (lambda (x) (not (= x (car lst)))) (cdr lst))))))
