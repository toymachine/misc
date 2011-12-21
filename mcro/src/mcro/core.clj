(ns mcro.core
  (:use [clojure.pprint]))

(deftype V3 [x y z])

(defn expand [x]
  (let [[op & args] x]
    (case op
      v3* (let [[s a] args
                ae (expand a)]
            [`(double (* ~s ~(nth ae 0)))
             `(double (* ~s ~(nth ae 1)))
             `(double (* ~s ~(nth ae 2)))])
      v3+ (let [[a b] args
                ae (expand a)
                be (expand b)]
            [`(double (+ ~(nth ae 0) ~(nth be 0)))
             `(double (+ ~(nth ae 1) ~(nth be 1)))
             `(double (+ ~(nth ae 2) ~(nth be 2)))])
      v3 args
      op)))

(defmacro minline-v3 [m]
  (let [[x y z] (expand m)]
    `(V3. ~x ~y ~z)))

(defn v3-str [a]
  (str "[" (.x a) " " (.y a) " " (.z a) "]"))

(defn testx []
  (minline-v3 (v3* 5.0 (v3+ (v3 0.1 0.2 0.3) (v3 1.1 1.2 1.3)))))

(pprint (v3-str (testx)))

