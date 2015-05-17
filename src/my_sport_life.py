#!/usr/bin/env python

'''
MySportLife, Martin Dvorak, 2015

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

@author: martin.dvorak@mindforger.com
'''

import yaml
from datetime import datetime

l18nweekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class MySportLife:
    '''
    Main class.
    '''
        
    def __init__(self, configurationFilePath):
        self.configurationFilePath

    def generate(self):
        pass


class MySportLifeConfiguration:
    '''
    My sport life configuration.
    '''

    def __init__(self, configurationFileName):
        self.configurationFileName = configurationFileName
        stream = open(self.logFileName, 'r')
        self.configuration = yaml.load(stream, Loader=yaml.CLoader)

    def getConfiguration(self):
        return self.configuration


class MySportLifeException(Exception):
    def __init__(self, value):
        self.value = value         
    def __str__(self):
        return repr(self.value)


class TrainingLog:
    '''
    Aggregated training logs across all years.
    
    The beauty of Python+YAML is that YAML files are loaded
    to native Python structures (lists, maps, ...). Thus YAML
    drives Python data structures and code here only performs
    traversal and analytics of these structures.    
    '''

    def __init__(self, logFileName):
        self.logFileName = logFileName
        # TODO load all data files declared in config.yaml and merge them
        stream = open(self.logFileName, 'r')
        self.log = yaml.load(stream, Loader=yaml.CLoader)

    def getLog(self):
        return self.log


class ActivityTotals:
    '''
    Total summary for a particular sport activity - used as dictionary value.
    '''
    days = set([]);
    phases = [];
    km = 0;
    seconds = 0;
    
    def __init__(self):
        pass
    
    def add(self, phase):
        self.days.add(phase.get('date'))
        self.phases.append(phase)
        if 'distance' in phase:
            if phase.get('distance').endswith('km'):
                self.km += float(phase.get('distance').replace('km',''))
            else:
                raise MySportLifeException('Unknown unit used in distance {}'.format(phase.get('distance')))
        if 'time' in phase:
            print 'TBD'


class Report:
    '''
    A class that performs analytics calculation on top of aggregated log.
    '''
    
    daysWorthIt = set([])
    sickDays = set([])
    activityTypes = set([])
    activities = {}

    def __init__(self, data):
        self.data = data

    def dateToWeekday(self, year, month, day):
        d = datetime.date(year, month, day)
        return self.l18nweekdays[d.weekday()]

    def calculate(self):
        print 'Processing...'
        for phase in self.data.get('log'):
            monthAndDay=phase.get('date').split('/');
            # TODO weekday=self.dateToWeekday(self.data.get('year'),monthAndDay[0],monthAndDay[1])
            print '  {}/{}/{} {}'.format(self.data.get('year'),monthAndDay[0],monthAndDay[1],'?')
            activity=phase.get('activity')
            if activity == 'sick':
                self.sickDays.add(phase.get('date'))
            else:
                self.daysWorthIt.add(phase.get('date'))
                if activity not in self.activityTypes:
                    self.activityTypes.add(activity)
                    self.activities[phase.get('activity')] = ActivityTotals()
                totals=self.activities.get(phase.get('activity'))
                totals.add(phase)

    # For every piece of equipment evaluate how much 1km cost
    def equipmentCostPerKm(self):
        print 'TBD'

    # For every piece of equipment evaluate how much 1day
    # of ownership cost
    def equipmentCostPerDay(self):
        print 'TBD'

    def byTimeTracksPerActivity(self):
        print 'TBD'
    def byDistanceTracksPerActivity(self):
        print 'TBD'
    def racesPerActivity(self):
        print 'TBD'

    def meDistancePerDayPerActivity(self):
        print 'TBD'
    def meDistancePerDayAllActivities(self):
        print 'TBD'
    def meTotalUnitsForEachActivity(self):
        print 'TBD'


class TxtLogGenerator:
    
    def __init__(self, targetDirectoryPath, report):
        self.targetDirectoryPath = targetDirectoryPath
        self.report = report
        
    def generate(self):
        # TODO make this single string
        print '\nReport:'
        print '  Active days: {}'.format(len(report.daysWorthIt))
        print '  Sick days: {}'.format(len(report.sickDays))
        print '  Phases: {}'.format(len(report.data.get('log'))-len(report.sickDays))
        print '  Running phases: {}'.format(report.totalRunningPhases)
        print '  Running km: {}'.format(report.totalRunningKm)
        print '  Concept2 phases: {}'.format(report.totalConcept2Phases)
        print '  Concept2 km: {}'.format(report.totalConcept2Km)
        print '\n'

htmlPagePrefix='''\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{}</title>
    <link href='./style.css' rel='stylesheet' type='text/css'>
  </head>
  <body>
    <center>
'''

htmlPageTitle='''      <div class="life-title">{}</div>'''

htmlPageSuffix='''
    </center>
  </body>
</html>
'''

htmlAllYearsSummaryTablePrefix='''
    <table>
    <tr>
      <td>Total</td>
      <td>Running</td>
      <td>Biking</td>
      <td>Rowing</td>
      <td>Skiing</td>
      <td>Swimming</td>
    </tr>
'''

htmlAllYearsSummaryTableSuffix='''
    </table>
'''
     
class HtmlLogGenerator:
    
    def __init__(self, targetDirectoryPath, report):
        self.targetDirectoryPath = targetDirectoryPath
        self.report = report
        
    def generate(self):
        self.generateIndexFile()

    def generateIndexFile(self):
        filePath = self.targetDirectoryPath+'/index.html'
        f = open(filePath, "w")
        f.write(htmlPagePrefix.format('My Sport Life'))
        f.write(htmlPageTitle.format('My Sport Life'))
        self.writeAllYearsSummaryTable(f)
        f.write(htmlPageSuffix)
        f.close()
        
    def writeAllYearsSummaryTable(self, f):
        f.write('\n      <table>')
        f.write('\n        <th>')
        for activityType in self.report.activityTypes:
            f.write('\n          <td>{}</td>'.format(activityType))
        f.write('\n        </th>')
        f.write('\n        <tr>')
        for activityType in self.report.activityTypes:
            f.write('\n          <td>{}</td>'.format(self.report.activities.get(activityType).km))
        f.write('\n        </tr>')
        f.write('\n      </table>')

# main()

#log = TrainingLog("config.yaml")
log = TrainingLog('../examples/20-years/2015.yaml')
report = Report(log.getLog())
report.calculate()
# txtLog = TxtLogGenerator('/home/dvorka/tmp/20years',report)
# txtLog.generate()
htmlLog = HtmlLogGenerator('/home/dvorka/tmp/20years',report)
htmlLog.generate()

# eof
