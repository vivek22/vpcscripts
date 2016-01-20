#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ' VIVEK SHARMA '

# importing modules

import os
import sys
import re
import string
import time
import threading
import thread
import ConfigParser

class myThread(threading.Thread):

    def __init__(self, x):
        threading.Thread.__init__(self)
        self.x = x
        self.tenant = 'tenant' + str(x)

        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'performanceconfig.txt'
        configParser.read(configFilePath)
        self.networkcount = int(configParser.get('QUOTA', 'networkcount'))
        self.subnetcount = int(configParser.get('QUOTA', 'subnetcount'))
        self.routercount = int(configParser.get('QUOTA', 'routercount'))
        self.portcount = int(configParser.get('QUOTA', 'portcount'))
        self.securitygroupcount = int(configParser.get('QUOTA', 'securitygroupcount'))
        self.securitygrouprulecount = int(configParser.get('QUOTA', 'securitygrouprulecount'))
        self.floatingipcount= int(configParser.get('QUOTA', 'floatingipcount'))

        self.OS_TENANT_NAME=configParser.get('ADMINRC','OS_TENANT_NAME')
        self.OS_USERNAME=configParser.get('ADMINRC','OS_USERNAME')
        self.OS_PASSWORD=configParser.get('ADMINRC','OS_PASSWORD')
        self.OS_AUTH_URL=configParser.get('ADMINRC','OS_AUTH_URL')

    def run(self):

        buildcommandtenantcreation = 'keystone --os-tenant-name '+self.OS_TENANT_NAME+' --os-username '+self.OS_USERNAME+' --os-password '+self.OS_PASSWORD+' --os-auth-url '+self.OS_AUTH_URL+' tenant-create --name '+ self.tenant+''
        ret = os.system(buildcommandtenantcreation)

        buildcommandusercreation = \
            'keystone --os-tenant-name '+self.OS_TENANT_NAME+' --os-username '+self.OS_USERNAME+' --os-password '+self.OS_PASSWORD+' --os-auth-url '+self.OS_AUTH_URL+' user-create --name=' \
            + self.tenant + 'user --pass=pass'
        ret = os.system(buildcommandusercreation)

        buildcommandtenantuserroleassociation = \
            'keystone --os-tenant-name '+self.OS_TENANT_NAME+' --os-username '+self.OS_USERNAME+' --os-password '+self.OS_PASSWORD+' --os-auth-url '+self.OS_AUTH_URL+' user-role-add --user=' \
            + self.tenant + 'user --tenant=' + self.tenant \
            + ' --role=Member'
        ret = os.system(buildcommandtenantuserroleassociation)

                # # till this point tenant creation and under that tenant user creation and already created role i.e admin associaion to that user ##

        passroutercreate = 0
        failroutercreate = 0
        for r in range(self.routercount):

            buildcommandrouter = 'neutron router-create router' \
                + str(r) + ' --os-username ' + self.tenant \
                + 'user --os-password pass --os-tenant-name ' \
                + self.tenant \
                + ' --os-auth-url '+self.OS_AUTH_URL+''
            ret = os.system(buildcommandrouter)
            if ret != 0:
                failroutercreate = failroutercreate + 1
		sys.exit(0)
            else:
                passroutercreate = passroutercreate + 1

        passnetworkcreate = 0
        failnetworkcreate = 0
        passsubnetcreate = 0
        failsubnetcreate = 0

        for n in range(self.networkcount):

            buildcommandnetwork = 'neutron net-create network' + str(n) \
                + ' --os-username ' + self.tenant \
                + 'user --os-password pass --os-tenant-name ' \
                + self.tenant \
                + ' --os-auth-url '+self.OS_AUTH_URL+''
            ret = os.system(buildcommandnetwork)

            if ret != 0:
                failnetworkcreate = failnetworkcreate + 1
		sys.exit(0)
            else:
                passnetworkcreate = passnetworkcreate + 1

            for s in range(self.subnetcount):

                buildcommandsubnet = \
                    'neutron subnet-create --name subnet' + str(s) \
                    + ' network' + str(n) + ' ' + str(s) \
                    + '.0.0.0/24 --os-username ' + self.tenant \
                    + 'user --os-password pass --os-tenant-name ' \
                    + self.tenant \
                    + ' --os-auth-url '+self.OS_AUTH_URL+''
                ret = os.system(buildcommandsubnet)

                if ret != 0:
                    failsubnetcreate = failsubnetcreate + 1
		    sys.exit(0)
                else:
                    psssubnetcreate = passsubnetcreate + 1

        passportcreate = 0
        failportcreate = 0
        for p in range(self.portcount):

            buildcommandport = \
                'neutron port-create network1 --fixed-ip ip_address=1.0.0.' \
                + str(p) + ' --os-username ' + self.tenant \
                + 'user --os-password pass --os-tenant-name ' \
                + self.tenant \
                + ' --os-auth-url '+self.OS_AUTH_URL+''
            ret = os.system(buildcommandport)

            if ret != 0:
                failportcreate = failportcreate + 1
		sys.exit(0)
            else:
                passportcreate = passportcreate + 1

        passsecuritygroupcreate = 0
        failsecuritygroupcreate = 0
        passsecuritygrouprulecreate = 0
        failsecuritygrouprulecreate = 0

        for sg in range(self.securitygroupcount):

            buildcommandsecuritygroup = \
                'neutron security-group-create securitygroup' + str(sg) \
                + ' --os-username ' + self.tenant \
                + 'user --os-password pass --os-tenant-name ' \
                + self.tenant \
                + ' --os-auth-url '+self.OS_AUTH_URL+''
            ret = os.system(buildcommandsecuritygroup)

            if ret != 0:
                failsecuritygroupcreate = failsecuritygroupcreate + 1
		sys.exit(0)
            else:
                passsecuritygroupcreate = passsecuritygroupcreate + 1

            for sgr in range(self.securitygrouprulecount):

                buildcommandsecuritygrouprule = \
                    'neutron security-group-rule-create --direction ingress --ethertype IPv4 --protocol tcp --port-range-min 80 --port-range-max 80 securitygroup' \
                    + str(sg) + ' --os-username ' + self.tenant \
                    + 'user --os-password pass --os-tenant-name ' \
                    + self.tenant \
                    + ' --os-auth-url '+self.OS_AUTH_URL+''
                ret = os.system(buildcommandsecuritygrouprule)

                if ret != 0:
                    failsecuritygrouprulecreate = \
                        failsecuritygrouprulecreate + 1
		    sys.exit(0)	
                else:
                    passsecuritygrouprulecreate = \
                        passsecuritygrouprulecreate + 1

        passfloatingipcreate = 0
        failfloatingipcreate = 0
        for f in range(self.floatingipcount):

            buildcommandfloatingip = \
                'neutron floatingip-create public --os-username ' \
                + self.tenant \
                + 'user --os-password pass --os-tenant-name ' \
                + self.tenant \
                + ' --os-auth-url '+self.OS_AUTH_URL+''
            ret = os.system(buildcommandfloatingip)

            if ret != 0:
                failfloatingipcreate = failfloatingipcreate + 1
		sys.exit(0)
            else:
                passfloatingipcreate = passfloatingipcreate + 1

        ##Till this point logical creation for each tenant is created ##

        passrouterlist = 0
        failrouterlist = 0

        buildcommandrouterlist ='neutron router-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandrouterlist)

        if ret !=0:
                failrouterlist = failrouterlist + 1
        else:
                passrouterlist = passrouterlist + 1

        passroutershow = 0
        failroutershow = 0

        for r in range (self.routercount):

                buildcommandroutershow ='neutron router-show router'+str(r)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
                ret = os.system(buildcommandroutershow)

                if ret !=0:
                        failroutershow = failroutershow + 1
                else:
                        passroutershow = passroutershow + 1

        passnetworklist = 0
        failnetworklist = 0
        passnetworkshow = 0
        failnetworkshow = 0

        buildcommandnetworklist ='neutron net-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandnetworklist)

        if ret !=0:
                failnetworklist = failnetworklist + 1
        else:
                passnetworklist = passnetworklist + 1

        for n in range (self.networkcount):

                buildcommandnetworkshow ='neutron net-show network'+str(n)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
                ret = os.system(buildcommandnetworkshow)

                if ret !=0:
                        failnetworkshow = failnetworkshow + 1
                else:
                        passnetworkshow = passnetworkshow + 1

        passsubnetlist = 0
        failsubnetlist = 0

        buildcommandsubnetlist ='neutron subnet-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandsubnetlist)

        if ret !=0:
                failsubnetlist = failsubnetlist + 1
        else:
                passsubnetlist = passsubnetlist + 1

        passsubnetshow = 0
        failsubnetshow = 0

        buildcommandsubnetshow ='for s in $(neutron subnet-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' | awk  \'{print $2}\'); do neutron subnet-show --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' $s; done'
        ret = os.system(buildcommandsubnetshow)

        if ret !=0:
                failsubnetshow = failsubnetshow + 1
        else:
                passsubnetshow = passsubnetshow + 1

        passportlist = 0
        failportlist = 0

        buildcommandportlist ='neutron port-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandportlist)

        if ret !=0:
                failportlist = failportlist + 1
        else:
                passportlist = passportlist + 1

        passportshow = 0
        failportshow = 0

        buildcommandportshow ='for p in $(neutron port-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' | awk  \'{print $2}\'); do neutron port-show --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' $p; done'
        ret = os.system(buildcommandportshow)

        if ret !=0:
                failportshow = failportshow + 1
        else:
                passportshow = passportshow + 1

        passsecuritygrouplist = 0
        failsecuritygrouplist = 0
        passsecuritygroupshow = 0
        failsecuritygroupshow = 0

        buildcommandsecuritygrouplist ='neutron security-group-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandsecuritygrouplist)

        if ret !=0:
                failsecuritygrouplist = failsecuritygrouplist + 1
        else:
                passsecuritygrouplist = passsecuritygrouplist + 1

        for sg in range (self.securitygroupcount):

                buildcommandsecuritygroupshow ='neutron security-group-show securitygroup'+str(sg)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
                ret = os.system(buildcommandsecuritygroupshow)

                if ret !=0:
                        failsecuritygroupshow = failsecuritygroupshow + 1
                else:
                        passsecuritygroupshow = passsecuritygroupshow + 1

        passsecuritygrouprulelist = 0
        failsecuritygrouprulelist = 0

        buildcommandsecuritygrouprulelist ='neutron security-group-rule-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandsecuritygrouprulelist)

        if ret !=0:
                failsecuritygrouprulelist = failsecuritygrouprulelist + 1
        else:
                passsecuritygrouprulelist = passsecuritygrouprulelist + 1

        passfloatingiplist = 0
        failfloatingiplist = 0

        buildcommandfloatingiplist ='neutron floatingip-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
        ret = os.system(buildcommandfloatingiplist)

        if ret !=0:
                failfloatingiplist = failfloatingiplist + 1
        else:
                passfloatingiplist = passfloatingiplist + 1

        passfloatingipshow = 0
        failfloatingipshow = 0

        buildcommandfloatingipshow ='for f in $(neutron floatingip-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' | awk  \'{print $2}\'); do neutron floatingip-show --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' $f; done'
        ret = os.system(buildcommandfloatingipshow)

        if ret !=0:
                failfloatingipshow = failfloatingipshow + 1
        else:
                passfloatingipshow = passfloatingipshow + 1


        print '####### summary of '+ self.tenant +' run #######'
        print 'For ' + self.tenant \
            + ' floatingip create PASS = %d FAIL = %d' \
            % (passfloatingipcreate, failfloatingipcreate)

        print 'For ' + self.tenant \
            + ' router create PASS = %d FAIL = %d' \
            % (passroutercreate, failroutercreate)

        print 'For ' + self.tenant \
            + ' network create PASS = %d FAIL = %d' \
            % (passnetworkcreate, failnetworkcreate)

        print 'For ' + self.tenant \
            + ' subnet create PASS = %d FAIL = %d' \
            % (passsubnetcreate, failsubnetcreate)

        print 'For ' + self.tenant \
            + ' port create PASS = %d FAIL = %d' \
            % (passportcreate, failportcreate)

        print 'For ' + self.tenant \
            + ' securitygroup create PASS = %d FAIL = %d' \
            % (passsecuritygroupcreate, failsecuritygroupcreate)

        print 'For ' + self.tenant \
            + ' securitygrouprule create PASS = %d FAIL = %d' \
            % (passsecuritygrouprulecreate,failsecuritygrouprulecreate)

        print 'For ' + self.tenant \
            + ' router list PASS = %d FAIL = %d' \
            % (passrouterlist,failrouterlist)

        print 'For ' + self.tenant \
            + ' router show PASS = %d FAIL = %d' \
            % (passroutershow,failroutershow)

        print 'For ' + self.tenant \
            + ' network list PASS = %d FAIL = %d' \
            % (passnetworklist,failnetworklist)

        print 'For ' + self.tenant \
            + ' network show PASS = %d FAIL = %d' \
            % (passnetworkshow,failnetworkshow)

        print 'For ' + self.tenant \
            + ' subnet list PASS = %d FAIL = %d' \
            % (passsubnetlist,failsubnetlist)

        print 'For ' + self.tenant \
            + ' subnet show PASS = %d FAIL = %d' \
            % (passsubnetshow,failsubnetshow)

        print 'For ' + self.tenant \
            + ' port list PASS = %d FAIL = %d' \
            % (passportlist,failportlist)

        print 'For ' + self.tenant \
            + ' port show PASS = %d FAIL = %d' \
            % (passportshow,failportshow)

        print 'For ' + self.tenant \
            + ' securitygroup list PASS = %d FAIL = %d' \
            % (passsecuritygrouplist,failsecuritygrouplist)

        print 'For ' + self.tenant \
            + ' securitygroup show PASS = %d FAIL = %d' \
            % (passsecuritygroupshow,failsecuritygroupshow)

        print 'For ' + self.tenant \
            + ' securitygrouprule list PASS = %d FAIL = %d' \
            % (passsecuritygrouprulelist,failsecuritygrouprulelist)

        print 'For ' + self.tenant \
            + ' floatingip list PASS = %d FAIL = %d' \
            % (passfloatingiplist,failfloatingiplist)

        print 'For ' + self.tenant \
            + ' floatingip show PASS = %d FAIL = %d' \
            % (passfloatingipshow,failfloatingipshow)


        totalapipass=passfloatingipcreate+passroutercreate+passnetworkcreate+passsubnetcreate+passportcreate+passsecuritygroupcreate+passsecuritygrouprulecreate+passrouterlist+passroutershow+passnetworklist+passnetworkshow+passsubnetlist+passsubnetshow+passportlist+passportshow+passsecuritygrouplist+passsecuritygroupshow+passsecuritygrouprulelist+passfloatingiplist+passfloatingipshow

        totalapifail=failfloatingipcreate+failroutercreate+failnetworkcreate+failsubnetcreate+failportcreate+failsecuritygroupcreate+failsecuritygrouprulecreate+failrouterlist+failroutershow+failnetworklist+failnetworkshow+failsubnetlist+failsubnetshow+failportlist+failportshow+failsecuritygrouplist+failsecuritygroupshow+failsecuritygrouprulelist+failfloatingiplist+failfloatingipshow

	totalapi=totalapipass+totalapifail
	percentagepass=(totalapipass/totalapi*100)
	percentagefail=(totalapifail/totalapi*100)
	print 'For '+ self.tenant +' TOTAL API = %d PASS = %d FAIL = %d' %(totalapi,totalapipass,totalapifail)
	print 'For '+ self.tenant +' PASS PERCENTAGE = %d FAIL PERCENTAGE = %d' %(percentagepass,percentagefail)
	print '############################ END '+self.tenant+' END ##################################'

# boilerplate

if __name__ == '__main__':

    for x in range(3):
        thread1 = myThread(x)
        thread1.start()

    print 'x'


