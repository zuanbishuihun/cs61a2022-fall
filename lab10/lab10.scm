(define (over-or-under num1 num2) 
    (cond ((< num1 num2) (- 1))
          ((= num1 num2) 0)
          ((> num1 num2) 1)))

(define (make-adder num) (lambda (inc) (+ num inc)))

(define (composed f g) (lambda (x) (f (g x))))

(define lst (cons (cons 1 nil) (cons 2 (cons (list 3 4) (cons 5 nil)))))

# 这个不是自己想出来的，在scheme中没有遍历这个说法，那么一切需要循环的都要改成递归
(define (duplicate lst)  
    (if (null? lst) nil
        (cons (car lst) (cons (car lst) (duplicate (cdr lst))))))
