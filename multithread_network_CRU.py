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


class myThread(threading.Thread):

    def __init__(self, x):
        threading.Thread.__init__(self)
        self.x = x
        self.tenant = 'tenant' + str(x)
        self.networkcount = 5
        self.subnetcount = 4
        self.routercount = 10
        self.portcount = 100
        self.securitygroupcount = 50
        self.securitygrouprulecount = 1
        self.floatingipcount = 5

    def run(self):

        buildcommandtenantcreation = \
            'keystone --os-tenant-name openstack --os-username admin --os-password Chang3M3 --os-auth-url https://identity.jiocloud.com:5000/v2.0/ tenant-create --name ' \
            + self.tenant + ''
        ret = os.system(buildcommandtenantcreation)

        buildcommandusercreation = \
            'keystone --os-tenant-name openstack --os-username admin --os-password Chang3M3 --os-auth-url https://identity.jiocloud.com:5000/v2.0/ user-create --name=' \
            + self.tenant + 'user --pass=pass'
        ret = os.system(buildcommandusercreation)

        buildcommandtenantuserroleassociation = \
            'keystone --os-tenant-name openstack --os-username admin --os-password Chang3M3 --os-auth-url https://identity.jiocloud.com:5000/v2.0/ user-role-add --user=' \
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
                + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
            ret = os.system(buildcommandrouter)
            if ret != 0:
                failroutercreate = failroutercreate + 1
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
                + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
            ret = os.system(buildcommandnetwork)

            if ret != 0:
                failnetworkcreate = failnetworkcreate + 1
            else:
                passnetworkcreate = passnetworkcreate + 1

            for s in range(self.subnetcount):

                buildcommandsubnet = \
                    'neutron subnet-create --name subnet' + str(s) \
                    + ' network' + str(n) + ' ' + str(s) \
                    + '.0.0.0/24 --os-username ' + self.tenant \
                    + 'user --os-password pass --os-tenant-name ' \
                    + self.tenant \
                    + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
                ret = os.system(buildcommandsubnet)

                if ret != 0:
                    failsubnetcreate = failsubnetcreate + 1
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
                + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
            ret = os.system(buildcommandport)

            if ret != 0:
                failportcreate = failportcreate + 1
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
                + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
            ret = os.system(buildcommandsecuritygroup)

            if ret != 0:
                failsecuritygroupcreate = failsecuritygroupcreate + 1
            else:
                passsecuritygroupcreate = passsecuritygroupcreate + 1

            for sgr in range(self.securitygrouprulecount):

                buildcommandsecuritygrouprule = \
                    'neutron security-group-rule-create --direction ingress --ethertype IPv4 --protocol tcp --port-range-min 80 --port-range-max 80 securitygroup' \
                    + str(sg) + ' --os-username ' + self.tenant \
                    + 'user --os-password pass --os-tenant-name ' \
                    + self.tenant \
                    + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
                ret = os.system(buildcommandsecuritygrouprule)

                if ret != 0:
                    failsecuritygrouprulecreate = \
                        failsecuritygrouprulecreate + 1
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
                + ' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
            ret = os.system(buildcommandfloatingip)

            if ret != 0:
                failfloatingipcreate = failfloatingipcreate + 1
            else:
                passfloatingipcreate = passfloatingipcreate + 1

        print '####### summary of '+ self.tenant +' run #######'
        print 'For ' + self.tenant \
            + ' floatingip PASS = %d FAIL = %d' \
            % (passfloatingipcreate, failfloatingipcreate)

        print 'For ' + self.tenant \
	    + ' router PASS = %d FAIL = %d' \
            % (passroutercreate, failroutercreate)

        print 'For ' + self.tenant \
            + ' network PASS = %d FAIL = %d' \
            % (passnetworkcreate, failnetworkcreate)

        print 'For ' + self.tenant \
            + ' subnet PASS = %d FAIL = %d' \
            % (passsubnetcreate, failsubnetcreate)

        print 'For ' + self.tenant \
            + ' port PASS = %d FAIL = %d' \
            % (passportcreate, failportcreate)

        print 'For ' + self.tenant \
            + ' securitygroup PASS = %d FAIL = %d' \
            % (passsecuritygroupcreate, failsecuritygroupcreate)

	print 'For ' + self.tenant \
            + ' securitygrouprule PASS = %d FAIL = %d' \
            % (passsecuritygrouprulecreate,failsecuritygrouprulecreate)

	totalapipass=passfloatingipcreate+passroutercreate+passnetworkcreate+passsubnetcreate+passportcreate+passsecuritygroupcreate+passsecuritygrouprulecreate
	totalapifail=failfloatingipcreate+failroutercreate+failnetworkcreate+failsubnetcreate+failportcreate+failsecuritygroupcreate+failsecuritygrouprulecreate
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


