(ns mcro.core
  (:use [clojure.pprint]))

(deftype V3 [^double x ^double y ^double z])

(declare expand)

(defn- expand-v3+ [a b]
  (let [ae (expand a)
        be (expand b)]
    [`(double (+ ~(nth ae 0) ~(nth be 0)))
     `(double (+ ~(nth ae 1) ~(nth be 1)))
     `(double (+ ~(nth ae 2) ~(nth be 2)))]))

(defn- expand-v3* [[s a]]
  (let [ae (expand a)]
    [`(double (* ~s ~(nth ae 0)))
     `(double (* ~s ~(nth ae 1)))
     `(double (* ~s ~(nth ae 2)))]))

(defn- expand [x]
  (let [[op & args] x]
    (case op
      v3* (expand-v3* args)
      v3+ (apply expand-v3+ args)
      v3 args)))

(defmacro minline-v3 [m]
  (let [[x y z] (expand m)]
    `(V3. ~x ~y ~z)))

(defn v3-str [a]
  (str "[" (.x a) " " (.y a) " " (.z a) "]"))

(defn testx []
  (minline-v3 (v3* 5.0 (v3+ (v3 0.1 0.2 0.3) (v3 1.1 1.2 1.3)))))

                                        ;(pprint (v3-str (testx)))
(println (macroexpand '(minline-v3 (v3+ (v3 0.1 0.2 0.3) (v3 1.1 1.2 1.3)))))

