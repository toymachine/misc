(ns org.pork.core
    (:refer-clojure :rename {map cljmap})
)

(require 'clojure.string)

(defn hello []
    (println "Hello WOrld!"))

(defn map [f l]
    (cljmap l f))

(defn split [s c]
    (clojure.string/split s (re-pattern c)))

(defn enumerate [s]
  (cljmap vector (range) s))

(defn dict [s]
    (into {} s))

(defn sorted_by [s keyfn]
    (sort-by keyfn s))

(defn sorted [s]
    (sort s))

(defn items [m] 
    (cljmap (fn [x y] (vector x y)) (keys m) (vals m)))
