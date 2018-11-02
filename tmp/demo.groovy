#! /usr/bin/env groovy
import hudson.model.*

/**/
/**/
/**/
/**/

str = """
casename: AAA ! labels: qmi,jj ! types: driver,ppy ! times: 3;
casename: BBB ! labels: spi,mm ! types: system,mmd ! times: 2;
casename: CCC ! labels: i2c ! types: qmi,ac,mdd ! times: 1;
casename: DDD ! labels: eth,t ! types: audio,wifi ! times: 4;
"""

list = str.trim().split(";")

casenames = []

for (i = 0; i < list.size(); i++){
    casenames.add(list[i].split("!")[0].split(":")[1].trim())
}

println casenames

class MapsItemParseException extends Exception{
    public MapsItemParseException (String msg){
        super(msg)
    }
}

maps = [:]

def deal_line(item){

    groups = item.trim().split("!")

    name   = groups[0].split(":")[0].trim()
    labels = groups[1].split(":")[0].trim()
    types  = groups[2].split(":")[0].trim()
    times  = groups[3].split(":")[0].trim()

    name_v   = groups[0].split(":")[1].trim()
    labels_v = groups[1].split(":")[1].trim().split(",")
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

for(i = 0; i < list.size(); i++){
    deal_line(list[i])
}

println maps

// def deal_line(item){

//     groups = item.split("!")
//     println groups[0].split(":")[0].trim().class

//     if (groups[0].split(":")[0].trim() == "casename"){
//         println groups[0].split(":")[1].trim()
//         maps[groups[0].split(":")[1].trim()] = [:]
//     }else{
//         throw new MapsItemParseException("In ACIS_MAPS file, 'casename' needed, but your configure [" +  groups[0].split(":")[0].trim() + "]")
//     }
//     if (groups[1].split(":")[0].trim() == "labels"){
//         println groups[1].split(":")[1].trim()
//         maps[groups[0].split(":")[1].trim()]["labels"] = groups[1].split(":")[1].trim().split(",")
//     }else{
//         throw new MapsItemParseException("In ACIS_MAPS file, 'labels' needed, but your configure [" + groups[1].split(":")[0].trim() + "]")
//     }
//     if (groups[2].split(":")[0].trim() == "types"){
//         println groups[2].split(":")[1].trim()
//         maps[groups[0].split(":")[1].trim()]["types"] = groups[2].split(":")[1].trim().split(",")
//     }else{
//         throw new MapsItemParseException("In ACIS_MAPS file, 'types' needed, but your configure [" +  groups[2].split(":")[0].trim() + "]")
//     }
//     if (groups[3].split(":")[0].trim() == "times"){
//         println groups[3].split(":")[1].trim()
//         maps[groups[0].split(":")[1].trim()]["times"] = groups[3].split(":")[1].trim()
//     }else{
//         throw new MapsItemParseException("In ACIS_MAPS file, 'times' needed, but your configure [" + groups[3].split(":")[0].trim() + "]")
//     }
// }


// def show(){
//     println("""
//     === [Beg] All Envs Provided by User ===

// [MAPS]
// ${env.MAPS}

// [FILTER]
// ${env.FILTER}

// [PLATFORM]
// ${env.PLATFORM}

// [FW_VERSION]
// ${env.FW_VERSION}

// [FW_IMAGE_PATH]
// ${env.FW_IMAGE_PATH}

//     === [End] All Envs Provided by User ===
//     """)
// }

// def strip_and_export(){
//     env.PLATFORM = env.PLATFORM.trim()
//     env.MAPS = env.MAPS.trim()
//     env.FILTER = env.FILTER.trim()
//     env.FW_VERSION = env.FW_VERSION.trim()
//     env.FW_IMAGE_PATH = env.FW_IMAGE_PATH.trim()
// }

//def matcher = readFile("${workspace}/ACIS_MAPS.txt")
import java.io.File
def file = new File("${workspace}/ACIS_MAPS.txt")
println file.class
println file.text


def exec_stage(string){
    println "-- Execute [" + string + "] stage......"
    // strip_and_export()
    // show()
    // println env.class
    // println env.PLATFORM.class
    println "-- Execute [" + string + "] stage done."
}
exec_stage("mm")



return this
