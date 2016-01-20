#!/usr/bin/python

__author__= " VIVEK SHARMA "



#importing modules

import os
import sys
import re
import string
import time
import threading
import thread
import ConfigParser

class myThread(threading.Thread):

	def __init__(self,x):
                threading.Thread.__init__(self)
                self.x = x
                self.tenant = 'tenant'+str(x)

	        configParser = ConfigParser.RawConfigParser()
        	configFilePath = r'performanceconfig.txt'
	        configParser.read(configFilePath)
		
        	self.networkcount = int(configParser.get('QUOTA','networkcount'))
        	self.subnetcount = int(configParser.get('QUOTA','subnetcount'))
        	self.routercount = int(configParser.get('QUOTA','routercount'))
        	self.portcount = int(configParser.get('QUOTA','portcount'))
        	self.securitygroupcount = int(configParser.get('QUOTA','securitygroupcount'))
        	self.securitygrouprulecount = int(configParser.get('QUOTA','securitygrouprulecount'))
        	self.floatingipcount= int(configParser.get('QUOTA','floatingipcount'))

        	self.OS_TENANT_NAME=configParser.get('ADMINRC','OS_TENANT_NAME')
        	self.OS_USERNAME=configParser.get('ADMINRC','OS_USERNAME')
        	self.OS_PASSWORD=configParser.get('ADMINRC','OS_PASSWORD')
        	self.OS_AUTH_URL=configParser.get('ADMINRC','OS_AUTH_URL')


        def run(self):

		passportdelete=0
		failportdelete=0
		
                buildcommandport ='for p in $(neutron port-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' | awk  \'{print $2}\'); do neutron port-delete --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' $p; done'
                ret = os.system(buildcommandport)

                if ret !=0:
			failportdelete = failportdelete + 1
                else:
			passportdelete = passportdelete + 1
		
		passnetworkdelete=0
		failnetworkdelete=0

                for n in range (self.networkcount):

                        buildcommandnetwork ='neutron net-delete network'+str(n)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
                        ret = os.system(buildcommandnetwork)

                        if ret !=0:
				failnetworkdelete = failnetworkdelete + 1
                        else:
				passnetworkdelete = passnetworkdelete + 1

		passrouterdelete=0
		failrouterdelete=0

                for r in range (self.routercount):

                        buildcommandrouter ='neutron router-delete router'+str(r)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
                        ret = os.system(buildcommandrouter)

                        if ret !=0:
				failrouterdelete = failrouterdelete + 1
                        else:
				passrouterdelete = passrouterdelete + 1

		passsecuritygroupdelete=0
		failsecuritygroupdelete=0

                for sg in range (self.securitygroupcount):

                        buildcommandsecuritygroup ='neutron security-group-delete securitygroup'+str(sg)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+''
                        ret = os.system(buildcommandsecuritygroup)

                        if ret !=0:
				failsecuritygroupdelete = failsecuritygroupdelete + 1
                        else:
				passsecuritygroupdelete = passsecuritygroupdelete + 1

		passfloatingipdelete=0
		failfloatingipdelete=0

		buildcommandfloatingip ='for f in $(neutron floatingip-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' | awk  \'{print $2}\'); do neutron floatingip-delete --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url '+self.OS_AUTH_URL+' $f; done'
		ret = os.system(buildcommandfloatingip)

		if ret !=0:
			failfloatingipdelete = failfloatingipdelete + 1
		else:
			passfloatingipdelete = passfloatingipdelete + 1

                ## Till this point logical resource deletion for each tenant is completed  ##

	        print '####### summary of '+ self.tenant +' run #######'
	        print 'For ' + self.tenant \
	            + ' floatingip delete PASS = %d FAIL = %d' \
	            % (passfloatingipdelete, failfloatingipdelete)

	        print 'For ' + self.tenant \
	            + ' router delete PASS = %d FAIL = %d' \
	            % (passrouterdelete, failrouterdelete)

	        print 'For ' + self.tenant \
	            + ' network delete PASS = %d FAIL = %d' \
	            % (passnetworkdelete, failnetworkdelete)

	        print 'For ' + self.tenant \
	            + ' port delete PASS = %d FAIL = %d' \
	            % (passportdelete, failportdelete)

	        print 'For ' + self.tenant \
	            + ' securitygroup delete PASS = %d FAIL = %d' \
	            % (passsecuritygroupdelete, failsecuritygroupdelete)


	        totalapipass=passfloatingipdelete+passrouterdelete+passnetworkdelete+passportdelete+passsecuritygroupdelete

	        totalapifail=failfloatingipdelete+failrouterdelete+failnetworkdelete+failportdelete+failsecuritygroupdelete

	        totalapi=totalapipass+totalapifail
	        percentagepass=(totalapipass/totalapi*100)
	        percentagefail=(totalapifail/totalapi*100)
	        print 'For '+ self.tenant +' TOTAL API = %d PASS = %d FAIL = %d' %(totalapi,totalapipass,totalapifail)
	        print 'For '+ self.tenant +' PASS PERCENTAGE = %d FAIL PERCENTAGE = %d' %(percentagepass,percentagefail)
	        print '############################ END '+self.tenant+' END ##################################'



                ## DELETION OF TENANT USER ##
	
                buildcommandtenantdelete ='keystone --os-tenant-name '+self.OS_TENANT_NAME+' --os-username '+self.OS_USERNAME+' --os-password '+self.OS_PASSWORD+' --os-auth-url '+self.OS_AUTH_URL+' tenant-delete '+self.tenant+''
                ret = os.system(buildcommandtenantdelete)

                buildcommanduserdelete ='keystone --os-tenant-name '+self.OS_TENANT_NAME+' --os-username '+self.OS_USERNAME+' --os-password '+self.OS_PASSWORD+' --os-auth-url '+self.OS_AUTH_URL+' user-delete '+self.tenant+'user'
                ret = os.system(buildcommanduserdelete)
	
#boilerplate

if __name__ == '__main__':

        for x in range (3):
                thread1= myThread(x)
                thread1.start()


        print "x"

