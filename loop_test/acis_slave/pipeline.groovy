#! /usr/bin/env groovy

node('master')
{
    def workspace = pwd()
    
    stage("master_envs_parser"){
        println "workspace: ${workspace}"
        def m = load "${workspace}/master_envs_parser.groovy"
        m.strip_and_export()
        m.show()
    }
    
    stage('master_job_monitor'){
        //sh "python3 ${workspace}/master_job_monitor.py"
    }
    
    stage('master_dispatcher'){

        //sh "python3 ${workspace}/master_mktree.py -s ${env.TESTCASE_PATH} -d ${env.REPORT_PATH}/${env.PLATFORM} -D ${env.ACIS_DIFF}"
        //sh "python3 ${workspace}/master_mktree.py -s ${env.TESTCASE_PATH} -d ${env.LOOP_TEST}/${env.PLATFORM} -D ${env.ACIS_DIFF}"
        sh "python3 ${workspace}/master_mktree.py -s /home/rex/nfs_acis/Integration_Test/acis_testcases -d /home/rex/nfs_acis/Integration_Test/log_and_report/${env.PLATFORM} -D ${env.ACIS_DIFF}"
        sh "python3 ${workspace}/master_mktree.py -s /home/rex/nfs_acis/Integration_Test/acis_testcases -d /home/rex/nfs_acis/Integration_Test/loop_test/${env.PLATFORM} -D ${env.ACIS_DIFF}"
        //sh 'mkdir /home/rex/nfs_acis/Integration_Test/loop_test/${env.PLATFORM}/${env.ACIS_DIFF}/acis_testcases/QMI'
        println "<< hook here >>"
        def dispatcher = load "${workspace}/master_dispatcher.groovy"
        
        def cookie = dispatcher.get_cookie()
        testplan = cookie[0]
        testplan_curser = cookie[1]
        
        //println testplan[testplan_curser[0]]["job"]
        //println testplan[testplan_curser[0]]["parameters"]
        
        //def item = testplan[testplan_curser[0]]
        //def builders = [:]
        //builders[testplan_curser[0]] = {
        //    build(job: item["job"],
        //          parameters: item["parameters"],
        //          wait: true)
        //}
        def builders = [:]
        for(i = 0; i < testplan_curser.size(); i++){
            def item = testplan[testplan_curser[i]]
            builders[testplan_curser[i]] = {
                build(job: item["job"],
                      parameters: item["parameters"],
                      wait: true)
            }            
        }
        parallel(builders)
    }
    
    stage('master_report'){
        //println "--- Jenkins Master report stage. Hook"
    }
    
    stage('master_db'){
        //println "--- Jenkins Master Database stage. Hook"
    }
    
    stage('master_web'){
        //println "--- Jenkins Master Website stage. Hook"
    }
}  