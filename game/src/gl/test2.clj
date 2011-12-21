(ns gl.test2
  (:use [gl.vector])
  (:require [gl.game :as game])
  (:import
   [java.awt Graphics2D Color]
   [java.util Random]))

(set! *warn-on-reflection* true)

(deftype State [position velocity])

(deftype Derivative [dx dv])


(defn spring [k b]
  ;creates an acceleration function for a spring
  (fn [^State state t]
    (v- (v* (- k) (.position state))
        (v* b (.velocity state)))))

;evaluate/integrate form the RK4 integrator
(defn evaluate ^Derivative [^State initial t dt ^Derivative derivative acceleration]
  (let [state (State. (v+ (.position initial) (v* dt (.dx derivative)))
                      (v+ (.velocity initial) (v* dt (.dv derivative))))]
    (Derivative. (.velocity state) (acceleration state (+ t dt)))))

(defn integrate ^State [^State state ^double t ^double dt acceleration]
  (let [^Derivative a (evaluate state t (double 0) (Derivative. vector-3d-zero vector-3d-zero) acceleration)
        ^Derivative b (evaluate state t (* dt (double 0.5)) a acceleration)
        ^Derivative c (evaluate state t (* dt (double 0.5)) b acceleration)
        ^Derivative d (evaluate state t dt c acceleration)]
    (State. (v+ (.position state) (v* dt (v* 1/6 (v+ (.dx a) (v* 2 (v+ (.dx b) (.dx c))) (.dx d)))))
            (v+ (.velocity state) (v* dt (v* 1/6 (v+ (.dv a) (v* 2 (v+ (.dv b) (.dv c))) (.dv d))))))))

;demo
(def acceleration
  (spring 20 0.5))

(defn simulate [state t dt]
  (integrate state t dt acceleration))

(defn render [^Graphics2D g w h ^State state]
  (doto g
    (.setColor Color/black)
    (.fillRect 0 0 w h)
    (.setColor Color/white)
    (.fillRect (- 200 (.x (.position state))) (- 200 (.y (.position state))) 15 15)))

(defn start []
  (game/start 400 400 25 simulate render (State. (vector-3d 200.0 100.0 0) vector-3d-zero)))
        
                                        ;(sim 100  1/10)
