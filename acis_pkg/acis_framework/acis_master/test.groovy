#! /usr/bin/env groovy


testplan = ["AAA":["labels": ["spi", "i2c"], "types" : ["driver"], "times": 3],
            "BBB":["labels": ["mm", "kk"], "types":["system", "qmi"], "times": 100],
            "CCC":["labels": ["tt", "yy"], "types":["rele", "audio"], "times": 22]]

curser = ["AAA", "BBB", "CCC"]

template = ["string": ["template_string": "string", "name" : "", "value" : ""],
            "label": ["template_label": "label", "name": "", "label" : ""]]

def make_testplan(curser, testplan){
    def map = [:]
    def list = []

    for(i = 0; i < curser.size(); i++){

        list.add(["t": "string", "name": "casename", "value": curser[i]])
        list.add(["t": "label",  "name": "label", "label": testplan[curser[i]]["labels"].join("&&")])
        list.add(["t": "string", "name": "times", "value": testplan[curser[i]]["times"].toString()])
        list.add(["t": "string", "name": "types", "value": testplan[curser[i]]["types"].join(",")])

        list.add(["f": "string", "name": "fw_version", "value": "1234"])
        list.add(["f": "string", "name": "fw_image_path", "value": "http://hello.com"])
        list.add(["f": "string", "name": "platform", "value": "9X40"])

        map[curser[i]] = list
        list = []

    }
    return map
}

map = make_testplan(curser, testplan)
println map

def date_diff = new Date().format('yyyy_MM_dd_HH_mm_ss')
println date_diff

return this
