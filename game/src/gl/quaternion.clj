(ns sio.quaternion)

(deftype Quaternion [w x y z])

(defn create [w x y z]
  (Quaternion. w x y z))

(def identity
  (quaternion 1 0 0 0))

(defn length [a]
  (Math/sqrt (+ (* (.w a) (.w a))
                (* (.x a) (.x a))
                (* (.y a) (.y a))
                (* (.z a) (.z a)))))
                
  
(defn q+ [^Quaternion a ^Quaternion b]
  (Quaternion. (+ (.w a) (.w b))
               (+ (.x a) (.x b))
               (+ (.y a) (.y b))
               (+ (.z a) (.z b))))

(defn q* [s ^Quaternion a]
  (Quaternion. (* s (.w a))
               (* s (.x a))
               (* s (.y a))
               (* s (.z a))))

(defn normalize [a]
  (let [len (length a)]
    (if (= len 0)
      (quaternion 1 0 0 0)
      ;else
      (q* (/ 1 len) a))))


(defn cosine [a b]
  (+ (* (.w a) (.w b))
     (* (.x a) (.x b))
     (* (.y a) (.y b))
     (* (.z a) (.z b))))
        
(defn slerp [a b t]
  {:pre [(>= t 0) (<= t 1)]}
  (let [cosine (cosine a b )]
    10))
    
  



