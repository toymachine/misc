(ns org.pork.core
    (:refer-clojure :rename {map cljmap}))

(defn hello []
    (println "Hello WOrld!"))

(defn map [f l]
    (cljmap l f))
