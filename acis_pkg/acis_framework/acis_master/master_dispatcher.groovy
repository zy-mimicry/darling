#! /usr/bin/env groovy

/**/
/**/
/**/
/**/

def toLower(list){
    ArrayList tmp = []
    for (l in list){
        tmp.add(l.toLowerCase())
    }
    return tmp
}

def toUpper(list){
    ArrayList tmp = []
    for (l in list){
        tmp.add(l.toUpperCase())
    }
    return tmp
}

/* ACIS Exceptions*/
class FilterTypeError extends Exception{
    public FilterTypeError (String msg){
        super("\n\n" + msg + "\n\n")
    }
}

class MapsItemParseException extends Exception{
    public MapsItemParseException (String msg){
        super("\n\n" + msg + "\n\n")
    }
}

def pick_line_types(item, list){

    groups = item.trim().split("!")

    types  = groups[2].split(":")[0].trim()
    types_v  = groups[2].split(":")[1].trim().split(",")

    def k
    if ( types == "types"){
        for (k = 0; k < types_v.size(); k++){
            /* Check the type with LowerCase */
            if (!list.grep(types_v[k].toLowerCase())){
                list.add(types_v[k].toLowerCase())
            }
        }
    }else{
        throw new MapsItemParseException("In ACIS_MAPS file, 'types' needed, but your configure [" +  types + "]")
    }
}

def make_types_list(lines, list){

    def i
    for (i = 0 ; i < lines.size(); i++){
        pick_line_types(lines[i], list)
    }
}

def deal_line_item(item, maps){

    groups = item.trim().split("!")

    name   = groups[0].split(":")[0].trim().toLowerCase()
    labels = groups[1].split(":")[0].trim().toLowerCase()
    types  = groups[2].split(":")[0].trim().toLowerCase()
    times  = groups[3].split(":")[0].trim().toLowerCase()

    name_v   = groups[0].split(":")[1].trim()
    ArrayList labels_v = groups[1].split(":")[1].trim().split(",")
    labels_v = toUpper(labels_v)
    types_v  = groups[2].split(":")[1].trim().split(",")
    times_v  = groups[3].split(":")[1].trim()

    if ( name == "casename"){
        maps[name_v] = [:]
    }else{
        throw new MapsItemParseException("In ACIS_MAPS file, 'casename' needed, but your configure [" +  name + "]")
    }
    if ( labels == "labels"){
        maps[name_v]["labels"] = labels_v
    }else{
        throw new MapsItemParseException("In ACIS_MAPS file, 'labels' needed, but your configure [" + labels + "]")
    }
    if ( types == "types"){
        maps[name_v]["types"] = types_v
    }else{
        throw new MapsItemParseException("In ACIS_MAPS file, 'types' needed, but your configure [" +  types + "]")
    }
    if ( times == "times"){
        maps[name_v]["times"] = times_v
    }else{
        throw new MapsItemParseException("In ACIS_MAPS file, 'times' needed, but your configure [" + times + "]")
    }
}


def MAPS_to_list(maps){
    return maps.trim().split(";")
}

def make_curser_maps(list, curser, maps){

    def i
    for (i = 0; i < list.size(); i++){
        curser.add(list[i].split("!")[0].split(":")[1].trim())
        deal_line_item(list[i], maps)
    }

    println maps
    println curser
}

def make_filter_maps(filter, /*env.FILTER*/
                     file,   /*Git file -- ACIS_MAPS.txt*/
                     maps,   /*ACIS_MAPS.txt to dict*/
                     maps_curser, /*The dict's curser list*/
                     new_maps,    /*Fill a new dict*/
                     new_maps_curser){ /*a new dict curser list*/

    ArrayList filter_types = filter.trim().split(",")
    filter_types = toLower(filter_types)
    ArrayList types_list = []
    def i,c
    make_types_list(MAPS_to_list(file), types_list)
    types_list = toLower(types_list) /* Maybe superfluous, but temporarily reserved*/
    println types_list
    println filter_types

    for(i = 0 ; i < filter_types.size(); i++){
        if (types_list.grep(filter_types[i])){
            for (c = 0 ; c < maps_curser.size(); c++){
                if (maps[maps_curser[c]]["types"].grep(filter_types[i])){
                    new_maps[maps_curser[c]] = maps[maps_curser[c]]
                    new_maps_curser.add(maps_curser[c])
                }
            }
        }else{
            throw new FilterTypeError("Please check your env.FILTER, framework can NOT know that [" + filter_types[i] + "]")
        }
    }
}

def remove_dup_self(maps_curser){ /*curser must be a list or support unique() method.*/
    maps_curser.unique()
}

