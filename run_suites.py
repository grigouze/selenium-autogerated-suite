#!/usr/bin/python

"""

Generate test suite with test case for selenium

"""

# $Id: run_suites.py 15971 2011-04-27 17:11:08Z mickael $

import os
import re
import commands

class Suites:
    """
    class for generate test suites
    """

    @staticmethod
    def print_html(files_list, title):
        """
        print the html suite
        """

        htmlbody = ""

        for myfiles in files_list:
            htmlbody = htmlbody + '<tr><td><a href="%s">%s</a></td></tr>' \
                % ( myfiles, myfiles )

        return '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head><meta content="text/html; charset=UTF-8" http-equiv="content-type" /><title>Test Suite %s</title></head><body><table id="suiteTable" cellpadding="1" cellspacing="1" border="1" class="selenium"><tbody><tr><td><b>Test Suite %s</b></td></tr>%s</tbody></table></body></html>''' % ( title, title, htmlbody )


    def __init__(self):
        dirstart = "suites"
        removes = [ '.svn' ]
        file_format = 'html'
        test_suite_name = '_generatedTestSuite.%s' % file_format
        self.all = [ ]

        for root, dirs, files in os.walk(dirstart):
            for remove in removes:
                if remove in dirs:
                    dirs.remove(remove)

            testcases = []

            if len(files):
                okhtml = 0
                for myfile in files:
                    if myfile.endswith('.%s' % file_format) and \
                        myfile != test_suite_name:
                        okhtml = okhtml + 1
                        testcases.append( myfile )

                if okhtml > 0:
                    newname = re.sub('^\./', '', root)
                    test_suite = re.sub('/', '_', newname) + test_suite_name
                    test_suite = re.sub('^' + dirstart + '_', '', test_suite)
                    myf = open(root + '/' + test_suite, 'w')
                    testcases.sort()
                    myf.write(self.print_html(testcases, newname))
                    myf.close()
                    self.all.append(root + '/' + test_suite)

if __name__ == '__main__':
    print "Removing *_generatedTestSuite*.html\n"
    commands.getoutput("find suites -name '*_generatedTestSuite*.html' -delete")

    print "Removing reports/*.html\n"
    commands.getoutput('rm -rf reports/*.html')

    mysuites = Suites()

    for suite in mysuites.all:
        print "exec suite '%s'" % suite
        report = suite.split('/')[-1]
        print "report %s" % report

        command = 'java -jar jar/selenium-server.jar -userExtensions extensions/user-extensions.js -htmlSuite "*firefox browser/firefox/firefox-bin" "https://web-v3.dev.gandi.net" "%s" "reports/%s"' % ( suite, report )

        print command

        res = commands.getoutput(command)
        print res
