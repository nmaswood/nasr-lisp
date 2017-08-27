sample_1 = """(defun sqrt-iter (guess x)
  (if (good-enough-p guess x)
      guess
      (sqrt-iter (improve guess x) x)))"""

sample_2 = """(defun factorial (n)
  (if (= n 1)
      1
      (* n (factorial (- n 1)))))"""
sample_3 = """(def a 10)"""
sample_4 = """(defun addone (x)  (+ x 1))"""

