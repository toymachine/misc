/*
(defn v+
  ([^Vector3D a ^Vector3D b]
     (vector-3d (+ (.x a) (.x b))
                (+ (.y a) (.y b))
                (+ (.z a) (.z b))))
  ([^Vector3D a ^Vector3D b & more]
     (reduce v+ (v+ a b) more)))
*/

public class Test
{
    public static void main(String[] argv) 
    {
	double s_x = 0.0, s_y = 0.0, s_z = 0.0;
	double a_x = 0.1, a_y = 0.2, a_z = 0.3;

	long start = System.nanoTime();
	for(long i = 0; i < 3000000000l; i++) {
	    s_x += a_x;
	    s_y += a_y;
	    s_z += a_z;
	}
	long end = System.nanoTime();

	System.out.println("Hello World! " + s_x + " " + s_y + " " + s_z + " " + ((end - start) / 1000000000.0));
    }
}