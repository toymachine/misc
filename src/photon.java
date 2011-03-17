interface ByteStream {
	def read() : (int, bytes)
	def write(bytes b)
}

interface File : ByteStream { 
    //there is no interface inheritance, the interface definitioin is what you get, no need to lookup inheritance tree
    //the bytestream here just documents that File is compatible with bytestream

    val MODE_R = “r”
	val MODE_RW = “rw”

    val BLAAT = [1,2,3,4] //constant list
    val PIET = {1: 2, 3: 4} //constant dict

    //interface methods
	def read() : int, bytes
	def write(bytes b)
    def close()

    //declare public static methods
    def ::open(string name, string mode) : File
}

//implement static method
def File::open(string name, string mode) : File
    return File() { 
        //return an implementation of interface 'File'
    	def read() : int, bytes {
    	}

    	def write(bytes b) {
    	}

        def close()  {
        }
    }
}

interface MyTuple(string name, string address) {
    def getName() {
        return name
    }

    def getAdress() {
        return address
    }
}

val mt = MyTuple("piet", "klaas")

interface iterable {
    def next() : any
}

//generator function
def map(function f, iterable i) : any
{
    for(x in i) {
        yield f(x)
    }
}

def enumerate(iterable i) : (int, any)
{
    var i = 0
    for(x in i) {
        yield (i, x)
    }
}

def main(list argv) : int
{
	return 10
}

val f = File.open(“c:\tmp\blaat.txt”, File.MODE_RW)
f.write(“piet”.toBytes())
val (bytes_read, bytes) = f.read() #destructuring

val mt = MyTuple(“piet”, “blaa”)

mt.name == “piet”
mt.adress == “blaa”


int
float
string (immutable string)
bytes (byte buffer for efficient io)
dict (mutable and non-mutable), key = immutable any, value = any
list  (mutable and non-mutable) holds anys
tuple (immutable)
function (the function instance)
interface (dict of name=>function or value)
    + user defined subtypes
any (a variant type)


