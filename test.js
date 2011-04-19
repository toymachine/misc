import java.text.SimpleDateFormat;

SDF_MONTH = SimpleDateFormat("yyyy-MM");

function main() {

    m = with(open("/home/henk/tmp/montlyuniques.txt"), function(f) {
        return {}.put(map(f, function(line) {
            return line.split('\t'), lineSplit[0].split('_') 
        }))
    }

    dates = map(m.keys(), SDF_MONTH.format)
    
    chart = {}.put("caption", "Seconds per part")
              .put("xaxisname", "Month")
              .put("yaxisname", "Seconds")

    data = {}.put("chart", chart)

    with(open("data3.js", "w"), function(f) {
        f.write("chartdata(" + gson.toJson(data) + ")")
    })

}