def merge_maps(maps,
               maps_curser,
               maps_filter,
               maps_filter_curser,
               maps_merged,
               maps_merged_curser){

    remove_dup_self(maps_curser)
    remove_dup_self(maps_filter_curser)

    def overwrite = []
    def a,c,d,g

    for (a = 0; a < maps_curser.size(); a++ ){
        for (b = 0; b < maps_filter_curser.size(); b++){
            if (maps_curser[a] == maps_filter_curser[b]){
                overwrite.add(maps_curser[a])
            }
        }
    }

    println overwrite

    for (c = 0; c < maps_filter_curser.size(); c++){
        for (d = 0; d < overwrite.size(); d++){
            if (maps_filter_curser[c] != overwrite[d]){
                maps_merged[maps_filter_curser[c]] = maps_filter[maps_filter_curser[c]]
                maps_merged_curser.add(maps_filter_curser[c])
            }
        }
    }

    for(g = 0; g < maps_curser.size(); g++){
        maps_merged[maps_curser[g]] = maps[maps_curser[g]]
        maps_merged_curser.add(maps_curser[g])
    }
}

/* If you add some envs, please modify here
 * For 'Linux', environments should be Upper, Just like 'LABEL'
 */
def make_testplan(maps, curser, testplan){

    def list = []
    def i

    for(i = 0; i < curser.size(); i++){

        maps[curser[i]]["labels"].add(env.PLATFORM) /* PLATFORM different 9x or 9x platform */

        /* MAPS and FILTER range */
        list.add([$class : "StringParameterValue", "name": "CASENAME", "value": curser[i]])
        /* Please set 'label' to lower case. */
        list.add([$class : "LabelParameterValue",  "name": "label", "label": maps[curser[i]]["labels"].join("&&")])
        list.add([$class : "StringParameterValue", "name": "TIMES", "value": maps[curser[i]]["times"].toString()])
        list.add([$class : "StringParameterValue", "name": "TYPES", "value": maps[curser[i]]["types"].join(",")])

        /* Other userful parameters */
        list.add([$class : "StringParameterValue", "name": "FW_VERSION", "value": env.FW_VERSION])
        list.add([$class : "StringParameterValue", "name": "FW_IMAGE_PATH", "value": env.FW_IMAGE_PATH])
        list.add([$class : "StringParameterValue", "name": "PLATFORM", "value": env.PLATFORM])
        list.add([$class : "StringParameterValue", "name": "FW_UPDATE", "value": env.FW_UPDATE])
        list.add([$class : "StringParameterValue", "name": "ACIS_DIFF", "value": env.ACIS_DIFF])
        //list.add([$class : "StringParameterValue", "name": "TESTCASE_PATH", "value": env.TESTCASE_PATH + '/' + env.PLATFORM])
        list.add([$class : "StringParameterValue", "name": "TESTCASE_PATH", "value": env.TESTCASE_PATH])
        list.add([$class : "StringParameterValue", "name": "REPORT_PATH", "value": env.REPORT_PATH])
        //list.add([$class : "StringParameterValue", "name": "LOOP_TEST", "value": env.LOOP_TEST + '/' + env.PLATFORM])
        list.add([$class : "StringParameterValue", "name": "LOOP_TEST", "value": env.LOOP_TEST])

        /* Cookie for parallel */
        testplan[curser[i]] = [ "job": "common_job" ,"parameters": list, "flags" : ""]
        list = []
    }
}

def get_cookie(){

    def maps = [:]
    def maps_curser = []

    def maps_file = [:]            /*From Git repo file -- ACIS_MAPS.txt*/
    def maps_file_curser = []      /*a curser list for maps dict*/

    def maps_filter = [:]
    def maps_filter_curser = []

    def maps_merged = [:]
    def maps_merged_curser = []

    make_curser_maps(MAPS_to_list(env.MAPS),   /*env.MAPS to list*/
                     maps_curser,         /*make a curser list for maps dict*/
                     maps)                /*maps dic*/

    //def file = new File("${workspace}/ACIS_MAPS.txt")
    
    def file = readFile("${workspace}/ACIS_MAPS.txt");
    
    
    make_curser_maps(MAPS_to_list(file),
                     maps_file_curser,
                     maps_file)

    make_filter_maps(env.FILTER,
                     file,
                     maps_file,
                     maps_file_curser,
                     maps_filter,
                     maps_filter_curser)

    println maps_filter
    println maps_filter_curser

    merge_maps(maps,
               maps_curser,
               maps_filter,
               maps_filter_curser,
               maps_merged,
               maps_merged_curser)
    println maps_merged
    println maps_merged_curser

    def testplan = [:]
    def testplan_curser = maps_merged_curser
    make_testplan(maps_merged,
                  maps_merged_curser,
                  testplan)

    return [testplan, testplan_curser]
}

return this
