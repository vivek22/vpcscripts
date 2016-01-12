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


class myThread(threading.Thread):

	def __init__(self,x):
                threading.Thread.__init__(self)
                self.x = x
                self.tenant = 'tenant'+str(x)
                self.networkcount = 5
                self.subnetcount = 4
                self.routercount = 10
                self.portcount = 100
                self.securitygroupcount = 50
                self.securitygrouprulecount = 1
                self.floatingipcount = 5

        def run(self):




                ## Tenant network logical resource deletion ##
		## Port delete ##
		## Subnet delete ##
		## Network delete ##
		## Security group deete ##

                #for p in range (self.portcount):
		
                buildcommandport ='for p in $(neutron port-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/ | awk  \'{print $2}\'); do neutron port-delete --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/ $p; done'
                print buildcommandport
                ret = os.system(buildcommandport)

                if ret !=0:
                	print 'fail of port deletion'
                else:
                	print 'pass of port deletion'

                for n in range (self.networkcount):

                        buildcommandnetwork ='neutron net-delete network'+str(n)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
                        print buildcommandnetwork
                        ret = os.system(buildcommandnetwork)

                        if ret !=0:
                                print 'fail of network deletion'
                        else:
                                print 'pass of network deletion'


                for r in range (self.routercount):

                        buildcommandrouter ='neutron router-delete router'+str(r)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
                        print buildcommandrouter
                        ret = os.system(buildcommandrouter)

                        if ret !=0:
                                print 'fail of router deletion'
                        else:
                                print 'pass of router deletion'

		## Note : need to add rule deletion code , skipping fornow as directly remove security group having rules inside unless associated with port works ## 

                for sg in range (self.securitygroupcount):

                        buildcommandsecuritygroup ='neutron security-group-delete securitygroup'+str(sg)+' --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/'
                        print buildcommandsecuritygroup
                        ret = os.system(buildcommandsecuritygroup)

                        if ret !=0:
                                print 'fail of securitygroup deletion'
                        else:
                                print 'pass of securitygroup deletion'


		buildcommandfloatingip ='for f in $(neutron floatingip-list --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/ | awk  \'{print $2}\'); do neutron floatingip-delete --os-username '+self.tenant+'user --os-password pass --os-tenant-name '+self.tenant+' --os-auth-url https://identity.jiocloud.com:5000/v2.0/ $f; done'
		print buildcommandfloatingip
		ret = os.system(buildcommandfloatingip)

		if ret !=0:
			print 'fail of floatingip deletion'
		else:
			print 'pass of floatingip deletion'

                ## Till this point logical resource deletion for each tenant is completed  ##


                ## DELETION OF TENANT USER ##

                buildcommandtenantdelete ='keystone --os-tenant-name openstack --os-username admin --os-password Chang3M3 --os-auth-url https://identity.jiocloud.com:5000/v2.0/ tenant-delete '+self.tenant+''
                print buildcommandtenantdelete
                ret = os.system(buildcommandtenantdelete)

                if ret !=0:
                        print 'fail of tenant delete'
                else:
                        print 'pass of tenant delete'

                buildcommanduserdelete ='keystone --os-tenant-name openstack --os-username admin --os-password Chang3M3 --os-auth-url https://identity.jiocloud.com:5000/v2.0/ user-delete '+self.tenant+'user'
                print buildcommanduserdelete
                ret = os.system(buildcommanduserdelete)

                if ret !=0:
                        print 'fail of user delete'
                else:
                        print 'pass of user delete'


                ##Till this point logical resources for each tenant is deleted  ##


		##deletion using awk makes 3 step deletion little slow in big environments ##
		##check should be implemented to check after i decrementor while deletion if anything left behind delete using awk method ##



#boilerplate

if __name__ == '__main__':

        for x in range (3):
                thread1= myThread(x)
                thread1.start()


        print "x"

