(define-macro
 (if-macro condition if-true if-false)
  `(if ,condition
    (eval ,if-true)
    (eval ,if-false)))
  
(define-macro (or-macro expr1 expr2)
  `(let ((v1 ,expr1))
     (if v1
         v1
         ,(eval 'expr2))))

(define (replicate x n) 
  (if (= n 0)
      nil
      (cons x (replicate x (- n 1))))) 

(define-macro (repeat-n expr n)
  `(replicate ',expr ,n))    ; 原本我想的是`(replicate ,expr ,n))这样是错误的。。。要把expr变出来一个就行

(define
 (list-of map-expr for var in lst if filter-expr)
  '(map (lambda (var) map-expr)
       (filter (lambda (var) filter-expr) lst)))


(define-macro (list-of-macro map-expr for var in lst if filter-expr)
   `(map (lambda (,var) ,map-expr)
       (filter (lambda (,var) ,filter-expr) ,lst)))