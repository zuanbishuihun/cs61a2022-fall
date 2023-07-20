(define-macro (when condition exprs)
  `(if ,condition
      (begin ,@exprs) ; 这用法都不知道啊。。。
      'okay))

; 真心不会
(define-macro (switch expr cases)
	(cons _________
		(map (_________ (_________) (cons _________ (cdr case)))
    			cases))
)