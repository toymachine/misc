public class test
{
    public static class func_sum implements Function {
        public int call(int a, int b) {
            func_sum_plus2 sum_plus2 = new func_sum_plus2(a);
            return a + b + sum_plus2.call(10, 20);
        }
    }

    public static class func_sum_plus2 implements Function {
        private int a;
        func_sum_plus2(int a) {
            this.a = a;
        }
        public int call(int x, int y) {
            return this.a + x + y;
        }
    }
}