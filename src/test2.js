
interface ByteStream {
    function read() : int, bytes
    function write(bytes b)
}

interface File : ByteStream {
    const MODE_R = “r”
    const MODE_RW = “rw”

    function close()

    function ::open(string name, string mode) : File
}

struct NameAddress {
    string name
    string adress
    string country =     
}

// na = NameAddress("piet", "klaas") is possible

//static function
function File::open(string name, string mode) : File {
    return File { //returns an implementation (instance) of interface 'File'
    	function read() : int, bytes {
    	}
    	function write(bytes b) {
    	}
        function close()  {
        }
    }
}

interface Test : Main {
    function ::main(list argv) : int 
    {
        with File::open("piet", File.MODE_READ) as f {
            for(line in f.readlines()) {
                println(line)
            }
        }

        return sum(argv[0], arv[1])
    }
}

